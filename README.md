# SnapCovery

## Demo
<div style="display: flex;">
    <img width="500" alt="Dashboard Screenshot" src="https://github.com/user-attachments/assets/a496f1c6-441d-48fa-a459-523f7dbe9250" />
    <img width="500" alt="Execution Screenshot" src="https://github.com/user-attachments/assets/44b2b378-ff2f-4e7e-a02e-711c24484bb8" />
</div>

## Overview
SnapCovery is a web-based dashboard for automating Snapchat streak recovery. It leverages Selenium for browser automation, Flask for the web interface, and Excel files for persistent storage. In this updated version, you can not only manage your friend list and update your profile details, but you also have the new ability to select a subset of friends for recovery, and view real-time execution logs via Socket.IO. CSV uploads now support friend images, and a dual list interface lets you move friends between "All Friends" and "Selected Friends" for targeted recovery.

## Features
- **User Details Management:**  
  Update your Snapchat username, email, and mobile number through the dashboard. These details are used to populate the recovery form automatically.

- **Friend List Management:**  
  - **Add Friends Manually:** Enter friend usernames with an optional image URL.  
  - **CSV Import:** Upload a CSV file that includes columns for `friend_username` and an optional `friend_image`.  
  - **Remove Options:** Remove individual friends or clear the entire friend list.

- **Selected Friends for Recovery:**  
  Choose a subset of friends from your list to be included in the streak recovery process. The dashboard displays two separate lists – one for all friends and one for the selected ones. Recovery will only run on the selected friends.

- **Real-Time Streak Recovery Execution:**  
  Execute the automation process via Selenium. Real-time progress and log updates are provided through Socket.IO, and a detailed report is displayed on the execution results page.

- **Web Dashboard:**  
  A modern, mobile-first interface built using Flask and Tailwind CSS, featuring a fixed navigation bar, gradient headers, and clear call-to-action buttons.

## Project Structure
```
SnapCovery/
├── main.py              # Main Flask application with all routes, Socket.IO integration, and automation logic
├── friends.xlsx         # Excel file for storing friend data (username and image URL)
├── results.xlsx         # Excel file for storing execution results
├── .gitignore           
└── templates/
    ├── index.html       # Home/Dashboard (user details, friend summary, execute recovery, and Snapchat Web link)
    ├── profile.html     # Profile management page
    ├── friends.html     # Friends management page with dual lists (all and selected friends), manual add, CSV import, and remove options
    └── execute.html     # Execution results page with real-time progress and logs
```

## Prerequisites
- Python 3.6+
- Google Chrome for Selenium automation
- ChromeDriver that matches your installed version of Chrome (or use `webdriver-manager` for automatic management)
- Required Python packages: Flask, pandas, openpyxl, selenium, webdriver-manager, flask-socketio, eventlet

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/bukhtyarhaider/SnapCovery.git
   cd SnapCovery
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install flask pandas openpyxl selenium webdriver-manager flask-socketio eventlet
   ```

## Configuration
- **User Details:**  
  Update your Snapchat username, email, and mobile number through the dashboard. These details are used to fill out the recovery form automatically.
  
- **Friend List:**  
  Add friend usernames manually (with an optional image URL) or import them from a CSV file (with columns `friend_username` and optionally `friend_image`).  
  The friends are stored in `friends.xlsx`.

- **Selected Friends:**  
  Use the dual list interface on the friends page to mark which friends should be included in the recovery process. The recovery automation will only process the selected friends.

- **Selenium Setup:**  
  The automation process uses Selenium with ChromeDriver. The `webdriver-manager` package automatically installs the correct version of ChromeDriver.

- **Real-Time Updates:**  
  Socket.IO is used to provide real-time execution progress and logs on the execute page.

## Running the Application
1. Start the Flask server:
   ```bash
   python main.py
   ```
2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage
1. **Update User Details:**  
   Go to the "Profile" page, update your Snapchat credentials (username, email, mobile), and click "Update Profile."

2. **Manage Friend List:**  
   - **Manual Add:** Use the form on the "Friends" page to add individual friends with an optional image URL.
   - **CSV Import:** Upload a CSV file with columns `friend_username` and optionally `friend_image`.
   - **Dual List Interface:**  
     - **All Friends:** View all added friends with options to remove or select them.
     - **Selected Friends:** View friends selected for recovery. Use the "Remove" button to deselect or "Clear Selected" to empty the list.
   - **Remove Options:** Remove individual friends or click "Remove All Friends" to clear the entire list.

3. **Execute Streak Recovery:**  
   Go to the "Execute" page and click "Execute Streak Recovery." The system will:
   - Loop through the selected friends.
   - Open the Snapchat recovery form.
   - Fill in your details and the selected friend’s username.
   - Submit the form and log the results in real time.
   - Display a detailed report on the status (Success/Failed) for each selected friend.

4. **Review Results:**  
   After execution, view the real-time progress and log updates on the "Execute" page, along with a detailed report and summary saved in `results.xlsx`.

## Troubleshooting
- **Selenium/ChromeDriver Issues:**  
  Ensure that ChromeDriver is up-to-date and compatible with your installed version of Google Chrome. The `webdriver-manager` helps manage this automatically.
  
- **Excel File Errors:**  
  Install `openpyxl` (if not already installed) to handle Excel file operations with pandas.
  
- **Real-Time Execution:**  
  If you encounter issues with Socket.IO, verify that `eventlet` is installed and that `eventlet.monkey_patch()` is called at the very beginning of your `main.py`.

## Future Enhancements
- Further improve the UI/UX for a smoother user experience.
- Add more detailed logging and error reporting.
- Explore additional integrations with Snapchat APIs or widgets if available.

## License
This project is licensed under the [MIT License](LICENSE).

---

This README now reflects all the updates and new features introduced in v2 of SnapCovery. Enjoy automating your Snapchat streak recovery with enhanced control and real-time feedback!