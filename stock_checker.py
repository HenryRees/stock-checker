import os
import argparse
import markdown
import smtplib
import time
from datetime import date
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Global variables

load_dotenv()
sender_email = os.environ["SENDER_EMAIL"]
sender_password = os.environ["SENDER_PASSWORD"]
user_agent = os.environ['USER_AGENT']

# Specify the path to the ChromeDriver executable
chrome_driver_path = os.environ['CHROME_DRIVER_PATH']

def check_stock(website_url: str, article_size: str) -> bool:

    item_inStock = False

    try:
        size = convert_size(website_url, article_size)
    except ValueError as e:
        print(f"Error: {e}")
        exit()

    # Set the path as an environment variable
    os.environ['webdriver.chrome.driver'] = chrome_driver_path

    # Create ChromeOptions and set headless mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_driver = webdriver.Chrome(options=chrome_options)

    # Specify a port (change it if needed)
    chrome_driver_port = 9515

    # Open a website
    try:
        chrome_driver.get(website_url)
    except Exception as e:
        print(f"An exception occured: {e}")
        exit()

    # Find all elements with 'disabled' attribute set to 'disabled'
    disabled_elements = chrome_driver.find_elements(By.XPATH, '//*[@disabled="disabled"]')

    if disabled_elements:
        for element in disabled_elements:
            if element.get_attribute("value") == size:
                item_inStock = False
            else:
                item_inStock = True
    
    # Close the browser
    chrome_driver.quit()

    return item_inStock

def convert_size(website_url: str, article_size: str): 

    if "abercrombie" in website_url:
        if article_size == "XS":
            return "XS_p"
        if article_size == "S":
            return "S_p"
        if article_size == "M":
            return "M_p"
        if article_size == "L":
            return "L_p"
        if article_size == "XL":
            return "XL_p"
        if article_size == "XXL":
            return "XXL"
    else:
        raise ValueError("This programme does not currently support that website") # type: ignore

def check_valid_size(article_size):

    VALID_SIZES = ("XS", "S", "M", "L", "XL", "XXL")

    if article_size not in VALID_SIZES:
        raise argparse.ArgumentTypeError(f"'{article_size}' is not a valid size. Please choose from: {', '.join(VALID_SIZES)}")
    
    return article_size

def send_email(recipient_email, website_url):
    
    subject = "Your item is in stock!!!"

    smtp_server = "smtp.gmail.com"  # Use the SMTP server of your email provider
    smtp_port = 587  # Port for Gmail is 587
    smtp_username = sender_email
    smtp_password = sender_password

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message_text = ("""# GOOD NEWS

Your item is in stock!
                                  
Click the link to purchase your item
                    
<WEBSITE_URL>""")

    message_text = message_text.replace("<WEBSITE_URL>", website_url)
    
    html_text = markdown.markdown(message_text)
    message.attach(MIMEText(html_text, "html"))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    server.sendmail(sender_email, recipient_email, message.as_string())

    server.quit()

def main(email_address: str, website_url: str, article_size: str):

    item_in_stock = check_stock(website_url, article_size)

    print(item_in_stock)

    while not item_in_stock:
        time.sleep(900)
        item_in_stock = check_stock(website_url, article_size)
        

        print(item_in_stock)
    
    send_email(email_address, website_url)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock Checker")

    parser.add_argument(
        "email_address", type=str, help="Please enter your email"
    )
    
    parser.add_argument(
        "website_url", type=str, help="Please enter the url of the item you want to check stock for"
    )
    parser.add_argument(
        "article_size", type=str, default="M", help="What size of item are you looking for"
    )
    
    args = parser.parse_args()

    main(args.email_address, args.website_url, args.article_size)