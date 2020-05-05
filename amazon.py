from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import smtplib, ssl
import sys
import getpass

print(f"Email: {sys.argv[1]}")
password = getpass.getpass()
email(sys.argv[1], password)

url = "https://primenow.amazon.com/signin"
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)

# Two minutes to login into Amazon Account
# Will probably encounter lots of CAPTCHA tests
browser.get(url)
time.sleep(120)
def find_slot():
    while True:
        browser.get("https://primenow.amazon.com/checkout/enter-checkout")
        potential_buttons = browser.find_elements_by_class_name("a-row.a-spacing-top-base")
        button = [x for x in potential_buttons if "Proceed" in x.text]
        button[0].click()
        time.sleep(3)
        two_hour = browser.find_elements_by_css_selector("#two-hour-window > div")
        one_hour = browser.find_elements_by_css_selector("#one-hour-window > div")
        for item in [two_hour + one_hour]:
            if "Unavailable" not in item.text:
                email()
                return True
        # Slow down while loop
        time.sleep(5)

def email(sender, password):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = sender
    receiver = sender
    message = "\
    AMAZON ALERT: SLOTS AVAILABLE" + "\n" + "This automated program found some 2-hour delivery slots. Please check to see if they are still available."
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    
    return True

find_slot()
