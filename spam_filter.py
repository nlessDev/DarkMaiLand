import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import numpy as np

class SpamFilter:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=10000)
        self.classifier = SGDClassifier(loss='log_loss')
        self.is_trained = False

    def train(self, spam_dir, ham_dir):
        emails, labels = self._load_data(spam_dir, ham_dir)
        X = self.vectorizer.fit_transform(emails)
        self.classifier.fit(X, labels)
        self.is_trained = True

    def predict(self, email_text):
        if not self.is_trained:
            return 0.0
        X = self.vectorizer.transform([email_text])
        return self.classifier.predict_proba(X)[0][1]

    def _load_data(self, spam_dir, ham_dir):
        # Implementation for loading email data
        pass
