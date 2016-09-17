import re
import sqlite3
import pandas as pd
from collections import defaultdict


class TagParser(object):
    def __init__(self):
        self.replace_name_to = {
                        'etage': None,
                        'surface': None,
                        'piece': None,
                        'toilette': None,
                        'cave': None,
                        'bain': 'salle de bain',
                        'eau' : 'salle de bain',
                        'balcon': None,
                        'parking': None,
                        'terrasse': None,
                        'manger': 'salle a manger',
                        'box': None,
                        'chambre': None,
                        'sejour': None,
                        'toilette': None,
                        'cable': None,
                        'ges': None,
                        'dpe': None,
                        'situation': None,
                        'annee de construction': None,
                        'disponibilite': None,
                        'orientation': None,
                        'chauffage': None,
                        'cuisine': None,
                        'travaux a prevoir': None,
                        }
        self.tokens = {
                'chauffage': [
                            "central",
                            "fuel",
                            "mixte",
                            "gaz",
                            "sol",
                            "climatisation",
                            "collectif",
                            "individuel",
                            "electrique",
                            "fuel",
                            "radiateur",
                            ],
                'cuisine': [
                            'americaine',
                            'aucune',
                            'coin',
                            'equipee',
                            'industrielle',
                            'separee',
                            ],
                'orientation': [
                            'ouest',
                            'est',
                            'nord',
                            'sud',
                            ]
                    }

    def process_tag(self, tag):
        m2 = True if "m2" in tag else False
        tag = tag.lower().replace("m2","[xx]")
        tag, tokens = self.find_token(tag)
        tag, num = self.find_num(tag)
        name = self.clean_name(tag)
        name = name + "_m2" if m2 else name
        value = tokens if tokens is not None else None
        value = num if value is None else value
        value = '' if value is None else value
        return (name, value)
    
    def find_num(self, tag):
        match = re.findall(r'([^m]{0,1}\d+)', tag)
        for m in match:
            tag = tag.replace(m, '[xx]')
        value = ''.join(match).replace(' ', '') if len(match)>0 else None
        return tag, value

    def find_token(self, tag):
        out = []
        for category in self.tokens.keys():
            if category in tag:
                for tok in self.tokens[category]:
                    if tok in tag:
                        out.append(tok)
                        tag = tag.replace(tok,'[xx]')
        out = ','.join(sorted(out)) if len(out) > 0 else None
        return tag, out

    def clean_name(self, tag):
        out = ""
        for name in self.replace_name_to:
            if name in tag:
                to_name = self.replace_name_to[name]
                out = name if to_name is None else to_name
                break
        else: 
            to_erase = ["[xx]", ":", "-", ",", " ", "."]
            for er in to_erase:
                tag = tag.replace(er,"")
            out = tag
        return out


class UpdateDBTags(object):
    def __init__(self, db, parser, dry_run=True):
        self.db = db
        self.dry_run = dry_run
        self.parser = parser
        self.changes = defaultdict(lambda: defaultdict())

    def run(self):
        self.initialize()
        tags = pd.read_sql_query("SELECT * FROM TAGS", self.con)
        self.collect_changes(tags)
        self.apply_changes_if_not_dry()
        self.close()

    def initialize(self):
        print("Connecting to %s ..." % self.db)
        self.con = sqlite3.connect(DATABASE)

    def collect_changes(self, tags):
        print("Collecting Changes ...")
        for i in range(len(tags)):
            ID, tag, tag_name, tag_value = tags.iloc[i]
            new_tag_name, new_tag_value = self.parser.process_tag(tag)
            if new_tag_name != tag_name or new_tag_value != tag_value:
                self.changes[(ID, tag)]['old'] = (tag_name, tag_value) 
                self.changes[(ID, tag)]['new'] = (new_tag_name, new_tag_value)
                if dry_run:
                    print "-- Parse Function diff: [%s] %s:" % (ID, tag)
                    print "     > Old: %s, %s" % (tag_name, tag_value)
                    print "     > New: %s, %s" % (new_tag_name, new_tag_value)

    def apply_changes_if_not_dry(self):
        n = len(self.changes)
        if n == 0:
            print "No changes ! DB tags are up to date !"
        elif self.dry_run:
            print "Did NOT Apply Changes in database: %s !" % self.db
        else:
            print "Applying %s Changes in database: %s..." % (n, self.db)
            for ID, tag in self.changes:
                new_tag_name, new_tag_value = changes[(ID, tag)]['new']
                self.con.execute("UPDATE tags SET tag_name=?, tag_value=? WHERE ID=? AND tag=?",
                            (new_tag_name, new_tag_value, ID, tag)
                        )
            print "... Done !"

    def close(self):
        self.con.commit()
        self.con.close()
        print("Connexion to DB %s closed!" % self.db)
        

if __name__ == "__main__":
    from settings import DATABASE

    dry_run = True
    parser = TagParser()

    update_engine = UpdateDBTags(DATABASE, parser, dry_run=dry_run)
    update_engine.run()

