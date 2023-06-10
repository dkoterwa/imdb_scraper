import datetime
import re
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

start_time = time.time()

# Set up Chrome WebDriver
driver = webdriver.Chrome()

# Open IMDb Top 250 page
driver.get('https://www.imdb.com/chart/top')

# Find movie containers
movie_containers = driver.find_elements(By.CSS_SELECTOR, '.lister-list tr')

# Create CSV file and write header
with open('imdb_top250_selenium_1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'rating', 'genre', 'date_published', 'duration'])

    # Iterate over movie containers
    for i in range(len(movie_containers)):
        print(i)
        # Re-find movie containers on each iteration
        movie_containers = driver.find_elements(By.CSS_SELECTOR, '.lister-list tr')

        # Extract information from container
        title_element = movie_containers[i].find_element(By.CSS_SELECTOR, '.titleColumn a')
        rating_element = movie_containers[i].find_element(By.CSS_SELECTOR, '.imdbRating strong')

        # Get text values
        title = title_element.text
        rating = rating_element.text

        title_element.click()

        movie_info = driver.find_elements(By.XPATH,
                                          '//h1[@data-testid="hero__pageTitle"]/following-sibling::ul//child::li')
        duration = movie_info[-1].text
        duration_split = re.split("[hm]", duration)
        if duration_split[1] == "":
            duration = (int(duration_split[0]) * 60)
        else:
            duration = (int(duration_split[0]) * 60) + int(duration_split[1])

        # Find genre elements on movie page
        driver.execute_script("window.scrollBy(0,8000);")

        elem_pulled_from_graphql = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="storyline-plot-summary"]')))

        genres = elem_pulled_from_graphql.find_elements(By.XPATH,
                                                        "//span[text()='Genre']/following-sibling::div//child::li")
        if len(genres) == 0:
            genres = elem_pulled_from_graphql.find_elements(By.XPATH,
                                                            "//span[text()='Genres']/following-sibling::div//child::li")


        date_published = \
        driver.find_elements(By.XPATH, '//div[@data-testid="title-details-section"]/child::ul/child::li/child::div')[
            0].text

        date_str = date_published
        date_str = date_str.split(" (")[0]
        date_obj = datetime.datetime.strptime(date_str, "%B %d, %Y")

        # Format the date object as "MM/DD/YYYY"
        formatted_date = date_obj.strftime("%m/%d/%Y")

        # Write data to CSV file
        writer.writerow([title, rating, genres[0].text, formatted_date, duration])

        # Go back to the top 250 page
        driver.back()
        # Wait briefly to ensure the page loads before continuing
        time.sleep(1)

# Close the WebDriver
driver.quit()

print("EXECUTION TIME %s seconds" % (np.round(time.time() - start_time, 2)))
