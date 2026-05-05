import joblib
import pandas as pd
from src.feature_extractor import WebsiteFeatureExtractor

class WebsiteClassifier:
    def __init__(self, model_path='models/rf_model.pkl'):
        self.model_path = model_path
        self.extractor = WebsiteFeatureExtractor()
        self.model = None
        self.classes = {0: "Safe", 1: "Suspicious", 2: "Scam"}
        
        try:
            self.model = joblib.load(self.model_path)
        except Exception as e:
            print(f"Error loading model: {e}. Please train the model first.")

    def predict(self, url):
        if not self.model:
            return "Model not loaded"
            
        features = self.extractor.get_url_features(url)
        if not features:
            return "Error extracting features"
            
        # Convert features to DataFrame for model
        features_df = pd.DataFrame([features])
        
        prediction = self.model.predict(features_df)[0]
        confidence = max(self.model.predict_proba(features_df)[0])
        
        return {
            "url": url,
            "classification": self.classes[prediction],
            "confidence": f"{confidence:.2%}",
            "features": features
        }

if __name__ == "__main__":
    classifier = WebsiteClassifier()
    # Test prediction
    result = classifier.predict("https://google.com")
    print(result)
