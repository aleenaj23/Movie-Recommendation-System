from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import pickle
import bs4 as bs
import urllib.request
import datetime
import numpy as np
from scipy.sparse import csr_matrix



app = Flask(__name__)

filename = 'nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('tranform.pkl','rb'))
ml_poster = pd.read_csv('data/2024_s.csv')
en_poster = pd.read_csv('data/2024_e.csv')

movie_data = pd.read_csv("data/final.csv")

english_data = pd.read_csv('data/english.csv')

filter_data = pd.read_csv('data/filter_data.csv')

actor  = pd.read_csv('data/get_actor.csv')

recommend_movie_poster = []

current_language = []

def create_similarity():
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(english_data['tag'])
    similarity = cosine_similarity(count_matrix)
    return similarity


similarity = pickle.load(open('data/similarity.pkl','rb'))

def get_poster(id):
    url = "https://api.themoviedb.org/3/find/{}?api_key=64f14bfc62f718d2cf962fe150e5bc40&external_source=imdb_id".format(id)

    response = requests.get(url)
    result = response.json()
    result = result['movie_results'][0]
    poster = 'https://image.tmdb.org/t/p/original' + result['poster_path']
    return poster


def rcmd(m):
    recommend_movie_poster.clear()
    m = m.lower()
    movie_data['Title'] = movie_data['Title'].str.lower()
    if m not in movie_data['Title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = movie_data.loc[movie_data['Title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11] # excluding first item since it is the requested movie itself
        movies = {}
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(movie_data['Title'][a])
            recommend_movie_poster.append(movie_data['Poster_url'][a])
            movies[i] = {"imdb_id" : movie_data['imdb_id'][a], "Title" : movie_data['Title'][a]}
        return movies 
        
