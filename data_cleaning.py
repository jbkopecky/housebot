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


def extract_tag_values(data, tag_contains, parse_value):
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
            # tags_out.append(t.replace(replace_value,"[xx]"))
            tags_out.append(tag_contains)
            values_out.append(replace_value)
        else:
            tags_out.append(t)
            values_out.append(v)
    data['tag'] = tags_out
    data['tag_value'] = values_out
    return data


def shrink_tags(data, tag_parse_map):
    bef = float(len(data['tag'].unique()))
    for t in tag_parse_map.keys():
        regex = tag_parse_map[t]
        data = extract_tag_values(data, t, regex)
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


if __name__ == "__main__":
    tag_parse_map = {
            'annee de construction': lambda x: re.findall(r"\d*\d*\d*\d", x),
            'disponibilite':         lambda x: re.findall(r"\d\d\/\d\d\/\d\d\d*\d*", x),
            'orientation':           lambda x: ["_".join(sorted([
                                                str([ x for x in y if not len(x)==0][0]) 
                                                for y in re.findall(r"(nord)|(est)|(ouest)|(sud)",x.lower())
                                                ]))],
            }
    con = sqlite3.connect("./data/raw_data.db")
    tags = pd.read_sql_query("SELECT * FROM TAGS", con)
    tags = shrink_tags(tags, tag_parse_map)
    # print_unique_tag_count(tags)
    for x in sorted(np.unique([ x for x in tags['tag'].values if 'chauffage' in x.lower()])):
        print x

