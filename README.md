AI Website Safety Classifier - Project Documentation
1. Project Overview
The AI Website Safety Classifier is a Python-based security tool designed to analyze and categorize website URLs into three risk levels: Safe, Suspicious, or Scam. It utilizes Machine Learning (Random Forest) and multi-dimensional feature extraction to provide real-time security assessments.

2. Key Features
AI-Powered Analysis: Uses a Random Forest classifier to detect patterns common in phishing and scam sites.
Multi-Source Feature Extraction:
Network Features: HTTPS status, domain length, and IP-based URLs.
Domain Intelligence: Automatic WHOIS lookup to determine domain age (newer domains are often riskier).
Content Scanning: Scans page HTML for high-risk keywords (e.g., "bank recovery", "crypto bonus").
Interactive Dashboard: A premium Streamlit UI for individual URL testing.
Batch Automation: A bulk scanning script that processes URL lists and exports findings to Excel.
3. System Architecture
Modular Code Structure
src/feature_extractor.py: The "brain" of the system that gathers data from the URL and the live website.
src/model_trainer.py: Handles data preprocessing, model training, and evaluation.
src/classifier.py: The interface for making predictions using the trained model.
app.py: The web interface layer.
bulk_scanner.py: The automation layer for enterprise-scale scanning.
4. Feature Set Details
The model makes decisions based on the following extracted features:

Feature	Description	Why it matters
URL Length	Total characters in the URL	Scams often use very long, obfuscated URLs.
Dot Count	Number of dots in the domain	Excessive subdomains are a common phishing tactic.
HTTPS Status	Whether the site uses SSL	Most safe sites use HTTPS; many scams do not.
Domain Age	Days since domain registration	New domains (under 30 days) are statistically more likely to be scams.
Keyword Score	Frequency of "urgent" or "financial" words	Scam sites use social engineering keywords to lure victims.
Is IP Address	If the URL is an IP instead of a name	Legitimate businesses rarely use raw IP addresses for public sites.
5. Usage Guide
Installation
Ensure you have Python installed, then install dependencies:

bash
pip install -r requirements.txt
Running the Interactive UI
Open your terminal.
Navigate to the project folder.
Run:
bash
streamlit run app.py
Running Bulk Scans
To scan a list of URLs from a file:

Create a urls.txt with one URL per line.
Run:
bash
python bulk_scanner.py --input urls.txt --output results.xlsx
6. Technical Specifications
Language: Python 3.10+
Machine Learning: Scikit-learn (Random Forest Classifier)
UI Framework: Streamlit
Data Handling: Pandas, OpenPyXL
Web Scraping: BeautifulSoup4, Requests
Domain Tools: Python-Whois, Tldextract
7. Storage Location
Project files are stored at: C:\Users\Admin\.gemini\antigravity\scratch\website-classifier
