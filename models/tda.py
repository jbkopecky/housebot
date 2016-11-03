from pipelines import ItemSelector
from pipelines import MyOneHotEncoder
from pipelines import FindReplace

from sklearn.preprocessing import Imputer
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import numpy as np
import pandas as pd
import km


fr_arrondissement = [
                ("Le ", ""),
                ('-', "_"),
                (' ', "_"),
                ('Saint', 'st'),
                ('_le_Pont', ''),
                ('_Perret', ''),
                ]

prepoc = Pipeline([
    ('Union', FeatureUnion([
        ('Surface', Pipeline([
            ('Selection', ItemSelector(['surface_m2'])),
            ('Normalise', MinMaxScaler()),
            ]),
         ),
        ('Max_Etages', Pipeline([
            ('Selection', ItemSelector(['etage', 'etage 2'])),
            ('Imputer', Imputer(strategy="most_frequent")),
            ('Normalise', MinMaxScaler()),
            ]),
         ),
        ('NoNaNFeats', Pipeline([
            ('Selection', ItemSelector(['piece'])),
            ('Normalise', MinMaxScaler()),
                                ]),
         ),
        ('Description', Pipeline([
            ('Selection', ItemSelector('description')),
            ('vect', CountVectorizer(max_features=500)),
            ('tfidf', TfidfTransformer()),
                                 ]),
         ),
        ]),
     ),
    ])

data = pd.read_csv('./data/merged_data.csv', index_col=0)

n = len(data)
data = data.dropna(subset=['surface_m2', 'piece'])
print "[Warning] dropped %s samples because of NaN values" % (n-len(data))

X = np.array(prepoc.fit_transform(data).todense())

mapper = km.KeplerMapper(verbose=2)

projected_data = mapper.fit_transform(X, projection="dist_mean")

complex = mapper.map(projected_X=projected_data, inverse_X=X,
                     clusterer=km.cluster.DBSCAN(
                                                eps=0.8,
                                                n_jobs=-1,
                                                min_samples=10
                                                 ),
                     nr_cubes=10, overlap_perc=0.9
                     )

mapper.visualize(complex, path_html="./plots/test_tda.html",
                 title="Test",
                 color_function="average_signal_cluster"
                 )
