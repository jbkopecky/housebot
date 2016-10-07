from sklearn.base import BaseEstimator, TransformerMixin
from collections import defaultdict
import pandas as pd
import numpy as np


class ItemSelector(BaseEstimator, TransformerMixin):
    """For data grouped by feature, select subset of data at a provided key.

    The data is expected to be stored in a 2D data structure, where the first
    index is over features and the second is over samples.  i.e.

    >> len(data[key]) == n_samples

    Please note that this is the opposite convention to sklearn feature
    matrixes (where the first index corresponds to sample).

    ItemSelector only requires that the collection implement getitem
    (data[key]).  Examples include: a dict of lists, 2D numpy array, Pandas
    DataFrame, numpy record array, etc.

    >> data = {'a': [1, 5, 2, 5, 2, 8],
    'b': [9, 4, 1, 4, 1, 3]}
    >> ds = ItemSelector(key='a')
    >> data['a'] == ds.transform(data)

    ItemSelector is not designed to handle data grouped by sample.  (e.g. a
    list of dicts).  If your data is structured this way, consider a
    transformer along the lines of `sklearn.feature_extraction.DictVectorizer`.

    Parameters
    ----------
    key : hashable, required
    The key corresponding to the desired value in a mappable.
    """
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]

class GoThrough(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, data):
        return self

class MyOneHotEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, do_parse=False, delim=","):
        self.do_parse = do_parse
        self.delim = delim

    def fit(self, x, y=None):
        return self

    def parse(self, st):
        return st.split(self.delim)

    def transform(self, data):
        features = defaultdict(lambda: np.zeros(len(data)))
        name = data.columns[0]
        for i in range(len(data)):
            value = data.iloc[i].values[0]
            values = self.parse(value) if self.do_parse else [value]
            for v in values:
                features["%s=%s" % (name, v.lower())][i] += 1
        df = pd.DataFrame(features, dtype=int, index=data.index)
        return df

class FindReplace(BaseEstimator, TransformerMixin):
    def __init__(self, find_replace_map):
        self.fr_map = find_replace_map

    def fit(self, x, y=None):
        return self

    def transform(self, data):
        for key, val in self.fr_map:
            data = data.apply(lambda x: x.replace(key, val))
        return data

class Debug(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, data):
        print data.head()
        return data
        

