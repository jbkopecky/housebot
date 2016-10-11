from pipelines import ItemSelector
from pipelines import MyOneHotEncoder
from pipelines import FindReplace
from pipelines import Debug

from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import FeatureHasher
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model as lm
from sklearn.metrics import explained_variance_score

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_results(data):
    # Plot results: Train / Test cross plot. 
    # data: [[y_train_pred, y_train], [y_test_pred, y_test]]
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    style = {
            'alpha': 0.8,
            's': 20.,
            'lw': 0.,
            }
    for i,ax in enumerate(axes):
        y_pred = data[i][0]
        y_actual = data[i][1]
        ax.scatter(y_pred, y_actual, c='grey', **style)
        ax.plot([0.,100000.],[0.,100000.], c='b')
        ax.plot([0.,75000.],[0.,100000.], c='b')
        ax.plot([0.,100000.],[0.,75000.], c='b')
        ax.set_xlabel('Predicted Price per m2')
        ax.set_ylabel('Actual Price per m2')
        ax.set_title('Model Errors')
        ax.set_ylim(0., 47000.)
        ax.set_xlim(0., 18000.)
    plt.show()


fr_arrondissement = [ 
                ("Le ", ""),
                ('-', "_"),
                (' ', "_"),
                ('Saint', 'st'),
                ('_le_Pont', ''),
                ('_Perret', ''),
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
            ]),
        ),
        # ('Agency', Pipeline([
        #     ('Selection', ItemSelector(['agency_phone'])),
        #     ('MyOneHotEncoder', MyOneHotEncoder()),
        #     ]),
        ('Max_Etages', Pipeline([
            ('Selection', ItemSelector(['etage', 'etage 2'])),
            ('Imputer', Imputer(strategy="most_frequent")),
            ]),
        ),
        ('NoNaNFeats', Pipeline([
            ('Selection', ItemSelector(['piece'])),
            ]),
        ),
        ]),
    ),
    ('Deb', Debug()),
    ('NormaliseMinMax', MinMaxScaler()),
    # ('lm', BayesianRidge(verbose=True)),
    ('lm', lm.BayesianRidge()),
    ])

data = pd.read_csv('./data/merged_data.csv', index_col=0)

n = len(data)
data = data.dropna(subset=['surface_m2', 'piece'])
print "[Warning] dropped %s samples because of NaN values"  % (n-len(data))

y = np.divide(data[['prix']].astype(float).values.T, data[['surface_m2']].astype(float).values.T)[0]
X = data.drop(['prix'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=2)

pipeline.fit(X_train, y_train)

y_test_pred = pipeline.predict(X_test)
y_train_pred = pipeline.predict(X_train)

plot_results([[y_train_pred, y_train], [y_test_pred, y_test]])

