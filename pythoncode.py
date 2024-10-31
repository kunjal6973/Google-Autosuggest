import requests
import xml.etree.ElementTree as ET
import streamlit as st
import pandas as pd  # Import Pandas

# Function to extract autosuggest keywords
def extract_autosuggest_keywords(keyword, country):
    try:
        apiurl = f"http://suggestqueries.google.com/complete/search?output=toolbar&hl={country}&q={keyword}"
        r = requests.get(apiurl)
        r.raise_for_status()  # To ensure we get proper responses
        tree = ET.fromstring(r.content)
        suggestions = [child.attrib['data'] for child in tree.iter('suggestion')]
        return [suggestion for suggestion in suggestions if not any(kw in suggestion.lower() for kw in ['pinterest', 'jpg', 'png', 'svg', 'amazon', 'facebook', 'instagram', 'tiktok'])][:5]
    except requests.RequestException as e:
        st.error(f"An error occurred while fetching data for keyword '{keyword}': {str(e)}")
        return []
    except ET.ParseError as e:
        st.error(f"An error occurred while parsing the response for keyword '{keyword}': {str(e)}")
        return []

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

        if not keywords_list:
            st.warning("Please enter at least one keyword.")
            return

        # Create a list to store the results
        results = []

        # Loop through the keywords
        for keyword in keywords_list:
            suggestions = extract_autosuggest_keywords(keyword, country)
            results.append({'Keyword': keyword, 'Suggested Keywords': ', '.join(suggestions)})

        # Convert results to a DataFrame
        df = pd.DataFrame(results)

        # Display the results in a table
        st.write(df)

        # Option to download the results as CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='output.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
