import pandas as pd
import os
import numpy as np
import zipfile
from bs4 import BeautifulSoup
import io

# Function to split DataFrame into smaller chunks
def split_dataframe_into_chunks(df, max_tokens=3500):
    chunks = []
    current_chunk = []
    current_chunk_token_count = 0
    
    # Function to estimate token count per row
    def estimate_token_count(row):
        row_text = " ".join(str(cell) for cell in row)
        return len(row_text) // 4  # Approximation: 4 characters per token
    
    for idx, row in df.iterrows():
        row_token_count = estimate_token_count(row)
        if current_chunk_token_count + row_token_count > max_tokens:
            chunks.append(pd.DataFrame(current_chunk, columns=df.columns))
            current_chunk = []
            current_chunk_token_count = 0
        current_chunk.append(row)
        current_chunk_token_count += row_token_count
    
    if current_chunk:
        chunks.append(pd.DataFrame(current_chunk, columns=df.columns))
    
    return chunks

def csv_converter(html):
    soup = BeautifulSoup(html, "html.parser")
    body_content = soup.body
    head_content = soup.head

    title_tag = head_content.find('title') if head_content else None
    title = title_tag.get_text(strip=True) if title_tag else "default_title"
    safe_title = "".join([c if c.isalnum() else "_" for c in title])

    data = {
        "page_title": [title],
        'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': [],
        "a": [], "navigation_menus": [], "reviews": [], "tables": [],
        "images": [], "links": [], "meta": [],
        "paragraphs": [], "articles": [], "quotes": [], "spans": []
    }

    if body_content:  # Check if body_content is not None
        for i in range(1, 7):
            data[f'h{i}'] = [h.get_text(strip=True) for h in body_content.find_all(f'h{i}')]

        # Extract additional content from HTML
        data["navigation_menus"] = [li.get_text(strip=True) for ul in body_content.find_all('ul', class_='nav') for li in ul.find_all('li')]
        data["reviews"] = [div.get_text(strip=True) for div in body_content.find_all('div', class_='review')]
        data["tables"] = [tr.get_text(strip=True) for table in body_content.find_all('table') for tr in table.find_all('tr')]
        data["images"] = [f"{img.get('src', '')}|{img.get('alt', '')}" for img in body_content.find_all('img')]
        data["links"] = [a.get('href', '') for a in body_content.find_all('a')]
        data["paragraphs"] = [p.get_text(strip=True) for p in body_content.find_all('p')]
        data["articles"] = [article.get_text(strip=True) for article in body_content.find_all('article')]
        data["quotes"] = [blockquote.get_text(strip=True) for blockquote in body_content.find_all('blockquote')]
        data["a"] = [a.get_text(strip=True) for a in body_content.find_all('a')]
        data["spans"] = [span.get_text(strip=True) for span in body_content.find_all('span')]
        
    # Pad all lists to the same length with NaN
    max_length = max(len(v) for v in data.values())
    data = {k: v + [np.nan] * (max_length - len(v)) for k, v in data.items()}

    # Create DataFrame
    df = pd.DataFrame(data)

    threshold = 0.9 * len(df)
    df.dropna(thresh=threshold, axis=1)
    df.fillna('No data', inplace=True)

    # Split DataFrame into chunks
    chunks = split_dataframe_into_chunks(df)

    return chunks, safe_title

def create_zip_from_chunks(chunks, folder_path, base_filename):
    zip_filename = os.path.join(folder_path, f"{base_filename}.zip")
    
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for i, chunk in enumerate(chunks):
            csv_buffer = io.StringIO()
            chunk.to_csv(csv_buffer, index=False, encoding='utf-8')
            zipf.writestr(f"{base_filename}_chunk_{i+1}.csv", csv_buffer.getvalue())

    return zip_filename
