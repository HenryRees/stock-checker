# Stock Checker

## Project Overview

This project uses Selenium's web scraping tools to repeatedly check whether the item you are looking for is in stock on an online store. When the item is in stock, the programme will send you an email letting you know that the item is available for purchase and will provide a link to the website. Please note this project is intended for research purposes and shouldn't be deployed repeatedly as this is in violation of most online stores' policies. 

### Technologies used

- Selenium to scrape the web
- Chrome WebDrivers to automate interactions with your browser


## Installation

To install first clone this repository.
```bash
git clone https://github.com/HenryRees/stock-checker
cd stock-checker
```

### Requirements
* `python 3.10.6`

The code below shows how to setup a virtual environment and installs the dependencies.

    # Create a virtual environment (venv)
    make env

    # Activate the virtual environment
    source venv/bin/activate

    # Install project dependencies from requirements.txt
    make deps

## Project structure

The project has two main parts:

- Web scraping
- Email component

### Scrapping component

1. I use Selenium paired with Chrome WebDrivers to scrape the Abercrombie & Fitch website available at "https://www.abercrombie.com/shop/uk". During the scraping, I look for all "disabled_elements" which refer to the size buttons on the product page which have been disabled i.e not in stock
2. I compare the set of disabled_elements to the desired size inputted by the user

### Email component

1. If your item is in stocl, the script prepares a markdown script saying this and provides a link to the website to purchase the email
2. The markdwon script is then emailed to the user based on a user specified email
