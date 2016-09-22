from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cross_validation import train_test_split
import pandas as pd


text_tfidf = Pipeline([
                ('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ])


parameters = {
            'vect__max_df': (0.5, 0.75, 1.0),
            #'vect__max_features': (None, 5000, 10000, 50000),
            'vect__ngram_range': ((1, 1), (1, 2)),
            # unigrams or bigrams
            #'tfidf__use_idf': (True, False),
            #'tfidf__norm': ('l1', 'l2'),
            }


if __name__ == "__main__":
    data = pd.read_csv('data/merged_data.csv', index_col=0)
    data = data[['prix', 'surface_m2', 'description']]
    print len(data)
    data = data.dropna()
    print len(data)
    y = data['prix'] / data['surface_m2']
    X = data['description']

    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=42)

    text_tfidf.fit_transform(X_train, y_train)

    import ipdb; ipdb.set_trace() # BREAKPOINT

