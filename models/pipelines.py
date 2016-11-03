from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from collections import defaultdict
import pandas as pd
import numpy as np
from tqdm import tqdm


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

    def get_feature_names(self):
        feature_names = self.key if isinstance(self.key, list) else [self.key]
        return feature_names


class MyOneHotEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, do_parse=False, delim=","):
        self.do_parse = do_parse
        self.delim = delim
        self.features = []

    def fit(self, x, y=None):
        return self

    def parse(self, st):
        if pd.isnull(st):
            return []
        else:
            return st.split(self.delim)

    def check_with_previously_fitted(self, feats, data_len):
        if len(self.features) == 0:
            self.features = feats.keys()
        else:
            for f in self.features:
                if f not in feats:
                    feats[f]
            for f in feats.keys():
                if f not in self.features:
                    # This feature is unkown to the model... we drop it !
                    del feats[f]
        return feats

    def transform(self, data):
        # TODO: split between fit / transform.
        n = len(data)
        features = defaultdict(lambda: np.zeros(n))
        name = data.columns[0]

        for i in tqdm(range(n)):
            value = data.iloc[i].values[0]
            values = self.parse(value) if self.do_parse else [value]
            for v in values:
                features["%s=%s" % (name, v.lower())][i] += 1
        features = self.check_with_previously_fitted(features, n)
        df = pd.DataFrame(features, dtype=int, index=data.index)
        return df

    def get_feature_names(self):
        return self.features


class FindReplace(BaseEstimator, TransformerMixin):
    def __init__(self, find_replace_map):
        self.fr_map = find_replace_map

    def fit(self, x, y=None):
        return self

    def transform(self, data):
        for col in data.columns:
            for key, val in self.fr_map:
                data.at[:, col] = data[col].apply(
                                                 lambda x: x.replace(key, val)
                                                 ).values
        return data


class Debug(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, data):
        import ipdb; ipdb.set_trace() # BREAKPOINT
        return data


class ReplaceNaN(BaseEstimator, TransformerMixin):
    def __init__(self, replace_by):
        self.replace_by = replace_by

    def fit(self, x, y=None):
        return self

    def transform(self, data):
        data.fillna(self.replace_by, inplace=True)
        return data


class PandasFeatureUnion(FeatureUnion):
    def transform(self, data):
        data = super(PandasFeatureUnion, self).transform(data)
        import ipdb; ipdb.set_trace() # BREAKPOINT

