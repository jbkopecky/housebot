import sqlite3
import pandas as pd
import hues
from collections import defaultdict
from tqdm import tqdm
import sklearn


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def reshape_tags(data, index=None, columns=None, values=None):
    if (index is None) or (columns is None) or (values is None):
        return None
    cols = [str(x) for x in data[columns].unique()]
    inds = [int(x) for x in data[index].unique()]
    num_duplicates = defaultdict(lambda: defaultdict(set))
    other_duplicates = defaultdict(lambda: defaultdict(set))
    df = pd.DataFrame(columns=cols, index=inds)
    for i in tqdm(range(len(data))):
        ind, col, val = data.iloc[i][[index, columns, values]]
        ind = int(ind)
        old_val = df.loc[ind, col]
        if pd.isnull(old_val):
             val = 1 if val == '' else val
             df.loc[ind, col] = val
        else:
            if val == "" or df.loc[ind, col] == "":
                df.loc[ind, col] = val if val != "" else df.loc[ind,col]
            elif is_number(val) and is_number(old_val):
                if abs(int(val)) == abs(int(old_val)) and abs(int(val)) == 1:
                    df.loc[ind, col] = '1'
                else:
                    num_duplicates[col][ind].add(old_val)
                    num_duplicates[col][ind].add(val)
            else:
                other_duplicates[col][ind].add(old_val)
                other_duplicates[col][ind].add(val)
                hues.warning("[Warning] Duplicate Value ! [ %s, %s ] : %s vs. %s" % (ind, col, df.loc[ind, col], val))
    if len(other_duplicates) > 0:
        hues("Cannot reshape: Non numerical duplicates ! %s" % other_duplicates)
    else:
        for col in num_duplicates.keys():
            max_duplicate = max([len(x) for x in num_duplicates[col].values()])
            col_names = [col] + [col + " " + str(n+1) for n in range(max_duplicate)[1:]]
            for ind in num_duplicates[col].keys():
                for i,v in enumerate(sorted(num_duplicates[col][ind])):
                    df.loc[ind,col_names[i]] = v
    return df


def reshape_price(data):
    indexes = [int(x) for x in sorted(data['ID'].unique())]
    df = pd.DataFrame(columns=['prix','last_seen'], index=indexes)
    for i in tqdm(range(len(data))):
        ID, time, prix = data.iloc[i]
        ID = int(ID)
        time0 = df.loc[ID]['last_seen']
        if not pd.isnull(time0):
            if int(time0) > int(time):
                continue
        df.loc[ID,'prix'] = int(prix.replace(" ",""))
        df.loc[ID,'last_seen'] = int(time)
    return df


if __name__ == "__main__":
    hues.info("Connecting")
    con = sqlite3.connect("./data/raw_data.db")

    hues.info("Importing annonces ...")
    annonces = pd.read_sql_query("SELECT * FROM annonce", con, index_col='ID')
    annonces = annonces[['arrondissement', 'agency_phone']]
    annonces.index = [int(x) for x in annonces.index]

    hues.info("Importing description ...")
    descriptions = pd.read_sql_query("SELECT * FROM description", con, index_col='ID')
    descriptions.index = [int(x) for x in descriptions.index]

    hues.info("Importing prices ...")
    prices = pd.read_sql_query("SELECT * FROM prix", con)
    prices = reshape_price(prices)

    hues.info("Importing tags ...")
    tags = pd.read_sql_query("SELECT * FROM tags", con)
    tags = tags[tags['tag_name']=='surface_m2']
    tags = reshape_tags(tags, 'ID', 'tag_name', 'tag_value')

    hues.info("* Merging into one dataframe...")
    con.close()
    data = pd.concat([annonces, descriptions, prices, tags], axis=1)
    data = data[['last_seen', 'prix', 'surface_m2', 'description', 'arrondissement']]
    data = data.dropna()
    data['prix_per_m2'] = data['prix'].astype('float') / data['surface_m2'].astype('float')
    data['surface_m2'] = data['surface_m2'].astype('float')
    data = data[['last_seen', 'arrondissement', 'surface_m2', 'prix_per_m2']]
    data.columns = ['date', 'z', 'x', 'y']
    for arr in list(set(data['z'].values)):
        data[data['z']==arr].to_json('../housebot_viz/data/%s.json' % str(arr).replace(" ", "_"), orient='index')

