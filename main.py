import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("AI total")

def writer_check(driver, text):
    try:
        driver.get("https://writer.com/ai-content-detector/")

        textarea = driver.find_element(By.TAG_NAME, "textarea")
        percentage = driver.find_element(By.ID, "ai-percentage")
        button = driver.find_element(By.CLASS_NAME, "dc-btn-gradient")

        textarea.send_keys(text)
        button.send_keys(Keys.END) # scroll to end of page
        button.click()

        while percentage.text == "":
            time.sleep(0.5)

        result = 100 - int(round(float(percentage.text)))
        return eval_result(result)
    except:
        return "Error encountered"
    
def cas_check(driver, text):
    try:
        driver.get("https://contentatscale.ai/ai-content-detector/")

        textarea = driver.find_element(By.TAG_NAME, "textarea")
        button = driver.find_element(By.CLASS_NAME, "check-ai-score")
        percentage = driver.find_element(By.ID, "progress")

        textarea.send_keys(text)
        button.send_keys(Keys.END)
        button.click()

        while percentage.text == "N/A":
            time.sleep(0.5)
        
        result = int(percentage.text[:-1])
        return eval_result(result)
    except:
        return "Error encountered"

def zerogpt_check(driver, text):
    try:
        driver.get("https://www.zerogpt.com/")

        textarea = driver.find_element(By.TAG_NAME, "textarea")
        button = driver.find_element(By.CLASS_NAME, "scoreButton")

        textarea.send_keys(text)
        button.send_keys(Keys.END)
        button.click()

        wait = WebDriverWait(driver, 10) # specifies waiting amount
        percentage = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".percentage-div span"))) # waits until element is present

        result = int(round(float(percentage.text.split("%", 1)[0])))
        return eval_result(result)
    except:
        return "Error encountered"

def crossplag_check(driver, text):
    try:
        driver.get("https://crossplag.com/ai-content-detector/")

        textarea = driver.find_element(By.TAG_NAME, "textarea")
        button = driver.find_element(By.ID, "checkButtonAIGen")
        description = driver.find_element(By.CLASS_NAME, "description")
        percentage = driver.find_element(By.CSS_SELECTOR, ".pointer span")

        textarea.send_keys(text)
        button.send_keys(Keys.END)
        button.click()

        while description.text == "Please provide some text for detection.":
            time.sleep(0.5)

        result = int(percentage.text[:-1])
        return eval_result(result)
    except:
        return "Error encountered"

def sapling_check(driver, text):
    try:
        text_list = text.split()
        if len(text_list) < 50:
            return "Not enough words"

        driver.get("https://sapling.ai/ai-content-detector")

        textarea = driver.find_element(By.TAG_NAME, "textarea")
        percentage = driver.find_element(By.ID, "fake-prob")

        textarea.clear()
        textarea.send_keys(text)
        time.sleep(5)
        
        result = int(round(float(percentage.text)))
        return eval_result(result)
    except:
        return "Error encountered"
    
def eval_result(result):
    
    if result >= 0 and result < 25:
        return "Very unlikely"
    elif result >= 25 and result < 50:
        return "Unlikely"
    elif result >= 50 and result < 75:
        return "Likely"
    elif result >= 75 and result <= 100:
        return "Very likely"

def check():

    chrome_options = Options()
    chrome_options.add_argument("--headless") # browser runs in the background
    chrome_options.add_argument("--log-level=3") # disables logging to the console
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = Service(ChromeDriverManager().install()) # installs ChromeDriver binary (connects api and browser)
    driver = webdriver.Chrome(service=service, options=chrome_options) # creates instance of Chrome browser

    print("Enter text to be checked for AI-plagiarism")
    print("For more accurate results, enter more words")
    text = input()

    writer_result = writer_check(driver, text)
    print(f"https://writer.com/ai-content-detector/ \t: {writer_result}")

    cas_result = cas_check(driver, text)
    print(f"https://contentatscale.ai/ai-content-detector/ \t: {cas_result}")

    zerogpt_result = zerogpt_check(driver, text)
    print(f"https://www.zerogpt.com/ \t\t\t: {zerogpt_result}")

    crossplag_result = crossplag_check(driver, text)
    print(f"https://crossplag.com/ai-content-detector/ \t: {crossplag_result}")

    sapling_result = sapling_check(driver, text)
    print(f"https://sapling.ai/ai-content-detector \t\t: {sapling_result}")

    print("Do you want to check something else? (y/n)")
    answer = input().lower()

    while answer != "y" and answer != "n":
        print("I didn't get that, please repeat (y/n)")
        answer = input().lower()

    if answer == "y":
        driver.quit()
        check()
    elif answer == "n":
        print("Thank you for using AI total")
        driver.quit()

check()