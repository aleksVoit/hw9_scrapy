Quotes Scraper
Overview
This project is a web scraper built using the Scrapy framework. It extracts quotes and author details 
from the Quotes to Scrape website and stores the data in both JSON files and a MongoDB database.

Features
Scrapes quotes, tags, and author information from the website.
Saves the data into JSON files (quotes.json and authors.json).
Stores quotes and author details in a MongoDB database.
Checks for duplicates before saving data to avoid redundancy.
Project Structure
bash
Copy code
├── main.py              # Entry point of the project
├── models.py            # MongoDB document models for authors and quotes
├── connect.py           # MongoDB connection setup
├── quotes.json          # JSON file to store scraped quotes
├── authors.json         # JSON file to store scraped authors
├── .env                 # Environment variables (e.g., MongoDB URI)
├── poetry.lock          # Poetry lock file for dependencies
├── pyproject.toml       # Poetry configuration file
└── README.md            # This file
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/quotes-scraper.git
cd quotes-scraper
Install dependencies:

This project uses Poetry for dependency management. Install Poetry if you haven't already:
bash
pip install poetry

Then, install the project dependencies:
bash
poetry install

Set up environment variables:
Create a .env file in the root directory and add your MongoDB connection string:
bash
MONGODB_URI=mongodb://your_mongo_uri

Usage
Run the scraper:
Start the scraper by running the main.py file:

bash
python3 main.py
The scraper will extract quotes and author information and store them in JSON files and the MongoDB database.

View the scraped data:

quotes.json: Contains all the scraped quotes with tags and authors.
authors.json: Contains details of all the authors.
Dependencies
Python 3.11
Scrapy
MongoEngine
json

Troubleshooting
Common Issues
SMTP Authentication Error: Ensure that the credentials used for email notifications are correct and that the email 
account allows less secure apps.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any questions or issues, please contact your email.
