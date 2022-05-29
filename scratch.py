import requests
from bs4 import BeautifulSoup
YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D'
response = requests.get(YOUTUBE_TRENDING_URL)
print('status code',response.status_code)

with open('trending.html','w') as f:
  f.write(response.text)

doc = BeautifulSoup(response.text,'html.parser')
print("Page_title :",doc.title.text)

video_tags = doc.find_all('div',class_ ="style-scope ytd-expanded-shelf-contents-renderer")
print(len(video_tags))