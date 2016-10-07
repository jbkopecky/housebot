from pipelines import ItemSelector
from pipelines import MyOneHotEncoder
from pipelines import FindReplace
from pipelines import Debug

from sklearn.feature_extraction.text import FeatureHasher

from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import Lasso

import pandas as pd

fr_arrondissement = [ 
                ("Le ", ""),
                ('-', "_"),
                (' ', "_"),
                    ]

pipeline = Pipeline([
    ('Union', FeatureUnion([
        ('Surface', Pipeline([
            ('Selection', ItemSelector(['surface_m2'])),
            ]),
        ),
        ('Arrondissement', Pipeline([
            ('Selection', ItemSelector(['arrondissement'])),
            ('Clean', FindReplace(fr_arrondissement)),
            ('MyOneHotEncoder', MyOneHotEncoder()),
            ('Debug', Debug())
            ]),
        ),
        ])
    ),
    ])

data = pd.read_csv('data/merged_data.csv', index_col=0)
print pipeline.fit_transform(data)

