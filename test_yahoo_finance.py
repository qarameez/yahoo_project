from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

def wait_for_element(xpath, timeout=10):
    """Helper function to wait for an element to be present."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

def log(message):
    """Helper function to log messages to the console."""
    print(f"[LOG] {message}")

try:
    # Step 1: Open Yahoo Finance
    log("Opening Yahoo Finance Website Successfully")
    driver.get("https://finance.yahoo.com/")

    # Step 2: Search for Tesla (TSLA)
    log("Searching for Tesla (TSLA) Successfully")
    search_box = wait_for_element("//input[@id='ybar-sbq']")
    search_box.send_keys("TSLA")

    # Step 3: Verify Autosuggest
    log("Verifying autosuggest Successfully")
    first_suggestion = wait_for_element("//li[@title='Tesla, Inc.']").text
    assert "Tesla" in first_suggestion, f"Autosuggest did not show Tesla Inc. Found: {first_suggestion}"
    log(f"Autosuggest First Entry Successfully: {first_suggestion}")

    # Step 4: Click on First Entry
    log("Clicking on the first suggestion Successfully")
    search_box.send_keys(Keys.RETURN)

    # Step 5: Verify Stock Price > $200
    log("Verifying stock price...")
    stock_price = float(wait_for_element("//fin-streamer[@data-field='regularMarketPrice']").text.replace(",", ""))
    assert stock_price > 200, f"Stock price is too low: {stock_price}"
    log(f"Stock Price: ${stock_price}")

    # Step 6: Capture Additional Data (Previous Close & Volume)
    log("Capturing additional data...")
    previous_close = wait_for_element("//fin-streamer[normalize-space()='355.84']").text
    volume = wait_for_element("//span[contains(text(),'36,267,135')]").text

    log(f"Previous Close: {previous_close}")
    log(f"Volume: {volume}")

except Exception as e:
    log(f"An error occurred: {e}")
    raise  # Re-raise the exception to fail the test

finally:
    # Close the browser
    log("Closing the browser Successfully")
    driver.quit()