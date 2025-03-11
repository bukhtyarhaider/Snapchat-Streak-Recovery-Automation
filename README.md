# Snapchat-Streak-Recovery-Automation

## Overview
This project provides a web-based dashboard to automate the Snapchat streak recovery process. It uses Selenium for browser automation, Flask for the web interface, and Excel files to store the friend list and execution results. Users can update their own contact details (username, email, mobile), manage a list of friend usernames, and trigger the streak recovery process with a single click.

## Features
- **User Details Management:**  
  Update your Snapchat username, email, and mobile number directly via the dashboard. These details are used to populate the recovery form.
- **Friend List Management:**  
  Add and view friend usernames for which the streak recovery should be executed. The list is stored persistently in an Excel file (`friends.xlsx`).
- **Streak Recovery Execution:**  
  Execute the Selenium-based automation to submit the recovery form for each friend. Results (success or failure) are recorded in `results.xlsx` and displayed on a dedicated results page.
- **Web Dashboard:**  
  A user-friendly web interface built using Flask to manage all aspects of the automation process.

## Project Structure
```
Snapchat-Streak-Recovery-Automation/
├── main.py              # Main Flask application
├── friends.xlsx         # Excel file for storing friend usernames
├── results.xlsx         # Excel file for storing automation results
├── .gitignore           
└── templates/
    ├── index.html       # Dashboard (user details, friend list, execute button)
    └── execute.html     # Execution results page
```

## Prerequisites
- Python 3.6+
- Google Chrome (for Selenium automation)
- ChromeDriver that matches your installed version of Chrome, or use `webdriver-manager` for automatic management.

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/bukhtyarhaider/Snapchat-Streak-Recovery-Automation.git
   cd Snapchat-Streak-Recovery-Automation
   ```

2. **Create a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install flask pandas openpyxl selenium webdriver-manager
   ```

## Configuration
- **User Details:**  
  Update your Snapchat username, email, and mobile number from the dashboard. These details are used when submitting the recovery form.
  
- **Friend List:**  
  Add friend usernames using the provided form. These are stored in `friends.xlsx`.
  
- **Selenium Setup:**  
  The automation uses Selenium with ChromeDriver. `webdriver-manager` ensures the correct version of ChromeDriver is used.

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
   Enter your username, email, and mobile number in the "User Details" section and click the "Update User Details" button.
   
2. **Manage Friend List:**  
   Add friend usernames via the "Add Friend Username for Streak Recovery" form. The current friend list is displayed below the form.
   
3. **Execute Streak Recovery:**  
   Click the "Execute Streak Recovery" button to run the automation. The system will:
   - Loop through the friend list.
   - Open the Snapchat recovery form.
   - Fill in your details and each friend's username.
   - Submit the form.
   - Record the result (Success/Failed) for each submission.
   
4. **Review Results:**  
   After execution, a results page will display the status for each friend, and a detailed log will be saved in `results.xlsx`.

## Troubleshooting
- **Selenium/ChromeDriver Issues:**  
  Ensure that ChromeDriver is up-to-date and matches your installed version of Google Chrome. Use `webdriver-manager` to simplify this process.
  
- **Excel File Errors:**  
  Verify that you have installed the `openpyxl` package, which is required for Excel file operations with pandas.
  
- **Performance:**  
  For longer friend lists, the automation process might take some time. Consider running Chrome in headless mode (uncomment the headless option in `app.py`) for faster execution.

## Future Enhancements
- Enhance the user interface for better usability.
- Implement additional error handling and logging for a more robust automation process.

## License
This project is licensed under the [MIT License](LICENSE).

---

This README provides all the necessary details to get started with the Snapchat Streak Recovery Automation Dashboard. Enjoy automating your streak recovery!
