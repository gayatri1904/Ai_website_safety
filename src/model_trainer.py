import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os
from src.feature_extractor import WebsiteFeatureExtractor

class ModelTrainer:
    def __init__(self, model_path='models/rf_model.pkl'):
        self.model_path = model_path
        self.extractor = WebsiteFeatureExtractor()
        if not os.path.exists('models'):
            os.makedirs('models')

    def generate_synthetic_data(self):
        """Generates a small synthetic dataset for demonstration purposes."""
        data = [
            # Safe URLs (Class 0)
            ("https://www.google.com", 0),
            ("https://www.github.com", 0),
            ("https://www.microsoft.com", 0),
            ("https://www.wikipedia.org", 0),
            ("https://www.amazon.com", 0),
            # Suspicious URLs (Class 1) - e.g. no HTTPS, many dots, recent
            ("http://secure-login-update.com", 1),
            ("http://verify-account-info.net", 1),
            ("http://192.168.1.100/login", 1),
            ("http://bit.ly/random-short-link", 1),
            ("http://paypal-security-check.xyz", 1),
            # Scam URLs (Class 2) - e.g. keywords like 'crypto bonus', 'free'
            ("http://free-crypto-giveaway.biz", 2),
            ("https://get-rich-quick-now.info", 2),
            ("http://official-bank-recovery-bonus.com", 2),
            ("https://winner-of-lottery-claim.cc", 2),
            ("http://urgent-account-recovery-scam.net", 2)
        ]
        
        features_list = []
        labels = []
        
        print("Extracting features for training data...")
        for url, label in data:
            feats = self.extractor.get_url_features(url)
            if feats:
                features_list.append(feats)
                labels.append(label)
        
        df = pd.DataFrame(features_list)
        df['label'] = labels
        return df

    def train(self, data_df=None):
        if data_df is None:
            data_df = self.generate_synthetic_data()
            
        X = data_df.drop('label', axis=1)
        y = data_df['label']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        print("Training complete. Evaluation:")
        print(classification_report(y_test, y_pred))
        
        joblib.dump(model, self.model_path)
        print(f"Model saved to {self.model_path}")
        return model

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train()
