from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup the Selenium Chrome Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open the webpage
    driver.get('https://subway.com.my/find-a-subway')

    # Wait for the search box to be available and input 'Kuala Lumpur'
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'fp_searchAddress'))
    )
    search_box.send_keys('Kuala Lumpur')

    # Find the search button and click it
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'fp_searchAddressBtn'))
    )
    search_button.click()

    # Wait for the search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'fp_listitem'))
    )

    outlets = driver.find_elements(By.CLASS_NAME, 'fp_listitem')

    # Iterate over each outlet
    for outlet in outlets:
        # Attempt to find the shop name and check if it is not empty
        name_element = outlet.find_elements(By.TAG_NAME, 'h4')
        if name_element and name_element[0].text.strip():
            name = name_element[0].text.strip()
        else:
            # If the name element is not found or is empty, skip this outlet
            continue

        # Extract all <p> elements inside the infoboxcontent and then filter out empty ones
        info_text_elements = outlet.find_elements(By.CSS_SELECTOR, '.infoboxcontent > p')
        info_texts = [elem.text.strip() for elem in info_text_elements if elem.text.strip() != '']

        # Check if it have multiple <p> elements and concatenate them as needed
        operating_hours = ' '.join(info_texts[1:])  # Skip the first element as it is assumed to be the address

        # Extract geographical coordinates of each outlet
        latitude = outlet.get_attribute('data-latitude')
        longitude = outlet.get_attribute('data-longitude')

        # Attempt to find the Waze link
        waze_link_elements = outlet.find_elements(By.CSS_SELECTOR, '.location_right a')
        waze_link = waze_link_elements[1].get_attribute('href') if len(
            waze_link_elements) > 1 else "Waze link not found"

        # Output the information
        print(f'Name: {name}')
        print(f'Address: {info_texts[0]}' if info_texts else "Address not found")
        print(f'Latitude: {latitude}')
        print(f'Longitude: {longitude}')
        print(f'Operating Hours: {operating_hours}')
        if waze_link:
            print(f'Waze Link: {waze_link}')
        print('---')

except Exception as e:
    print(f'An error occurred: {e}')
finally:
    # Close the browser regardless of what happens
    driver.quit()
