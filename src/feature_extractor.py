import re
import socket
import whois
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tldextract
from urllib.parse import urlparse

class WebsiteFeatureExtractor:
    def __init__(self):
        self.suspicious_keywords = ['login', 'bank', 'verify', 'update', 'password', 'account', 'security', 'wallet', 'crypto', 'bonus', 'free']
        
    def get_url_features(self, url):
        features = {}
        
        # Ensure url has scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        try:
            parsed_url = urlparse(url)
            domain = tldextract.extract(url).registered_domain
            
            # URL Based Features
            features['url_length'] = len(url)
            features['dot_count'] = url.count('.')
            features['has_at_symbol'] = 1 if '@' in url else 0
            features['is_https'] = 1 if parsed_url.scheme == 'https' else 0
            
            # Check if domain is IP
            try:
                socket.inet_aton(parsed_url.netloc)
                features['is_ip'] = 1
            except:
                features['is_ip'] = 0
                
            # Domain Age Feature
            features['domain_age_days'] = self._get_domain_age(domain)
            
            # Content Based Features (Keyword density)
            features['keyword_score'] = self._get_keyword_score(url)
            
            return features
        except Exception as e:
            print(f"Error extracting features for {url}: {e}")
            return None

    def _get_domain_age(self, domain):
        try:
            w = whois.whois(domain)
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if creation_date:
                age = (datetime.now() - creation_date).days
                return age
            return 0 # Unknown age
        except:
            return 0

    def _get_keyword_score(self, url):
        try:
            response = requests.get(url, timeout=5, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            score = 0
            for word in self.suspicious_keywords:
                if word in text:
                    score += 1
            return score
        except:
            return 0

if __name__ == "__main__":
    extractor = WebsiteFeatureExtractor()
    print(extractor.get_url_features("https://google.com"))
