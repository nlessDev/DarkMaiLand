import pytest
import numpy as np
from smtpx.spam_filter import SpamFilter

class TestSpamFilter:
    @pytest.fixture
    def filter(self):
        return SpamFilter()

    def test_spam_classification(self, filter):
        spam_samples = [
            "Free money!!! Click here",
            "You won $1,000,000",
            "Nigerian prince needs help"
        ]
        
        ham_samples = [
            "Meeting rescheduled to tomorrow",
            "Project update attached",
            "Weekly status report"
        ]

        filter.train(spam_samples, ham_samples)
        
        spam_prob = filter.predict("Claim your free iPhone now!")
        assert spam_prob > 0.7
        
        ham_prob = filter.predict("Reminder: Team lunch tomorrow")
        assert ham_prob < 0.3

    def test_untrained_filter(self, filter):
        assert filter.predict("Test") == 0.0

    def test_model_persistence(self, filter, tmp_path):
        model_file = tmp_path / "spam_model.pkl"
        filter.train(["spam"], ["ham"])
        filter.save_model(model_file)
        
        new_filter = SpamFilter()
        new_filter.load_model(model_file)
        assert new_filter.predict("spam word") > 0.5
