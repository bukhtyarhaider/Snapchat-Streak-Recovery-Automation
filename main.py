import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# -------------------------------
# Configuration
# -------------------------------
# Your static form details (update these as needed)
MY_USERNAME = "your_username"
MY_EMAIL = "your_email@example.com"
MY_MOBILE = "1234567890"

# URL for the streak recovery form
URL = "https://help.snapchat.com/hc/en-us/requests/new?co=true&ticket_form_id=149423"

# XPaths for form fields
USERNAME_XPATH = "//*[@id='request_custom_fields_24281229']"
EMAIL_XPATH = "//*[@id='request_custom_fields_24335325']"
MOBILE_XPATH = "//*[@id='request_custom_fields_24369716']"
FRIEND_USERNAME_XPATH = "//*[@id='request_custom_fields_24369736']"
SUBMIT_BUTTON_XPATH = "//*[@id='new_request']/footer/input"

# -------------------------------
# Read Friend List
# -------------------------------
# Ensure you have a file named "friends.xlsx" with a column "friend_username"
friend_df = pd.read_excel("friends.xlsx")

# This list will store the outcome for each friend submission
results = []

# -------------------------------
# Setup ChromeDriver with Selenium
# -------------------------------
options = webdriver.ChromeOptions()
# Uncomment the line below to run in headless mode if desired
# options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# -------------------------------
# Process Each Friend
# -------------------------------
for index, row in friend_df.iterrows():
    friend_username = row["friend_username"]
    status = "Failed"  # Default status
    
    try:
        # Load the recovery form page
        driver.get(URL)
        time.sleep(2)  # wait for the page to fully load
        
        # Fill in the Username field
        username_field = driver.find_element(By.XPATH, USERNAME_XPATH)
        username_field.clear()
        username_field.send_keys(MY_USERNAME)
        
        # Fill in the Email field
        email_field = driver.find_element(By.XPATH, EMAIL_XPATH)
        email_field.clear()
        email_field.send_keys(MY_EMAIL)
        
        # Fill in the Mobile Number field
        mobile_field = driver.find_element(By.XPATH, MOBILE_XPATH)
        mobile_field.clear()
        mobile_field.send_keys(MY_MOBILE)
        
        # Fill in the Friend's Username field with the current friend
        friend_username_field = driver.find_element(By.XPATH, FRIEND_USERNAME_XPATH)
        friend_username_field.clear()
        friend_username_field.send_keys(friend_username)
        
        # Submit the form
        submit_button = driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH)
        submit_button.click()
        
        # Allow some time for the submission to process (adjust if needed)
        time.sleep(3)
        
        # Optionally, add logic to verify if submission was successful.
        # For now, if no exception is raised, we'll consider it successful.
        status = "Success"
    except Exception as e:
        print(f"Error processing friend '{friend_username}': {e}")
        status = "Failed"
    
    # Record the result
    results.append({"friend_username": friend_username, "status": status})

# Close the browser once done
driver.quit()

# -------------------------------
# Save the Results
# -------------------------------
results_df = pd.DataFrame(results)
results_df.to_excel("results.xlsx", index=False)
print("Process completed. Results saved to results.xlsx")
