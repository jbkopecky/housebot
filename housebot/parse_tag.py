import re

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
        tag = tag.lower().replace("m2","[xx]")
        tag, tokens = self.find_token(tag)
        tag, num = self.find_num(tag)
        name = self.clean_name(tag)
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

if __name__ == "__main__":
    import pandas as pd
    import sqlite3

    con = sqlite3.connect("./data/raw_data.db")
    tags = pd.read_sql_query("SELECT * FROM TAGS", con)
    tags = tags['tag'].values

    Parser = TagParser()

    for t in tags[:696]:
        print t, Parser.process_tag(t)




