from collections import defaultdict
import pandas as pd
import numpy as np
import operator
import sqlite3
import re


def replace_0_by_1(data):
    values = data['values'].values
    out = []
    for v in values:
        if v == 0:
            out.append(1)
        else:
            out.append(v)
    data['values'] = out
    return data

def remove_first_trailing_ws(data):
    tags = data['tag']
    out = []
    for t in tags:
        if t[0] == " ":
            out.append(t[1:])
        elif t[-1] == " ":
            out.append(t[:-1])
        else: 
            out.append(t)
    data['tag'] = out
    return data


def extract_tag_values(data, tag_contains, parse_value, replace=False):
    tag_values = data['tag']
    tags_out = []
    values = data['tag_value']
    values_out = []
    for i in range(len(tag_values)):
        t = tag_values[i]
        v = values[i]
        replace_value = None
        if tag_contains in t.lower():
            if '[xx]' not in t:
                val = parse_value(t)
                if not len(val) == 1:
                    import ipdb; ipdb.set_trace() # BREAKPOINT
                    print "%s [ERROR] Did not find value in %s" % (__name__, t)
                else:
                    replace_value = val[0]
        if replace_value is not None:
            if replace:
                tags_out.append(t.replace(replace_value,"[xx]"))
            else:
                tags_out.append(tag_contains)
            values_out.append(replace_value)
        else:
            tags_out.append(t)
            values_out.append(v)
    data['tag'] = tags_out
    data['tag_value'] = values_out
    return data


def shrink_tags(data, tag_parse_map, replace=False):
    bef = float(len(data['tag'].unique()))
    for t in tag_parse_map.keys():
        regex = tag_parse_map[t]
        data = extract_tag_values(data, t, regex, replace=replace)
        aft = float(len(data['tag'].unique())) 
        perc = 100. * aft / bef 
        print "%s [INFO] tags shrunk at %s percent after parsing %s" % (__name__, perc, t)  
    return data


def print_unique_tag_count(data):
    count = defaultdict(lambda: 1)
    for t in data['tag']:
        count[t] += 1
    for k,v in sorted(count.items(), key=operator.itemgetter(1), reverse=True):
        print "%06i: %s" % (v,k)


def parse_annee_construction_value(text):
    return re.findall(r"\d*\d*\d*\d", text)


def parse_dispo_value(text):
    return re.findall(r"\d\d\/\d\d\/\d\d\d*\d*", text)


def parse_orientation_value(text):
    out = []
    finds = re.findall(r"(nord)|(est)|(ouest)|(sud)", text.lower())
    for y in finds:
        for x in y:
            if len(str(x)) > 0:
                out.append(str(x))
    return ["_".join(sorted(out))]


def parse_chauffage_value(text):
    out = []
    features = [
            "central",
            "fuel",
            "mixte",
            "gaz",
            "sol",
            "climatisation",
            "collectif",
            "individuel",
            "sol",
            "electrique",
            "fuel",
            "radiateur",
            ]
    for f in features:
        if f in str(text):
            out.append(f)
    return [";".join(out)]


def parse_cuisine_value(text):
    out = []
    features = [
            'americaine',
            'aucune',
            'coin',
            'equipee',
            'industrielle',
            'separee',
            ]
    for f in features:
        if f in str(text):
            out.append(f)
    return [";".join(out)]


def parse_m2(text):
    out = str(text.split("m2")[0])
    out = out.replace(" ","")
    return [out]


def parse_deux_points(text):
    out = str(text.split(":",)[-1])
    out = out.replace(" ", "")
    return [out]


def replace_name_tag(data, name_map):
    out = []
    for t in data['tag']:
        for n in name_map.keys():
            if n in t.lower():
                replace = n if name_map[n] is None else name_map[n]
                out.append(replace)
                break
        else:
            out.append(t.lower())
    data['tag'] = out
    return data


def drop_bullshit(data, cutoff):
    n = len(data['tag'].values)
    cutoff_val = cutoff * n 
    count = defaultdict(lambda: 1)
    for t in data['tag']:
        count[t] += 1
    for k in count.keys():
        if count[k] < cutoff_val:
            print "%s [INFO] Dropping %s, only %s occurences out of %s" % (__name__, k, count[k], n)
            data = data[data['tag'] != k]
    return data 


if __name__ == "__main__":
    tag_parse_map = {
            'annee de construction': parse_annee_construction_value,
            'disponibilite': parse_dispo_value,
            'orientation': parse_orientation_value,
            'chauffage': parse_chauffage_value,
            'cuisine': parse_cuisine_value,
            }
    tag_split = {
            'm2': parse_m2,
            ':': parse_deux_points,
            }
    tag_name_map = { 
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
            }
    con = sqlite3.connect("./data/raw_data.db")
    tags = pd.read_sql_query("SELECT * FROM TAGS", con)
    tags = remove_first_trailing_ws(tags)
    tags = shrink_tags(tags, tag_parse_map)
    tags = shrink_tags(tags, tag_split, replace=True)
    tags = replace_name_tag(tags, tag_name_map)
    tags = drop_bullshit(tags, 0.0001)
    print_unique_tag_count(tags)
    # for x in sorted(np.unique([ x for x in tags['tag'].values if 'cuisine' in x.lower()])):
        # print x

