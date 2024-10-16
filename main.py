import streamlit as st
from scrape import scrape_website, clean_body_content
from csv_saver import csv_converter, create_zip_from_chunks
import os

st.title("🤖 AI Web Scraper")
url = st.text_input("Enter a Website URL:")

# Use Streamlit session state to retain data across interactions
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = None

if st.button("Scrape Website") and url:
    if not url.startswith('https://'):
        st.write("Not a valid website. Try again")
    else:
        result = scrape_website(url)

        if result:  # Check if result is not None or empty
            clean_body = clean_body_content(result)

            # Store the result in session state
            st.session_state.scraped_data = result

            with st.expander("Preview"):
                st.text_area("DOM Content", clean_body, height=300)

            if st.session_state.scraped_data:
                # Prepare chunks but do not save them yet
                chunks, safe_title = csv_converter(st.session_state.scraped_data)
                
                # Ensure the folder exists
                folder_path = "csv_chunks"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Create zip file from chunks
                zip_filename = create_zip_from_chunks(chunks, folder_path=folder_path, base_filename=safe_title)

                with open(zip_filename, 'rb') as f:
                    st.download_button(
                        label="Download CSV Chunks (.zip)",
                        data=f.read(),
                        file_name=os.path.basename(zip_filename),
                        mime='application/zip'
                    )
            else:
                st.write("Failed to scrape the website. Please try again.")
