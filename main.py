import secrets
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import time

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Flask-SocketIO Imports
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app, async_mode='eventlet')

# Files and column names
FRIENDS_FILE = 'friends.xlsx'
FRIENDS_COLUMN = 'friend_username'
FRIEND_IMAGE_COLUMN = 'friend_image'

# Streak recovery form details (constants)
FORM_URL = "https://help.snapchat.com/hc/en-us/requests/new?co=true&ticket_form_id=149423"
USERNAME_XPATH = "//*[@id='request_custom_fields_24281229']"
EMAIL_XPATH = "//*[@id='request_custom_fields_24335325']"
MOBILE_XPATH = "//*[@id='request_custom_fields_24369716']"
FRIEND_USERNAME_XPATH = "//*[@id='request_custom_fields_24369736']"
SUBMIT_BUTTON_XPATH = "//*[@id='new_request']/footer/input"

# Global variables
# friend_list holds all friends as dictionaries: {"friend_username": ..., "friend_image": ...}
friend_list = []
# selected_friends holds a subset of friend_list that the user chooses for recovery.
selected_friends = []
user_details = {
    "MY_USERNAME": "",
    "MY_EMAIL": "",
    "MY_MOBILE": ""
}

def load_friends():
    if os.path.exists(FRIENDS_FILE):
        df = pd.read_excel(FRIENDS_FILE)
        if FRIENDS_COLUMN in df.columns:
            if FRIEND_IMAGE_COLUMN not in df.columns:
                df[FRIEND_IMAGE_COLUMN] = ""
            return df[[FRIENDS_COLUMN, FRIEND_IMAGE_COLUMN]].to_dict('records')
        else:
            return []
    else:
        return []

def save_friends(friends):
    df = pd.DataFrame(friends)
    df.to_excel(FRIENDS_FILE, index=False)

def background_execute_streak_recovery(selected):
    results = []
    total = len(selected)
    if total == 0:
        socketio.emit('progress_update', {
            'progress': 0,
            'log': "No selected friends for recovery."
        }, namespace='/execute')
        return results

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    for idx, friend in enumerate(selected):
        progress = int((idx / total) * 100)
        socketio.emit('progress_update', {
            'progress': progress,
            'log': f"Processing {friend['friend_username']} ({idx+1}/{total})"
        }, namespace='/execute')
        status = "Failed"
        try:
            driver.get(FORM_URL)
            time.sleep(2)
            driver.find_element(By.XPATH, USERNAME_XPATH).clear()
            driver.find_element(By.XPATH, USERNAME_XPATH).send_keys(user_details['MY_USERNAME'])
            driver.find_element(By.XPATH, EMAIL_XPATH).clear()
            driver.find_element(By.XPATH, EMAIL_XPATH).send_keys(user_details['MY_EMAIL'])
            driver.find_element(By.XPATH, MOBILE_XPATH).clear()
            driver.find_element(By.XPATH, MOBILE_XPATH).send_keys(user_details['MY_MOBILE'])
            driver.find_element(By.XPATH, FRIEND_USERNAME_XPATH).clear()
            driver.find_element(By.XPATH, FRIEND_USERNAME_XPATH).send_keys(friend['friend_username'])
            driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH).click()
            time.sleep(3)
            status = "Success"
            socketio.emit('progress_update', {
                'progress': progress,
                'log': f"Successfully processed {friend['friend_username']}"
            }, namespace='/execute')
        except Exception as e:
            socketio.emit('progress_update', {
                'progress': progress,
                'log': f"Error processing {friend['friend_username']}: {e}"
            }, namespace='/execute')
        results.append({"friend_username": friend['friend_username'], "status": status})
    driver.quit()
    socketio.emit('progress_update', {
        'progress': 100,
        'log': "Execution complete.",
        'final_results': results
    }, namespace='/execute')
    return results

# Load friend list on startup.
friend_list = load_friends()

@app.route('/')
def index():
    return render_template('index.html', friends=friend_list, user_details=user_details, selected=selected_friends)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global user_details
    if request.method == 'POST':
        user_details['MY_USERNAME'] = request.form.get('my_username')
        user_details['MY_EMAIL'] = request.form.get('my_email')
        user_details['MY_MOBILE'] = request.form.get('my_mobile')
        return redirect(url_for('profile'))
    return render_template('profile.html', user_details=user_details)

@app.route('/friends', methods=['GET', 'POST'])
def friends_page():
    global friend_list, selected_friends
    if request.method == 'POST':
        # Manual addition form.
        if request.form.get('friend_username'):
            new_friend = request.form.get('friend_username')
            friend_image = request.form.get('friend_image') or ""
            if new_friend:
                friend_list.append({"friend_username": new_friend, "friend_image": friend_image})
                save_friends(friend_list)
        # CSV file upload.
        if 'csv_file' in request.files:
            csv_file = request.files['csv_file']
            if csv_file:
                try:
                    df = pd.read_csv(csv_file)
                    if 'friend_username' in df.columns:
                        if 'friend_image' not in df.columns:
                            df['friend_image'] = ""
                        new_friends = df[['friend_username', 'friend_image']].to_dict('records')
                        friend_list.extend(new_friends)
                        # Remove duplicates by friend_username.
                        unique = {}
                        for f in friend_list:
                            unique[f['friend_username']] = f
                        friend_list = list(unique.values())
                        save_friends(friend_list)
                except Exception as e:
                    print("Error reading CSV file:", e)
        return redirect(url_for('friends_page'))
    return render_template('friends.html', friends=friend_list, selected=selected_friends)

@app.route('/remove_friend', methods=['POST'])
def remove_friend():
    global friend_list, selected_friends
    friend_username = request.form.get('friend_username')
    friend_list = [f for f in friend_list if f['friend_username'] != friend_username]
    # Also remove from selected list if present.
    selected_friends = [f for f in selected_friends if f['friend_username'] != friend_username]
    save_friends(friend_list)
    return redirect(url_for('friends_page'))

@app.route('/remove_all_friends', methods=['POST'])
def remove_all_friends():
    global friend_list, selected_friends
    friend_list = []
    selected_friends = []
    save_friends(friend_list)
    return redirect(url_for('friends_page'))

# New routes for selecting and deselecting friends.
@app.route('/select_friend', methods=['POST'])
def select_friend():
    global friend_list, selected_friends
    friend_username = request.form.get('friend_username')
    # Find friend in friend_list
    friend = next((f for f in friend_list if f['friend_username'] == friend_username), None)
    if friend and friend not in selected_friends:
        selected_friends.append(friend)
    return redirect(url_for('friends_page'))

@app.route('/deselect_friend', methods=['POST'])
def deselect_friend():
    global selected_friends
    friend_username = request.form.get('friend_username')
    selected_friends = [f for f in selected_friends if f['friend_username'] != friend_username]
    return redirect(url_for('friends_page'))

@app.route('/clear_selected_friends', methods=['POST'])
def clear_selected_friends():
    global selected_friends
    selected_friends = []
    return redirect(url_for('friends_page'))

@app.route('/execute', methods=['GET'])
def execute_page():
    return render_template("execute.html")

@socketio.on('start_execution', namespace='/execute')
def handle_start_execution():
    # Use selected_friends for recovery.
    socketio.start_background_task(target=background_execute_streak_recovery, selected=selected_friends)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
