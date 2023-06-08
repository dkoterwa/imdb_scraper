import pandas as pd
import numpy as np
import requests
from requests import get
from bs4 import BeautifulSoup
import re
import time
import json
import datetime
from tqdm import tqdm
from colorama import Fore


class IMDB_soup_scraper:
    def __init__(self, limit_pages_to_100=True, results_save_path=None):
        """Constructor of our class. It sets all needed parameters for our scraping operation, e.g. main link with films to scrap,
        headers to use while scraping, or the path to save our results.

        Args:
            limit_pages_to_100 (bool, optional): boolean argument to limit scraping to only 100 links. Defaults to True.
            results_save_path (string, optional): path to save our csv with results. Defaults to None.
        """
        self.main_link = "https://www.imdb.com/chart/top/?ref_=nv_mv_250&fbclid=IwAR0XgsprrxZZ0TxxHKuIG_h3VxUm_gLEiO8cSZZTf-foIxG4WdS-zjl40Gs"
        self.headers = {
            "Accept-Language": "en-US, en;q=0.5",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0",
        }
        self.results_save_path = results_save_path
        self.limit_pages_to_100 = limit_pages_to_100

    def collect_base_information(self):
        """This function scraps the website with top 250 films on IMDB, we first have to get individual keys (film_links) to be able to visit
        the website of an individual film. Additionally, we collect information about titles.

        Returns:
            film_links: a list with links of specific films
            film_titles: a list with titles of specific films
        """
        page = requests.get(self.main_link, headers=self.headers)
        soup = BeautifulSoup(page.text, "html.parser")
        film_links = []
        film_titles = []
        top_250_info = soup.find_all("a", href=re.compile(r"/title/tt\d+"))

        # Get link and title of every film on the website
        for film in top_250_info:
            if film.find("img"):
                continue  # Skip if the tag contains an <img> tag
            film_links.append(film["href"])
            film_titles.append(film.get_text())

        # Check if we collected everything needed
        assert len(film_links) == len(
            film_titles
        ), "Number of scraped links is not equal to number of scraped titles"

        print("Base info has been collected")
        self.film_titles = film_titles
        return film_links, film_titles

    def collect_main_information(self, film_links):
        """This function takes previously scraped list with links and goes inside the website of every individual film.
        There, it collects the characteristics of specific film.

        Args:
            film_links (list): a list with individual keys of films

        Returns:
            results_df: a dataframe with scraped films and information about them
        """
        # Define lists of features to collect
        ratings = []
        genres = []
        dates_published = []
        durations = []

        if self.limit_pages_to_100:
            limit = 100
        else:
            limit = len(film_links)

        # Iterate through every link and get information of specific film
        for link in tqdm(film_links[:limit]):
            url = "https://www.imdb.com" + link
            print(Fore.CYAN + "URL", url)
            page = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(page.text, "html.parser")
            script_tag = soup.find("script", type="application/ld+json")
            json_content = json.loads(script_tag.string)

            rating = json_content["aggregateRating"]["ratingValue"]  # Getting rating
            if rating is not None and rating != "":
                print(Fore.GREEN + "Rating scraped")
                ratings.append(rating)
            else:
                print(Fore.RED + "Rating not scraped")
                ratings.append(None)

            genre = json_content["genre"][0]  # Getting genre
            if genre is not None and rating != "":
                print(Fore.GREEN + "Genre scraped")
                genres.append(genre)
            else:
                print(Fore.RED + "Genre not scraped")
                genres.append(None)

            date_published = json_content["datePublished"]  # Getting date published
            if date_published is not None and rating != "":
                print(Fore.GREEN + "Date of publish scraped")
                dates_published.append(date_published)
            else:
                print(Fore.RED + "Date of publish not scraped")
                dates_published.append(None)

            duration = json_content["duration"]  # Getting duration
            # Converting the duration to normal format
            if "H" in duration and "M" in duration:
                duration_obj = datetime.datetime.strptime(duration, "PT%HH%MM")
                duration_minutes = duration_obj.hour * 60 + duration_obj.minute
            elif "H" in duration:
                duration_obj = datetime.datetime.strptime(duration, "PT%HH")
                duration_minutes = duration_obj.hour * 60
            else:
                duration_minutes = 0

            if duration_minutes is not None and duration_minutes != 0:
                print(Fore.GREEN + "Duration scraped")
                durations.append(duration_minutes)
            else:
                print(Fore.RED + "Duration not scraped")
                durations.append(None)

        # Creating dataframe with results
        results_df = pd.DataFrame(
            {
                "title": self.film_titles[:limit],
                "rating": ratings,
                "genre": genres,
                "date_published": dates_published,
                "duration": durations,
            }
        )
        # Saving results if requested
        if self.results_save_path is not None:
            results_df.to_csv(self.results_save_path + "/scraper_results.csv")
            print(Fore.WHITE + "\n" + "Results have been saved")

        print(results_df.head())
        return results_df


if __name__ == "__main__":
    start_time = time.time()
    scraper = IMDB_soup_scraper(limit_pages_to_100=True)
    film_links, film_titles = scraper.collect_base_information()
    results = scraper.collect_main_information(film_links)
    print("EXECUTION TIME %s seconds" % (np.round(time.time() - start_time, 2)))
