import requests
import string
import xml.etree.ElementTree as ET
import streamlit as st
import csv
import pandas as pd  # Import Pandas once

# Function to extract autosuggest keywords
def extract_autosuggest_keywords(keyword, country):
    apiurl = f"http://suggestqueries.google.com/complete/search?output=toolbar&hl={country}&q={keyword}"
    r = requests.get(apiurl)
    tree = ET.fromstring(r.text)
    suggestions = [child.attrib['data'] for child in tree.iter('suggestion')]
    return [suggestion for suggestion in suggestions if not any(keyword in suggestion.lower() for keyword in ['pinterest', 'jpg', 'png', 'svg', 'amazon', 'facebook', 'instagram', 'tiktok'])][:5]

# Streamlit app
def main():
    st.title("Google Autosuggest Keyword Extractor")
    st.markdown(
        """
        <p style="font-style: italic;">
            Created by <a href="https://www.linkedin.com/in/kunjal-chawhan/" target="_blank">Kunjal Chawhan</a> |
            <a href="https://www.decodedigitalmarket.com" target="_blank">More Apps & Scripts on my Website</a>
        </p>
        """,
        unsafe_allow_html=True
    )

    # Text input for keywords
    keywords_input = st.text_area("Paste your list of keywords here (one keyword per line)")

    # Country selection
    country = st.selectbox("Select country for autosuggestions", ["de", "us", "uk", "in", "es"])  # Add more countries as needed

    # Button to extract keywords
    if st.button("Get Results"):
        keywords_list = [line.strip() for line in keywords_input.split('\n') if line.strip()]
        
        # Create a CSV file to store the results
        with open('output.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Keyword', 'Suggested Keywords'])
            
            # Loop through the keywords
            for keyword in keywords_list:
                suggestions = extract_autosuggest_keywords(keyword, country)
                writer.writerow([keyword, ', '.join(suggestions)])

        st.success("Extraction completed. Results saved in output.csv")

        # Display the results in a table
        df = pd.read_csv('output.csv')
        st.write(df)

if __name__ == "__main__":
    main()
