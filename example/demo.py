import requests
import pandas as pd
import pickle

# movie = input("enter movie: ")
my_api_key = '64f14bfc62f718d2cf962fe150e5bc40'

# url = 'https://api.themoviedb.org/3/search/movie?api_key='+my_api_key+'&query='+movie

def findmalayalam(data):
    movies_list = data.get('movies_list')  # Extract the movies_list
    for movie in movies_list['results']:
        if movie['original_language'] == 'ml':
            selected_movie = movie
            return (selected_movie)


def rcmd(m):
    m = m.lower()
    data['Title'] = data['Title'].str.lower()
    if m not in data['Title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['Title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['Title'][a])
        return l

def similarity_(movie):
    rc = rcmd(movie)

    if type(rc)==type('string'):
        return rc
    else:
        m_str="---".join(rc)
        return m_str

# response = requests.get(url)
# result = response.json()
# details = {'movies_list': result}
# movie = findmalayalam(details)

# print(movie)

# data = pd.read_csv("data/final.csv")
# similarity = pickle.load(open('data/similarity.pkl','rb'))

# movie = data[data['Title'] == "Bramayugam"]
# id = movie.imdb_id
# id = list(id)
# print(id)

# url = "https://api.themoviedb.org/3/find/{}?api_key=64f14bfc62f718d2cf962fe150e5bc40&external_source=imdb_id".format(id[0])

# response = requests.get(url)
# result = response.json()
# print(type(result))

# print(similarity_("bramayugam"))

url = "https://api.themoviedb.org/3/person/popular?api_key=64f14bfc62f718d2cf962fe150e5bc40"
response = requests.get(url)
result = response.json()
print(result)