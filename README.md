# Snapchat-Streak-Recovery-Automation

This project provides a basic setup for automating the Chrome browser using Selenium and ChromeDriver. The code demonstrates how to initialize ChromeDriver, navigate to a website, and perform basic actions.

## Prerequisites

- **Python 3.x:** Ensure Python is installed. Download it from [python.org](https://www.python.org/downloads/).
- **Google Chrome:** The installed Chrome version should match the version of ChromeDriver.
- **ChromeDriver:** Download the appropriate version from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/). Alternatively, use `webdriver-manager` to manage the driver automatically.

## Setup

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a Virtual Environment (Optional):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install selenium webdriver-manager
   ```

## Usage

There are two approaches to initializing ChromeDriver:

### 1. Using WebDriver Manager (Recommended)

This approach automatically handles the correct version of ChromeDriver.

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options if needed
options = webdriver.ChromeOptions()
# Uncomment the next line to run in headless mode:
# options.add_argument("--headless")

# Initialize ChromeDriver automatically
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open a website
driver.get("https://www.example.com")

# Close the browser
driver.quit()
```

### 2. Specifying the ChromeDriver Path Manually

If you prefer not to use `webdriver-manager`, specify the path directly:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Replace '/path/to/chromedriver' with the actual path to your ChromeDriver
service = Service("/path/to/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://www.example.com")
print("Page title:", driver.title)
driver.quit()
```

## Troubleshooting

- **Version Mismatch:**  
  Ensure your ChromeDriver version matches your installed Chrome version.
  
- **PATH Issues:**  
  If specifying the path manually, double-check that the provided path is correct.
  
- **Headless Mode:**  
  For environments without a GUI (e.g., CI servers), enable headless mode by uncommenting the `--headless` option.

Feel free to update this README as your project evolves. If you have any questions or need further assistance, just let me know!
``` 