from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

def train_model(X_train, y_train):
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)

    clf = MultinomialNB()
    clf.fit(X_train_vec, y_train)

    # Save both
    joblib.dump(clf, "spam_model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")

    return clf, vectorizer
