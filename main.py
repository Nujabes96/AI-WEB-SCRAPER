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
            st.subheader("🐱‍💻 Steps for AI analysis")
            st.write("1. Donwload the zip file below and extract the files\n 3. Provide each chunk-file to a LLM such as ChatGPT or Claude\n 4. Write a prompt according to your needs. Here's an example you can use:")
            st.code("""You will receive multiple CSV chunks. Please process each chunk to extract relevant insights. The data may include:
- **Columns**: page_title, h1, h2, h3, h4, h5, h6, a, navigation_menus, reviews, tables, images, meta, links, paragraphs, articles, quotes and spans.
Determine the title of all the news on the website and combine it with the upcoming chunks to create a cohesive list. Here's the first chunk. Let me know when you're ready for the next chunk.""","markdown")
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
