import ssl
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Ensure SSL module is available
ssl._create_default_https_context = ssl._create_unverified_context

# Router login details
ROUTER_IP = "http://192.168.1.1"
USERNAME = "admin"
PASSWORD = "admin1334"

# Function to get the current public IP
def get_public_ip():
    try:
        return requests.get("http://ifconfig.me").text.strip()
    except Exception as e:
        return f"Error fetching IP: {e}"

# Get IP before changing it
old_ip = get_public_ip()
print(f"Current IP: {old_ip}")

# WebDriver options
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")  # Bypass SSL warnings
options.add_argument("--headless=new")  # Headless mode
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--window-size=1920x1080")  # Set default window size

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)  # Set explicit wait

try:
    # Open Router Page
    driver.get(ROUTER_IP)
    
    # Login to the Router
    wait.until(EC.presence_of_element_located((By.ID, "txt_Username"))).send_keys(USERNAME)
    wait.until(EC.presence_of_element_located((By.ID, "txt_Password"))).send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.ID, "loginbutton"))).click()
    
    # Navigate to "Advanced" settings
    wait.until(EC.element_to_be_clickable((By.ID, "name_addconfig"))).click()
    
    # Switch to menu frame
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "menuIframe")))
    
    # Select WAN configuration row
    wait.until(EC.element_to_be_clickable((By.ID, "wanInstTable_record_6"))).click()
    
    # Scroll down to "Enable LCP Detection"
    driver.execute_script("window.scrollBy(0, 500);")
    
    # Toggle "Enable LCP Detection" checkbox
    wait.until(EC.element_to_be_clickable((By.ID, "LcpEchoReqCheck"))).click()
    
    # Save settings
    wait.until(EC.element_to_be_clickable((By.ID, "ButtonApply"))).click()
    
    print("IP change request sent to router. Waiting for new IP...")
except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()

# Wait for the router to apply the change and reconnect
time.sleep(10)

# Get IP after change
new_ip = get_public_ip()
print(f"New IP: {new_ip}")

if old_ip == new_ip:
    print("IP did not change. Try manually restarting the router.")
else:
    print("IP successfully changed!")
    
time.sleep(15)  # Allow time before exit instead of using input()
