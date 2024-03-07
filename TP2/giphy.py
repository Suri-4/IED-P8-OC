import requests
from plotly.graph_objs import Bar
from plotly import offline

API_KEY = '9w1uNYrtx3ThHChu9LDIbYPrcX5Rup6U'
URL = 'https://api.giphy.com/v1/gifs/trending'

params = {"api_key": API_KEY, "limit": 10, "rating": "g"}
headers = {"Accept": "application/json"}

request = requests.get(URL, params=params, headers=headers)
print(f"Status code: {request.status_code}")

resultat = request.json()

gifs = resultat['data']

gif_titles = []
like = []

for gif in gifs:
    gif_titles.append(gif['title'])
    like.append(gif['like_count'])

data = [{
    'type': 'bar',
    'x': gif_titles,
    'y': like,
}]

layout = {
    'title': 'Gif populaire',
    'xaxis': {'title': 'Nom du gif'},
    'yaxis': {'title': 'Popularité'}
}

fig = {'data': data, 'layout': layout}
offline.plot(fig, filename='gif_like.html')


# params = {"api_key": API_KEY, "limit": 10, "rating": "g"}

# response = requests.get(URL, params=params).json()

# for gif in response['data']:
#     title = gif['title']
#     trending_datetime = gif['trending_datetime']
#     URL = gif["url"]
#     print(f"{title} \n {trending_datetime} \n {URL} \n")