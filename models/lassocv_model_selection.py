from pipelines import ItemSelector
from pipelines import MyOneHotEncoder
from pipelines import FindReplace
from pipelines import ReplaceNaN
from utils import make_xy_data

from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn import linear_model as lm
import matplotlib.pyplot as plt
import numpy as np
import time


###############################################################################

fr_arrondissement = [
                ("Le ", ""),
                ('-', "_"),
                (' ', "_"),
                ('Saint', 'st'),
                ('_le_Pont', ''),
                ('_Perret', ''),
                ]

features = Pipeline([
    ('Union', FeatureUnion([
        ('Surface', Pipeline([
            ('Selection', ItemSelector(['surface_m2'])),
            ('Normalise', MinMaxScaler()),
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
            ('best', TruncatedSVD(n_components=200)),
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
    ])

X, y = make_xy_data('./data/merged_data.csv', ['surface_m2', 'piece'])

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=2)

X_tr = features.fit_transform(X_train, None)
X_te = features.transform(X_test)

###############################################################################

t1 = time.time()
model = lm.LassoCV(cv=20, verbose=2).fit(X_tr, y_train)
t = time.time() - t1

# Display results
m_log_alphas = -np.log10(model.alphas_)
plt.figure()
plt.plot(m_log_alphas, model.mse_path_, ':')
plt.plot(m_log_alphas, model.mse_path_.mean(axis=-1), 'k',
         label='Average across the folds', linewidth=2)
plt.axvline(-np.log10(model.alpha_), linestyle='--', color='k',
            label='alpha: CV estimate')
plt.legend()
plt.xlabel('-log(alpha)')
plt.ylabel('Mean square error')
plt.title('Mean square error on each fold: coordinate descent'
          ' (train time: %.2fs)' % t)
plt.axis('tight')
plt.show()

###############################################################################
