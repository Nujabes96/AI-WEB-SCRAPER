# 🤖 AI Web Scraper

AI Web Scraper is a web application that allows users to scrape websites, clean the content, and download the data in CSV format. The application is built using Streamlit and leverages Selenium for web scraping.

## Features

- **Web Scraping**: Enter a website URL to scrape its content.
- **Data Cleaning**: Clean the scraped HTML content to remove unnecessary tags and scripts.
- **CSV Export**: Convert the cleaned data into CSV format and download it as a zip file.
- **Session Management**: Retain scraped data across interactions using Streamlit's session state.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nujabes96/AI-WEB-SCRAPER.git
   cd AI_WEB_SCRAPER
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run main.py
   ```

## Usage

1. **Enter a Website URL**: Input the URL of the website you want to scrape.
2. **Scrape Website**: Click the "Scrape Website" button to start scraping.
3. **Preview Content**: View the cleaned DOM content in the preview section.
4. **Download CSV Chunks**: Download the scraped data as CSV chunks in a zip file.

## Project Structure

- `main.py`: The main application file that handles the Streamlit interface and user interactions.
- `scrape.py`: Contains functions for setting up the Selenium driver and scraping website content.
- `csv_saver.py`: Handles the conversion of HTML content to CSV format and zipping the CSV files.
- `requirements.txt`: Lists all the Python dependencies required for the project.

## Dependencies

- `streamlit`: For building the web application interface.
- `selenium`: For web scraping using a headless browser.
- `beautifulsoup4`: For parsing and cleaning HTML content.
- `webdriver-manager`: For managing the Selenium WebDriver.
- `lxml`, `html5lib`: For HTML parsing.
- `python-dotenv`: For managing environment variables.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.
