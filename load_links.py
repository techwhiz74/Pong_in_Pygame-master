# load_links.py

import pandas as pd

def get_phishing_links(csv_file_path):
    phishing_links_df = pd.read_csv(csv_file_path)
    phishing_links = phishing_links_df['domain'].tolist()  # Assuming 'domain' column contains the links
    return phishing_links

if __name__ == "__main__":
    links = get_phishing_links('phishing_links.csv')
    for link in links:
        print(link)
