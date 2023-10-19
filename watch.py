#  Import selenium and the webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Import configuration
from os import getenv
from dotenv import load_dotenv
load_dotenv()

# URL For Refurbished Steam Deck
URL = "https://store.steampowered.com/sale/steamdeckrefurbished/"

# Set the options for the webdriver
options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1400")

# Start the webdriver
driver = webdriver.Chrome(options=options)
# Set implicit wait in order to wait for the Cart Btns to load
driver.implicitly_wait(10)
# Navigate to the URL
driver.get(URL)

# Find the divs that contain the cart buttons for each Steam Deck
cart_divs = driver.find_elements(By.CSS_SELECTOR, "div.salepurchaseonlydisplay_PurchaseOnlyCtn_4-0sk")

# Check each steam deck to see if it is available
for cart_div in cart_divs:
    div = cart_div.find_element(By.CSS_SELECTOR, "div.salepurchaseonlydisplay_Name_2K2zo")
    # if (div.text == "Steam Deck 64 GB - Valve Certified Refurbished"):
    span = cart_div.find_element(By.CSS_SELECTOR, "span")
    # If Available, Send Email
    if (span.text == "Add to Cart"):
        msg = EmailMessage()
        msg.set_content( f"{div.text} is available", subtype='plain')
        msg['Subject'] = f"{div.text} is available"
        msg['From'] = f"Steam Deck Watcher <{getenv('smpt_user')}>"
        msg['To'] = getenv('to')
        
        s = smtplib.SMTP(getenv('smtp_host'), getenv('smtp_port'))
        s.starttls()
        s.login(getenv('smpt_user'), getenv('smtp_password'))
        s.send_message(msg)
        s.quit()
        
        print(f"{div.text} is available")


# Save a screenshot of the page and quit the webdriver
driver.save_screenshot("screenshot.png")
driver.quit()
