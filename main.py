from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import time

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Files and column name
FRIENDS_FILE = 'friends.xlsx'
FRIENDS_COLUMN = 'friend_username'

# Streak recovery form details (constant)
FORM_URL = "https://help.snapchat.com/hc/en-us/requests/new?co=true&ticket_form_id=149423"
USERNAME_XPATH = "//*[@id='request_custom_fields_24281229']"
EMAIL_XPATH = "//*[@id='request_custom_fields_24335325']"
MOBILE_XPATH = "//*[@id='request_custom_fields_24369716']"
FRIEND_USERNAME_XPATH = "//*[@id='request_custom_fields_24369736']"
SUBMIT_BUTTON_XPATH = "//*[@id='new_request']/footer/input"

# Global variables to store friend list and user details.
friend_list = []
user_details = {
    "MY_USERNAME": "",
    "MY_EMAIL": "",
    "MY_MOBILE": ""
}

def load_friends():
    """Load the friend list from an Excel file."""
    if os.path.exists(FRIENDS_FILE):
        df = pd.read_excel(FRIENDS_FILE)
        return df[FRIENDS_COLUMN].tolist() if FRIENDS_COLUMN in df.columns else []
    else:
        return []

def save_friends(friends):
    """Save the friend list to an Excel file."""
    df = pd.DataFrame({FRIENDS_COLUMN: friends})
    df.to_excel(FRIENDS_FILE, index=False)

def execute_streak_recovery(friends):
    """Execute the streak recovery automation for each friend using user-supplied details."""
    results = []

    # Setup ChromeDriver
    options = webdriver.ChromeOptions()
    # Uncomment the next line to run headless:
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for friend in friends:
        status = "Failed"
        try:
            driver.get(FORM_URL)
            time.sleep(2)  # wait for the page to load

            # Fill in the form using user_details and current friend
            driver.find_element(By.XPATH, USERNAME_XPATH).clear()
            driver.find_element(By.XPATH, USERNAME_XPATH).send_keys(user_details['MY_USERNAME'])

            driver.find_element(By.XPATH, EMAIL_XPATH).clear()
            driver.find_element(By.XPATH, EMAIL_XPATH).send_keys(user_details['MY_EMAIL'])

            driver.find_element(By.XPATH, MOBILE_XPATH).clear()
            driver.find_element(By.XPATH, MOBILE_XPATH).send_keys(user_details['MY_MOBILE'])

            driver.find_element(By.XPATH, FRIEND_USERNAME_XPATH).clear()
            driver.find_element(By.XPATH, FRIEND_USERNAME_XPATH).send_keys(friend)

            # Submit the form
            driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH).click()
            time.sleep(3)  # wait for submission to process

            status = "Success"
        except Exception as e:
            print(f"Error processing friend '{friend}': {e}")
            status = "Failed"
        results.append({"friend_username": friend, "status": status})

    driver.quit()

    # Save results to an Excel file
    results_df = pd.DataFrame(results)
    results_df.to_excel("results.xlsx", index=False)
    return results

# Load friend list on startup
friend_list = load_friends()

@app.route('/', methods=['GET', 'POST'])
def index():
    global friend_list, user_details
    if request.method == 'POST':
        # Distinguish between friend addition and user details update via a hidden input field.
        action = request.form.get('action')
        if action == 'add_friend':
            new_friend = request.form.get('friend_username')
            if new_friend:
                friend_list.append(new_friend)
                save_friends(friend_list)
        elif action == 'update_settings':
            # Update the user details with the submitted values
            user_details['MY_USERNAME'] = request.form.get('my_username')
            user_details['MY_EMAIL'] = request.form.get('my_email')
            user_details['MY_MOBILE'] = request.form.get('my_mobile')
        return redirect(url_for('index'))
    return render_template('index.html', friends=friend_list, user_details=user_details)

@app.route('/execute', methods=['POST'])
def execute():
    # Execute streak recovery automation for the current friend list using the latest user details.
    results = execute_streak_recovery(friend_list)
    return render_template("execute.html", results=results)

if __name__ == '__main__':
    app.run(debug=True)
