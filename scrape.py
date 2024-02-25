import csv  # Import CSV library for handling CSV file operations.
import requests  # Import requests library for making HTTP requests.
from bs4 import BeautifulSoup  # Import BeautifulSoup from bs4 for parsing HTML content.

from openai import OpenAI  # Import OpenAI from the openai library to interact with the OpenAI API.
client = OpenAI(api_key='API TOKEN HERE')  # Initialize the OpenAI client with your API key.

def fetch_discussion_text(url):
    print(url)  # Print the URL being processed for debugging purposes.
    texts = ""  # Initialize an empty string to accumulate discussion texts.
    response = requests.get(url)  # Make an HTTP GET request to the specified URL.
        #response has severeal attributes the .text containts the HTML content tjem tje html.parser just parses through it
    soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content of the response.
    discussion_text = soup.select(".comment-body")  # Select elements with the class "comment-body".
    var = discussion_text[0].select_one('p')  # Select the first paragraph within the first ".comment-body".
    while (var is not None):  # Loop through siblings of the paragraph as long as there are elements.
        if var.name == 'p':  # Check if the current element is a paragraph.
            texts += var.text.strip()  # Add the text of the paragraph to the accumulating string.
        elif var.name == 'div':  # Check if the current element is a div.
            if "data-snippet-clipboard-copy-content" in var:  # Check if the div has the specific attribute.
                texts += var["data-snippet-clipboard-copy-content"]  # Add the content of the attribute to the string.
        texts += "\n"  # Add a newline after each element's text.
        var = var.find_next_sibling()  # Move to the next sibling element.
    return texts  # Return the accumulated text.

def summarize_text(text):
    try:
        response = client.chat.completions.create(
            #chat.completions: This refers to a specific type of API call within the OpenAI API that is designed for generating chat-like interactions. and the .create gets a response from the model
            model="gpt-3.5-turbo",  # Specify the model to use for the completion.
            messages=[
                {"role": "system", "content": "You will summarize this text in less than 100 words. Just say what the overall issue is in the discussion"},
                {"role": "user", "content": text}
            ],  # Set up the conversation context for summarization.
            temperature=0.3,  # Set the creativity level of the response.
            max_tokens=100,  # Limit the maximum length of the generated summary.
        )
        summary = response.choices[0].message.content  # Extract the summary content from the response.
        return summary  # Return the generated summary.
    except Exception as e:
        print(f"An error occurred: {e}")  # Print any errors that occur.
        return "Summary generation failed."  # Return a default error message.
    

def category_text(text):
    """
    Uses OpenAI's API to generate a summary for the given text.
    Adjust the engine to the latest version you intend to use.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with the actual latest version if different
            messages=[
                {"role": "system", "content": """You will identify the categroy each discussion belongs to. Discussions have issued diffeerent problems and you need to choose which issue the disccusions belong to. These issues are either Finetuning issues,
                 syntax errors, Handling files, speed issues, Integration, or lastly subtitile issues. Just state the name of the category, no need to say "category": ..."""},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=5,  # Adjust based on desired summary length
        )
        summary = response.choices[0].message.content
        print (summary)
        return summary
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Summary generation failed."
    

def severe_text(text):
    """
    Uses OpenAI's API to generate a summary for the given text.
    Adjust the engine to the latest version you intend to use.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with the actual latest version if different
            messages=[
                {"role": "system", "content": """you have to rate the severity  of the the issue in each discussion. I want you to rate the severity
                 of the issue discussed at each section with a numerical number from 0-5. 0 is considered being an issue that is more like quality of life problem, and 5 being an issue such as the program is not feasible (e.g. not fast enought)
                 or it just crashes, meaning it is a severe issue. Make sure the severity that you list is ONLY a numerical number rangning from 0-5. I DONT WANT AN ANSWER LONGER THAN A SINGLE DIGIT NUMBER. Just state the number of the severity, no need to say "severity": ... """},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=50,  # Adjust based on desired summary length
        )
        summary = response.choices[0].message.content
        print (summary)
        return summary
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Summary generation failed."
    


discussions_data = []  # Initialize an empty list to store discussion data.

for i in range(1, 41):  # Loop through pages 1 to 40.
    url = 'LINK HERE'+str(i)  # Construct the URL for the current page.
    response = requests.get(url)  # Make an HTTP GET request to the URL.
        #response has severeal attributes the .text containts the HTML content then the html.parser just parses through it
    soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content of the response.

    for discussion in soup.select('.Box-row--drag-hide'):  # Select each discussion entry.
            #The argument to .select(), '.Box-row--drag-hide', is a CSS selector that matches elements with the class Box-row--drag-hide
        title = discussion.select_one('.Link--primary').text.strip()  # Extract the discussion title. Again it slects anything on the css class .link--primary which i found out was the title
        link = "https://github.com" + discussion.select_one('.Link--primary')["href"] + "/body"  # Construct the link to the discussion body.
        text_summary = fetch_discussion_text(link)  # Fetch the discussion text.
        summary = summarize_text(text_summary)  # Summarize the discussion text.
        category = category_text(text_summary)  # Categorize the discussion content.
        severity = severe_text(text_summary)  # Assess the severity of the discussed issue.
        username = discussion.select_one('.Link--muted').text.strip()  # Extract the username of the discussion author.
        upvotes = discussion.select_one('.Link--secondary').text.strip()  # Placeholder for upvotes; requires API or correct parsing to fetch actual values.
        discussions_data.append([title, username, upvotes, summary, category, severity])  # Append the collected data to the list.


# Specify the filename where the scraped data will be saved.
filename = 'github_discussions.csv'

# Opening a file with the specified filename for writing. 
# The 'w' mode indicates that the file will be written to, and if it exists, it will be overwritten.
# 'newline' parameter is set to '' to ensure that newlines are handled according to the standards of the CSV format.
# 'encoding' is set to 'utf-8' to support a wide range of characters (including non-ASCII characters).
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    # Create a csv.writer object for writing to the CSV file.
    # This object will be used to write data rows into the file.
    writer = csv.writer(file)
    
    # Write the header row to the CSV file. 
    # This row contains the column names, defining the structure of the dataset.
    writer.writerow(['Title', 'Username', 'Upvotes', 'Summary', 'Category', 'Severity'])
    
    # Iterate over each discussion data item stored in the discussions_data list.
    # Each 'discussion' variable represents a single github discussion's data as a list.
    for discussion in discussions_data:
        # Write the current discussion's data as a row in the CSV file.
        # This includes all the collected information: title, username, upvotes, summary, category, and severity.
        writer.writerow(discussion)

# Print a confirmation message indicating that the data has been successfully saved to the specified filename.
# This helps in verifying that the script has completed its execution and the data is stored.
print(f'Data has been saved to {filename}')
