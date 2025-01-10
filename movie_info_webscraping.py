from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
headers = {
    "User-Agent": "Chrome",
    "Accept-Language": "en-US",
}
response = requests.get(url, headers=headers)


def main():
    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')

        movies_block = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 iyTDQy compact-list-view ipc-metadata-list--base')
        movie_title_list = movies_block.findAll('h3', class_='ipc-title__text')
        movie_trailer_list = movies_block.findAll(class_='ipc-lockup-overlay ipc-focusable')
        movie_rating_list = movies_block.findAll(class_='ipc-rating-star--rating')
        movie_vote_list = movies_block.findAll(class_='ipc-rating-star--voteCount')
        movie_year_and_duration = movies_block.findAll(class_='sc-300a8231-7 eaXxft cli-title-metadata-item')
        movie_year_list = [] 
        movie_duration_list = []
        for i in movie_year_and_duration:
            if len(i.text) == 4:            
                movie_year_list.append(i)
            elif len(i.text) > 4 and ('h' and 'm' in i.text):
                movie_duration_list.append(i)

        display_results(movie_title_list, movie_trailer_list, movie_rating_list, movie_year_list, movie_vote_list, movie_duration_list)
        save_to_excel(movie_title_list)
    else:
        print("Connection Error")



def display_results(movie_title_list, movie_trailer_list, movie_rating_list, movie_year_list, movie_vote_list, movie_duration_list):
    print(f"\n")
    i = 1
    for (title, trailer, rating, year, vote, duration) in zip(movie_title_list, movie_trailer_list, movie_rating_list, movie_year_list, movie_vote_list, movie_duration_list):
        print(f"{i}) Title: {title.text[4:]}\n    Rating: {rating.text}\n    Votes: {vote.text}\n    Release Year: {year.text}\n    Duration: {duration.text}\n    Trailer: https://www.imdb.com{trailer.get('href')}\n-----------------------------------------------")
        i += 1


#This module is not working completely
#AS it is saving to excel but in HTML format like; <h3 class=".....">First Movie</h3>
def save_to_excel(title_list):
    df = pd.DataFrame({'Title': title_list})
    with pd.ExcelWriter('movie_data.xlsx') as writer:
        df.to_excel(writer, sheet_name='movie_data', index=False)

main()