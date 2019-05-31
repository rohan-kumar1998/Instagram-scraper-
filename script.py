from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as soup 
import json
import os

url = "https://www.instagram.com/explore/tags/italy/"

uClient = urlopen(url)
page_html = uClient.read()
page_html = page_html.decode("utf8")	

uClient.close()

page_soup = soup(page_html, "html.parser")

script = page_soup.find('script', text=lambda t: t.startswith('window._sharedData'))

page_json = script.text.split(' = ', 1)[1].rstrip(';')

page_json
data = json.loads(page_json)

posts = []
for post in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
            posts.append(post['node']['shortcode'])

DIR = 'pictures'
if not os.path.isdir(f'{DIR}'):
        os.makedirs(f'{DIR}')
for i in range(len(posts)):
    post = posts[i]
    image_DIR = os.path.join(DIR, str(post) + ".jpg")
    post_url = "https://www.instagram.com/p/"+str(post)+"/"
    #print(url)
    postClient = urlopen(post_url)
    post_html = postClient.read()
    post_html = post_html.decode("utf8")
    postClient.close()
    post_soup = soup(post_html, "html.parser")
    post_script = post_soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    post_json = post_script.text.split(' = ', 1)[1].rstrip(';')
    post_data = json.loads(post_json)
    #print(post_data)
    text_data = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
    text_data = text_data.split('#')
    hashtags = []
    image_url = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
    text = text_data[0]
    for i in range(len(text_data)):
        if(i > 0):
            hashtags.append(text_data[i])
    urlretrieve(str(image_url),image_DIR)
    image_id = post
    comment_count = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['count']
    comment_list = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges'] 
    #print(comment_list[0]['node']['text'])
    #print(comment_count)
    comments = []
    for i in range(comment_count):
         comments.append(comment_list[i]['node']['text'])
    print(text) #add try and except for no text -> do later. 
    print(hashtags)
    print(comments)