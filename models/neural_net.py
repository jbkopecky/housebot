from pipelines import ItemSelector
from pipelines import MyOneHotEncoder
from pipelines import FindReplace
from pipelines import ReplaceNaN
from utils import plot_results
from utils import make_xy_data
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.neural_network import MLPRegressor as nnet
import matplotlib.pyplot as plt


fr_arrondissement = [
                ("Le ", ""),
                ('-', "_"),
                (' ', "_"),
                ('Saint', 'st'),
                ('_le_Pont', ''),
                ('_Perret', ''),
                ]

model = Pipeline([
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
    ('nnet', nnet(activation='logistic', alpha='0.001', random_state=32, verbose=2)),
    ])

X, y = make_xy_data('./data/merged_data.csv', ['surface_m2', 'piece'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=32)

model.fit(X_train, y_train)

y_test_pred = model.predict(X_test)
y_train_pred = model.predict(X_train)

train_error = mean_squared_error(y_train_pred, y_train)
test_error = mean_squared_error(y_test_pred, y_test)

train_title = "Train error: ", train_error
test_title = "Test error: ", test_error

plot_results({train_title: [y_train_pred, y_train],
              test_title: [y_test_pred, y_test]})

plt.savefig("./plots/neural_net.png")
plt.show()
