import pandas as pd

# english_data = pd.read_csv("data/english.csv")
# print(data.columns)

# director = "priyadarshan"

# filtered_df = data.query('{} in Directors'.format(director))

# print(filtered_df)
import urllib.request
from bs4 import BeautifulSoup as bs

def scrape_reviews(imdb_id):
    sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
    soup = bs(sauce, 'lxml')
    soup_result = soup.find_all("div", {"class": "text show-more__control"})
    reviews_list = []  # list of reviews

    for reviews in soup_result:
        if reviews.string:
            review_text = reviews.string.strip()  # Remove leading/trailing spaces
            reviews_list.append(review_text)

    return reviews_list
for i in scrape_reviews('tt0214915'):
    print(i + "\n\n")