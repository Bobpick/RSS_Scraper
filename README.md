# RSS and Atom Feed Scraper

This Python program scrapes articles from RSS and Atom feeds, checks for alert words in the content, and stores relevant articles in a SQLite database. Additionally, it generates an HTML file containing hyperlinks to the scraped articles.

## Installation

To use this program, ensure you have Python installed on your system. You'll also need to install the following dependencies:

- [feedparser](https://pypi.org/project/feedparser/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

You can install these dependencies via pip:

```bash
pip install feedparser
pip install beautifulsoup4
```

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Bobpick/RSS_scraper.git
```

2. Navigate to the directory containing the `rss.py` file.

3. Run the program:

```bash
python rss.py
```

## Description

- The program imports necessary libraries and defines utility functions for HTML cleaning, duplicate purging, and alert word checking.
- It specifies the paths to the second Python program and the file for storing article links.
- The program scrapes articles from specified RSS and Atom feed URLs, processes each article, and stores relevant information in a SQLite database.
- Duplicate entries based on the article link are purged from the database.
- Hyperlinks to relevant articles are appended to an HTML file for easy access.
- Finally, the second Python program is executed.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the Mozilla License. See the [LICENSE](LICENSE) file for details.