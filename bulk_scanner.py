import pandas as pd
from src.classifier import WebsiteClassifier
import argparse
import os

def bulk_scan(input_file, output_file='results.xlsx'):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # Load URLs
    with open(input_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Starting bulk scan of {len(urls)} URLs...")
    
    classifier = WebsiteClassifier()
    results = []

    for url in urls:
        print(f"Scanning: {url}")
        prediction = classifier.predict(url)
        if isinstance(prediction, dict):
            # Flatten the result for Excel
            res_row = {
                "URL": prediction['url'],
                "Classification": prediction['classification'],
                "Confidence": prediction['confidence']
            }
            # Add features to the row
            res_row.update(prediction['features'])
            results.append(res_row)
        else:
            results.append({"URL": url, "Classification": "Error", "Confidence": "0%"})

    # Export to Excel
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
    print(f"Scan complete. Results exported to {output_file}")

if __name__ == "__main__":
    # Create a dummy urls.txt if it doesn't exist
    if not os.path.exists('urls.txt'):
        with open('urls.txt', 'w') as f:
            f.write("https://google.com\n")
            f.write("http://scam-site-example.xyz\n")
            f.write("https://github.com\n")
            f.write("http://login-verify-bank.net\n")

    parser = argparse.ArgumentParser(description="Bulk Website Safety Scanner")
    parser.add_argument("--input", default="urls.txt", help="Input file with URLs (one per line)")
    parser.add_argument("--output", default="scan_results.xlsx", help="Output Excel file path")
    
    args = parser.parse_args()
    bulk_scan(args.input, args.output)
