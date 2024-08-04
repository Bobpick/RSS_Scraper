import feedparser
import requests
import os
import sqlite3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import subprocess
from dateutil import parser
from datetime import datetime, timedelta, timezone
import pytz


# Function to clean HTML from text
def clean_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


# Define the file path for the second Python program
second_program_path = 'C:/Users/Bob/Documents/Intelligence/people_job.py'
file_path = 'C:/Users/Bob/Documents/Intelligence/article_links.html'

# Check if the file exists
if os.path.exists(file_path):
    # Delete the file if it exists
    os.remove(file_path)
    print(f"Existing file '{file_path}' deleted.")


def purge_duplicates():
    try:
        # Execute SQL query to delete duplicate entries based on the link column
        c.execute('''DELETE FROM articles WHERE rowid NOT IN (
                         SELECT MIN(rowid) FROM articles GROUP BY link)''')
        conn.commit()  # Commit changes
        print("Duplicates purged successfully.")
    except Exception as e:
        print(f"Error purging duplicates: {e}")


# Function to check if any alert word is present in the text
def check_alert_words(text):
    for word in alert_words:
        if word in text:
            return True
    return False


# List of RSS feed URLs
rss_urls = ['https://www.marinecorpstimes.com/arc/outboundfeeds/rss/category/news/',
            'https://www.geopolitical.report/latest/rss/',
            'https://feeds.stripes.com/apps/front_page.xml',
            'https://www.navytimes.com/arc/outboundfeeds/rss/category/news/?outputType=xml',
            'https://www.armytimes.com/m/rss/',
            'https://moxie.foxnews.com/google-publisher/latest.xml',
            'https://moxie.foxnews.com/google-publisher/us.xml',
            'https://moxie.foxnews.com/google-publisher/world.xml',
            'https://www.allsides.com/news/rss',    
            'https://www.nationalguard.mil/News/RSS-Feeds/',
            'https://rss.app/feed/tBZvKlhOBXX2dSPs',
            'https://rss.app/feeds/5noD9wrJOL1ZQd9M.xml',
            'https://rss.app/feeds/t6WP4fPXvVmutigr.xml',
            'https://rss.app/feeds/ixu33LeurwAMfEp6.xml',
            'https://www.pacom.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=639&max=100']

# List of Atom feed URLs
atom_urls = ['https://www.ntd.com/ntd-news-today/feed']

# Alert words dictionary
alert_words = {

    "bombing": true,
    "destroyed": true,
    "catastrophe": true,
    "devastation": true,
    "crisis": true,
    "emergency": true,
    "tragedy": true,
    "disaster": true,
    "casualties": true,
    "evacuation": true,
    "hazard": true,
    "antifa": true,
    "emergency response": true,
    "emergency services": true,
    "threat": true,
    "hazardous": true,
    "hazardous material": true,
    "evacuated": true,
    "shelter-in-place": true,
    "lockdown": true,
    "danger": true,
    "emergency preparedness": true,
    "rescue": true,
    "relief efforts": true,
    "humanitarian aid": true,
    "emergency management": true,
    "evacuation order": true,
    "state of emergency": true,
    "emergency evacuation": true,
    "collapsed": true,
    "collapse": true,
    "declared a disaster": true,
    "warnings": true,
    "emergency procedures": true,
    "emergency situation": true,
    "crisis management": true,
    "crisis response": true,
    "fatalities": true,
    "injured": true,
    "extensive damage": true,
    "widespread destruction": true,
    "trauma": true,
    "catastrophic event": true,
    "natural disaster": true,
    "man-made disaster": true,
    "calamity": true,
    "mass casualties": true,
    "search and rescue": true,
    "emergency shelter": true,
    "survival": true,
    "emergency supplies": true,
    "accident": true,
    "pandemic": true,
    "epidemic": true,
    "outbreak": true,
    "quarantine": true,
    "containment": true,
    "mass shooting": true,
    "active shooter": true,
    "terror attack": true,
    "terrorist incident": true,
    "hostage situation": true,
    "civil unrest": true,
    "riot": true,
    "looting": true,
    "martial law": true,
    "curfew": true,
    "cyber attack": true,
    "data breach": true,
    "infrastructure failure": true,
    "power outage": true,
    "nuclear incident": true,
    "radiation leak": true,
    "chemical spill": true,
    "toxic release": true,
    "wildfire": true,
    "earthquake": true,
    "tsunami": true,
    "hurricane": true,
    "tornado": true,
    "flood": true,
    "landslide": true,
    "avalanche": true,
    "volcanic eruption": true,
    "famine": true,
    "drought": true,
    "mass migration": true,
    "refugee crisis": true,
    "economic collapse": true,
    "bridge collapse": true,
    "water contamination": true,
    "transportation accident": true,
    "biohazard": true,
    "isolation": true,
    "public health crisis": true,
    "medical emergency": true,
    "blizzard": true,
    "heatwave": true,
    "financial crisis": true,
    "plane crash": true,
    "building fire": true,
    "explosion": true,
    "gas leak": true,
    "hazardous waste": true,
    "toxic exposure": true,
    "environmental disaster": true,
    "oil spill": true,
    "pipeline rupture": true,
    "chemical explosion": true,
    "industrial accident": true,
    "water shortage": true,
    "food shortage": true,
    "security breach": true,
    "terrorism": true,
    "bomb threat": true,
    "hostage crisis": true,
    "military conflict": true,
    "war": true,
    "armed conflict": true,
    "ethnic violence": true,
    "genocide": true,
    "bio-terrorism": true,
    "chemical attack": true,
    "biological threat": true,
    "radiological incident": true,
    "pandemic threat": true,
    "social unrest": true,
    "mass protest": true,
    "emergency hotline": true,
    "first responders": true,
    "crisis hotline": true,
    "relief operations": true,
    "humanitarian crisis": true,
    "public safety": true
}


