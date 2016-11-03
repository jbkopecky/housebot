from pipelines import ItemSelector
from pipelines import MyOneHotEncoder
from pipelines import FindReplace
from pipelines import ReplaceNaN
from utils import plot_ic_criterion
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
            ('best', TruncatedSVD(n_components=1000)),
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

model_bic = lm.LassoLarsIC(criterion='bic', verbose=2)
t1 = time.time()
model_bic.fit(X_tr, y_train)
t_bic = time.time() - t1
alpha_bic_ = model_bic.alpha_

model_aic = lm.LassoLarsIC(criterion='aic', verbose=2)
model_aic.fit(X_tr, y_train)
alpha_aic_ = model_aic.alpha_

plt.figure()
plot_ic_criterion(model_aic, 'AIC', 'b')
plot_ic_criterion(model_bic, 'BIC', 'r')
plt.legend()
plt.title('Information-criterion for model selection (training time %.3fs)'
          % t_bic)
plt.show()

###############################################################################
