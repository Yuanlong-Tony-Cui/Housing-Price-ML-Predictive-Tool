from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the web driver (here, we're using Chrome)
driver = webdriver.Chrome()

# Load the webpage
driver.get("https://www.facebook.com/groups/110354088989367")

# Find all the button elements with the text "See more"
buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'See more')]")

# Click on each button and wait for the page to finish loading
for button in buttons:
    # Wait for the button to be clickable
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'See more')]")))
    button.click()

    # Wait for the page to finish loading
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))

# Save the final page source
page_source = driver.page_source

# Close the web driver
driver.quit()

# Write the page source to a file
with open("Acquisition/page.html", "w", encoding="utf-8") as f:
    f.write(page_source)
