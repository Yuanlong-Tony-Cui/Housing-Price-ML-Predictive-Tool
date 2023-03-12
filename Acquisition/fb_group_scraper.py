from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def fb_group_scraper(url,scrolls,html_name):

    # Start a web driver
    driver = webdriver.Chrome()

    # Load the initial page
    driver.get(url)

    # define a function to scroll down the page
    def scroll_down():
        # scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # wait for the page to load

    # define a function to click all "See More" buttons
    def click_see_more():
        # find all the "See More" buttons
        see_more_buttons = driver.find_elements(By.XPATH, "//div[contains(text(), 'See more')]")

        # click each "See More" button
        for button in see_more_buttons:
            try:
                button.send_keys(Keys.RETURN)
                time.sleep(2)
            except:
                pass

    # scroll down the page x times
    for i in range(scrolls):
        scroll_down()

    # click all "See More" buttons
    click_see_more()

    # Save the final page source
    url = driver.current_url()
    driver.get(url)
    page_source = driver.find_element_by_tag_name("body").text

    # Close the web driver
    driver.quit()

    # Write the page source to a file
    with open(html_name, "w", encoding="utf-8") as f:
        f.write(page_source)