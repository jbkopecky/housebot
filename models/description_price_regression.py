from pipelines import ItemSelector
from pipelines import Debug
from utils import make_xy_data
from sklearn import linear_model as lm
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from utils import plot_compare_feature_levels
from utils import plot_results
import matplotlib.pyplot as plt
import numpy as np


model = Pipeline([
    ('selection', ItemSelector('description')),
    ('tfidf', TfidfVectorizer(max_df=0.8, min_df=0.1)),
    ('lassocv', lm.LassoCV(verbose=2)),
    ])

if __name__ == "__main__":
    X, y = make_xy_data('./data/merged_data.csv', ['surface_m2', 'piece'])
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.3,
                                                        random_state=2)

    import ipdb; ipdb.set_trace() # BREAKPOINT
    X_transformed = model.fit(X_train, y_train)

    y_test_calc = model.predict(X_test)
    y_train_calc = model.predict(X_train)

    plot_results({
        'test result': [y_test_calc, y_test],
        'train_result': [y_train_calc, y_train],
        })

    plt.show()

    tfidf = model.named_steps['tfidf']
    lasso = model.named_steps['lassocv']
    feats = sorted(zip(
                       np.array(tfidf.get_feature_names())[lasso.coef_ > 0.],
                       np.array(lasso.coef_)[lasso.coef_ > 0.]
                       ), key=lambda x: x[1])
    plot_compare_feature_levels(feats)
    plt.show()