# Function to parse dates with multiple formats
def parse_date(date_str):
    try:
        # Use dateutil.parser to parse the date string
        parsed_date = parser.parse(date_str)

        # If the parsed date doesn't have timezone info, assume it's UTC
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=pytz.UTC)
        else:
            # Convert to UTC if it's not already
            parsed_date = parsed_date.astimezone(pytz.UTC)

        return parsed_date
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date_str}. Error: {str(e)}")

# Function to process each article
def process_article(entry):
    title_html = ''  # Initialize title_html outside of the try block

    pubDate = entry.get('published', '')
    if not pubDate:
        print(f"Error processing link: {entry.link}. No published date found.")
        return

    try:
        pub_date_obj = parse_date(pubDate)  # Parse the date string as UTC
    except ValueError as e:
        print(f"Error processing link: {entry.link}. {e}")
        return

    link = entry.link

    description = entry.get('description', '')
    publisher = entry.get('dc_publisher', '')
    categoryTitle = entry.get('categoryTitle', '')
    title = entry.title

    try:
        response = requests.get(link)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx status codes)

        full_content = response.text
        text = clean_html(full_content)

        # Check if any alert word is present in the text
        if check_alert_words(text):
            print(f"Alert: '{title}'")

            # Create a new SQLite connection and cursor inside the function
            conn = sqlite3.connect('C:/users/bob/documents/intelligence/newsarticles.db')
            c = conn.cursor()

            # Check if the article was published in the last 24 hours
            yesterday = datetime.now(pytz.utc) - timedelta(days=1)
            if pub_date_obj > yesterday:
                print(f"Today's article: '{title}'")

                # Generate HTML hyperlink for the title
                title_html += f'<a href="{link}" target="_blank">{title}</a></p>\n'

                # Insert article data into the database
                c.execute('''INSERT OR IGNORE INTO articles (pubDate, link, description, publisher, categoryTitle, title, body)
                             VALUES (?, ?, ?, ?, ?, ?, ?)''',
                          (pub_date_obj.strftime('%a, %d %b %Y %H:%M:%S %Z'), link, description, publisher,
                           categoryTitle, title, text))

                # Write the HTML hyperlink to a text file
                with open('C:/Users/Bob/Documents/Intelligence/article_links.html', 'a') as file:
                    file.write(title_html)

                conn.commit()  # Commit changes immediately after inserting the article

                # Close the SQLite connection after processing the article
                conn.close()

    except Exception as e:
        print(f"Error processing link: {link}. Error: {e}")


processed_links = set()
# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/Bob/Documents/Intelligence/newsarticles.db')
c = conn.cursor()

# Get the current date in the format used in the pubDate attribute (e.g., 'Mon, 11 Apr 2024 12:00:00 GMT')
today_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z')

# Iterate over RSS URLs
for rss_url in rss_urls:
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        process_article(entry)

# Iterate over Atom URLs
for atom_url in atom_urls:
    feed = feedparser.parse(atom_url)
    for entry in feed.entries:
        process_article(entry)

# Call the function to purge duplicates
purge_duplicates()

# Close the database connection
conn.close()

# Run the second Python program
subprocess.run(['python', second_program_path])
