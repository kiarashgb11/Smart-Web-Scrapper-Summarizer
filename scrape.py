import csv
import requests
from bs4 import BeautifulSoup


from bs4 import BeautifulSoup
from openai import OpenAI
client = OpenAI(api_key='OPEN AI TOKEN HERE')

# Replace 'YOUR_API_KEY_HERE' with your actual OpenAI API key

def fetch_discussion_text(url):
    print (url)
    texts = ""
    """
    Fetches the discussion text from a given GitHub discussion URL.
    This is a placeholder function. You'll need to implement the extraction
    of discussion text based on the page's structure.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Example: Extract some text from the discussion page
    discussion_text = soup.select(".comment-body")  # Update this selector based on the actual content you need
    var = discussion_text[0].select_one('p')
    while (var is not None):
        if var.name == 'p':
            texts += var.text.strip()
        elif var.name == 'div':
            if "data-snippet-clipboard-copy-content" in var:
                texts += var["data-snippet-clipboard-copy-content"]
        texts += "\n"
        var = var.find_next_sibling()
    
    #print (texts)

    return texts

def summarize_text(text):
    """
    Uses OpenAI's API to generate a summary for the given text.
    Adjust the engine to the latest version you intend to use.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with the actual latest version if different
            messages=[
                {"role": "system", "content": "You will summarize this text in less than 100 words. Just say what the overall issue is in the discussion"},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=100,  # Adjust based on desired summary length
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Summary generation failed."


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


# Initialize a list to store discussion data
discussions_data = []

for i in range(1, 41):
    # URL of the GitHub discussions page
    url = 'PUT YOUR URL HERE'+str(i)

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')


    # Find all discussion entries
    for discussion in soup.select('.Box-row--drag-hide'):
        # Extract the title, which is within an <a> tag with class 'Link--primary'
        title = discussion.select_one('.Link--primary').text.strip()
        
        link = "https://github.com" + discussion.select_one('.Link--primary')["href"] + "/body"
        
        text_summary = fetch_discussion_text(link)
        summary = summarize_text(text_summary)

        category = category_text(text_summary)

        severity = severe_text(text_summary)

        # Extract the username, which is within an <a> tag with class 'Link--secondary'
        username = discussion.select_one('.Link--muted').text.strip()
        
        # Extract the number of upvotes. This might require a more specific selector based on the page's structure.
        # Since GitHub Discussions do not directly show upvotes in the HTML like issues do, this is a placeholder.
        # In actual scraping, you'd likely need to use GitHub's API to get accurate upvote counts.
        upvotes = discussion.select_one('.Link--secondary').text.strip()

        # Append the extracted data to the list
        discussions_data.append([title, username, upvotes, summary, category, severity])

# Specify the filename
filename = 'github_discussions.csv'

# Writing to CSV
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Title', 'Username', 'Upvotes', 'Summary', 'Category', 'Severity'])
    # Write all rows of data
    for discussion in discussions_data:
        writer.writerow(discussion)

print(f'Data has been saved to {filename}')
