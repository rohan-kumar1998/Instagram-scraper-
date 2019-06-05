from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as soup 
import os
import requests
import time
import json
#import csv

posts = []

end_cursor = '' 
tag = 'britain' 
page_count = 5 

for i in range(page_count):
    url = "https://www.instagram.com/explore/tags/{0}/?__a=1&max_id={1}".format(tag, end_cursor)
    r = requests.get(url)
    data = json.loads(r.text)
    
    end_cursor = data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor'] # value for the next page
    edges = data['graphql']['hashtag']['edge_hashtag_to_media']['edges'] # list with posts
    
    for item in edges:
        if(item['node']['shortcode'] not in posts):
            posts.append(item['node']['shortcode'])
    time.sleep(1) # insurance to not reach a time limit
print(len(posts))

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
