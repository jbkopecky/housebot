from pipelines import ItemSelector
from pipelines import MyOneHotEncoder
from pipelines import FindReplace
from pipelines import ReplaceNaN
from utils import plot_results

from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn import ensemble
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fr_arrondissement = [
                ("Le ", ""),
                ('-', "_"),
                (' ', "_"),
                ('Saint', 'st'),
                ('_le_Pont', ''),
                ('_Perret', ''),
                ]

params = {
        'n_estimators': 500,
        'max_depth': 4,
        'min_samples_split': 1,
        'learning_rate': 0.01,
        'loss': 'ls',
        'verbose': 2,
        }

model = Pipeline([
    ('Union', FeatureUnion([
        ('Surface', Pipeline([
            ('Selection', ItemSelector(['surface_m2'])),
            ('Normalise', StandardScaler()),
            ]),
         ),
        ('Arrondissement', Pipeline([
            ('Selection', ItemSelector(['arrondissement'])),
            ('Clean', FindReplace(fr_arrondissement)),
            ('MyOneHotEncoder', MyOneHotEncoder()),
            ('Normalise', MinMaxScaler()),
            ]),
         ),
        ('orientation', Pipeline([
            ('Selection', ItemSelector(['orientation'])),
            ('Encoder', MyOneHotEncoder(do_parse=True)),
            ('Replace_NaN', ReplaceNaN(0.)),
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
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('best', TruncatedSVD(n_components=500)),
            ]),
         ),
        ('General', Pipeline([
            ('Selection', ItemSelector(['balcon', 'visavis', 'piscine',
                                        'box', 'meuble', 'refaitaneuf'])),
            ('Replace_NaN', ReplaceNaN(0.)),
            ('Normalise', MinMaxScaler()),
            ]),
         ),
        ], n_jobs=-1),
     ),
    ('gb', ensemble.GradientBoostingRegressor(**params)),
    ])


X,y = make_xy_data('./data/merged_data.csv', ['surface_m2', 'piece'])

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2)

model.fit(X_train, y_train)

joblib.dump(model, "./models/linear_model.pckl")

y_test_pred = model.predict(X_test)
y_train_pred = model.predict(X_train)

train_error = mean_squared_error(y_train_pred, y_train)
test_error = mean_squared_error(y_test_pred, y_test)

print "Train error: ", train_error
print "Test error: ", test_error

plot_results([[y_train_pred, y_train], [y_test_pred, y_test]])
plt.savefig("./plots/GBoost_model_errors_with_description.png")
plt.show()