def rcmd_e(m):
    recommend_movie_poster.clear()
    m = m.lower()
    similarity_e = create_similarity()
    data = english_data
    data['Title'] = data['Title'].str.lower()
    if m not in data['Title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['Title']==m].index[0]
        lst = list(enumerate(similarity_e[i]))
        lst = sorted(lst, key = lambda x:x[1], reverse = True)
        lst = lst[1:11]
        movies = {}
        for i in range(len(lst)):
            a = lst[i][0]
            recommend_movie_poster.append(get_poster(data['Const'][a]))
            movies[i] = {'imdb_id': data['Const'][a], "Title": data['Title'][a]}
        return movies

def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["','')
    my_list[-1] = my_list[-1].replace('"]','')
    return my_list


@app.route('/')
def home():
    return render_template("lot.html")


@app.route('/index')
def index():
  posters = {}
  if current_language[0] == 'malayalam':
      for i in range(6):
          posters[ml_poster['Title'][i]] = ml_poster['poster'][i]
  else:
      for i in range(6):
          posters[en_poster['Title'][i]] = en_poster['poster'][i]
  return render_template("index.html", posters = posters)



#######################
@app.route('/loadlang')
def lang():
	return render_template('lang.html')



@app.route('/preference')
def preference():
  language = request.args.get('lang')
  current_language.clear()
  current_language.append(language)
  posters = {}
  if current_language[0] == 'malayalam':
      for i in range(6):
          posters[ml_poster['Title'][i]] = ml_poster['poster'][i]
  else:
      for i in range(6):
          posters[en_poster['Title'][i]] = en_poster['poster'][i]
  return render_template("index.html", posters = posters)

  #return render_template('preference.html', language=language)


######################
  
with open('new_json.json') as f:
    data = json.load(f)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    print(current_language[0])
    query = request.args.get('query')
    results = []
    if current_language[0] == "malayalam":
        for movie in data['data']:
            if query.lower() in movie['Title'].lower():
                results.append(movie['Title'])
            if len(results) >= 5:
                break
    elif current_language[0] == "english":
        for title in english_data['Title']:
            if query.lower() in title.lower():
                results.append(title)
            if len(results) >= 5:
                break 
    return jsonify(results)



@app.route('/findmalayalam', methods = ['POST', 'GET'])
def findmalayalam():
    title = request.form['title']
    if current_language[0] == "malayalam":
        movie_data['Title'] = movie_data['Title'].str.lower()
        movie = movie_data[movie_data['Title'] == title]
        id = movie.imdb_id
        id = list(id)
    else:
        english_data['Title'] = english_data['Title'].str.lower()
        movie = english_data[english_data['Title'] == title]
        id = movie.Const
        id = list(id)
    
    
    url = "https://api.themoviedb.org/3/find/{}?api_key=64f14bfc62f718d2cf962fe150e5bc40&external_source=imdb_id".format(id[0])

    response = requests.get(url)
    result = response.json()
        
    return jsonify(result)

    """Implement: on receiving the title go through the final.csv to find the imdb id of the movie and return the id to js file"""
    # data = json.loads(request.get_data("data"))
    # movies_list = data['movies_list']

    # # movies_list = data.get('movies_list')  # Extract the movies_list
    # for movie in movies_list:
    #     if movie['original_language'] == 'ml':
    #         selected_movie = movie
    #         return jsonify(selected_movie)




@app.route("/similarity_movie",methods=["POST"])
def similarity_movie():
    movie = request.form['name']
    if current_language[0] == "malayalam":
        rc = rcmd(movie)
    else: 
        rc = rcmd_e(movie)
    if type(rc)==type('string'):
        return rc
    else:
        return jsonify(rc)

@app.route("/recommend",methods=["POST"])
def recommend():
    # getting data from AJAX request
    title = request.form['title']
    orginal_title = request.form['orginal_title']
    cast_ids = request.form['cast_ids']
    cast_names = request.form['cast_names']
    cast_chars = request.form['cast_chars']
    cast_bdays = request.form['cast_bdays']
    cast_bios = request.form['cast_bios']
    cast_places = request.form['cast_places']
    cast_profiles = request.form['cast_profiles']
    imdb_id = request.form['imdb_id']
    poster = request.form['poster']
    genres = request.form['genres']
    overview = request.form['overview']
    vote_average = request.form['rating']
    vote_count = request.form['vote_count']
    release_date = request.form['release_date']
    runtime = request.form['runtime']
    status = request.form['status']
    rec_movies = request.form['rec_movies']
    rec_ids = request.form['rec_ids']
    # rec_posters = request.form['rec_posters']

    # get movie suggestions for auto complete
    

    # call the convert_to_list function for every string that needs to be converted to list
    rec_movies = convert_to_list(rec_movies)
    # rec_posters = convert_to_list(rec_posters)
    cast_names = convert_to_list(cast_names)
    cast_chars = convert_to_list(cast_chars)
    cast_profiles = convert_to_list(cast_profiles)
    cast_bdays = convert_to_list(cast_bdays)
    cast_bios = convert_to_list(cast_bios)
    cast_places = convert_to_list(cast_places)
    
    # convert string to list (eg. "[1,2,3]" to [1,2,3])
    cast_ids = cast_ids.split(',')
    cast_ids[0] = cast_ids[0].replace("[","")
    cast_ids[-1] = cast_ids[-1].replace("]","")
    
    # rendering the string to python string
    for i in range(len(cast_bios)):
        cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"','\"')
    
    # combining multiple lists as a dictionary which can be passed to 
    # the html file so that it can be processed easily and the order of information will be preserved
    movie_cards = {recommend_movie_poster[i]: rec_movies[i] for i in range(len(recommend_movie_poster))}
    
    casts = {cast_names[i]:[cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(len(cast_profiles))}

    cast_details = {cast_names[i]:[cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]] for i in range(len(cast_places))}

    # web scraping to get user reviews from IMDB site
    sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    soup_result = soup.find_all("div",{"class":"text show-more__control"})

    reviews_list = [] # list of reviews
    reviews_status = [] # list of comments (good or bad)
    for reviews in soup_result:
        if reviews.string:
            reviews_list.append(reviews.string)
            # passing the review to our model
            movie_review_list = np.array([reviews.string])
            movie_vector = vectorizer.transform(movie_review_list)
            pred = clf.predict(movie_vector)
            reviews_status.append('Good' if pred else 'Bad')
            # reviews_status.append('Good')

    # combining reviews and comments into a dictionary
    reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}     

    # passing all the data to the html file
    # return render_template('recommend.html',title=title,poster=poster,overview=overview,vote_average=vote_average,
    #    release_date=release_date,genres=genres,cast_details=cast_details,casts=casts
    #     )
    return render_template('recommend.html',title=title,poster=poster,overview=overview,vote_average=vote_average,
        vote_count=vote_count,release_date=release_date,runtime=runtime,status=status,genres=genres,
        movie_cards=movie_cards,casts=casts,cast_details=cast_details, reviews = reviews)
#reviews=movie_reviews

@app.route('/filter')
def filter():
    actors = actor['Actor_Name'].to_list()
    directors = filter_data['Directors'].unique().tolist()
    actors.insert(0, 'Any')
    directors.insert(0, 'Any')
    
    years = ['1990s', 'Early 2000s', 'Late 2000s/Early 2010s', '2010s/Present']
    years.insert(0, 'Any')
    return render_template('new.html', actors = actors, directors = directors, years = years)


# @app.route('/filter_movie')
@app.route('/filtering',methods=["POST"])
def filtering():
    actors = request.form['actors']
    directors = request.form['directors']
    years = request.form['years']
    actors = convert_to_list(actors)
    directors = convert_to_list(directors)
    years = convert_to_list(years)
    act = []
    for actor in actors:
        if actor == "Any":
            act.extend(filter_data['Title'].to_list())
        else:
            act.extend(filter_data.query('cast1 == @actor')['Title'].to_list())
            act.extend(filter_data.query('cast2 == @actor')['Title'].to_list())
    dir = []
    for director in directors:
        if director == "Any":
            dir.extend(filter_data['Title'].to_list())
        else:
            dir.extend(filter_data.query('Directors == @director')['Title'].to_list())
    year = []
    start = {'1990s': 1990, 'Early 2000s': 2000, 'Late 2000s/Early 2010s': 2010, '2010s/Present': 2014}
    end = {'1990s': 1999, 'Early 2000s': 2009, 'Late 2000s/Early 2010s': 2014, '2010s/Present': 2024}

    for y in years:
        if y == "Any":
            year.extend(filter_data['Title'].to_list())
        else:
            s = start[y]
            e = end[y]
            year.extend(filter_data.query('Year >= @s and Year <= @e')['Title'].to_list())



    set1 = set(act)
    set2 = set(dir)
    set3 = set(year)

    # common = list(set1.intersection(set2))
    common = (set1 & set2 & set3)
    movie_cards = {}
    for i in common:
        p = movie_data[movie_data['Title'] == i].index[0]
        poster = movie_data['Poster_url'][p]
        movie_cards[poster] = i
    # print(movie_cards)
    return render_template('filter_display.html', movie_cards = movie_cards)

@app.route('/gallery',methods=["GET","POST"])
def gallery():
    new = pd.read_csv('data/2024_s.csv')
    new_poster = new['poster'].tolist()
    old = pd.read_csv("data/90_s.csv")
    old_poster = old['poster'].tolist()
    act = pd.read_csv("data/actors_poster.csv")
    actor = act['poster'].tolist()
    return render_template('gallery.html', new_poster = new_poster, old_poster = old_poster, actor = actor)


if __name__ == '__main__':
  app.run(debug=True)

