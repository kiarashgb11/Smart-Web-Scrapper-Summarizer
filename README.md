# GitHub Discussion Scraper

This project is designed to scrape GitHub discussions from specified pages, analyze their content to summarize, categorize, and rate the severity of issues discussed, and finally compile this data into an Excel file. It leverages the BeautifulSoup library for web scraping, requests for fetching web content, and the OpenAI API for processing and analyzing text data.

## Features

- **Web Scraping:** Utilizes `requests` and `BeautifulSoup` to navigate and parse GitHub discussion pages.
- **Text Analysis:** Employs OpenAI's GPT-3 model to summarize discussion content, categorize the type of issue discussed, and rate the severity of the issue on a scale from 0 to 5.
- **Data Compilation:** Gathers and stores discussion data including titles, usernames, upvotes, summaries, categories, and severity ratings into a CSV file for easy analysis and review.

## Setup

1. **Prerequisites:**
   - Python 3.x installed on your system.
   - Install required Python packages: `beautifulsoup4`, `requests`, and `openai`.
     ```
     pip install beautifulsoup4 requests openai
     ```
   - An API key from OpenAI. You'll need to replace `'YOUR_API_KEY_HERE'` with your actual OpenAI API key in the script.

2. **Installation:**
   - Clone this repository or download the script to your local machine.
   - Ensure you have the prerequisites installed.
   - Replace the placeholder API key with your actual OpenAI API key.

## Usage

Execute the script with Python from your terminal:


The script will automatically scrape GitHub discussions, analyze the text, and save the results to a file named `github_discussions.csv` in the same directory as the script.

## Output

The output CSV file will contain the following columns:

- `Title`: The title of the GitHub discussion.
- `Username`: The GitHub username of the discussion author.
- `Upvotes`: The number of upvotes the discussion received. (Note: Actual upvote data extraction may require GitHub's API.)
- `Summary`: A summary of the discussion content, generated by OpenAI's GPT-3 model.
- `Category`: The category of the issue discussed, as determined by OpenAI's GPT-3 model.
- `Severity`: The severity of the issue discussed, rated on a scale from 0 to 5 by OpenAI's GPT-3 model.

## Note

This script is intended for educational and research purposes. Please respect GitHub's `robots.txt` and terms of service when scraping their site. Additionally, be mindful of OpenAI's API usage limits and costs when using their services for text analysis.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](#) for open issues or to open a new issue.

## License

Distributed under the MIT License. See `LICENSE` for more information.
