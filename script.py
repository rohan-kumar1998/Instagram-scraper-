from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as soup 
import os
import requests
import time
import json
import csv

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
with open('data.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile) 
    title = ['id', 'text', 'text_hashtag','comment_1','comment_2','comment_3','comment_4','comment_5']
    csvwriter.writerow(title)
    for i in range(len(posts)):
        post = posts[i]
        image_DIR = os.path.join(DIR, str(i+1) + ".jpg")
        post_url = "https://www.instagram.com/p/"+str(post)+"/"
        #print(url)
        postClient = urlopen(post_url)
        post_html = postClient.read()
        time.sleep(1)
        post_html = post_html.decode("utf8")
        postClient.close()
        post_soup = soup(post_html, "html.parser")
        post_script = post_soup.find('script', text=lambda t: t.startswith('window._sharedData'))
        post_json = post_script.text.split(' = ', 1)[1].rstrip(';')
        post_data = json.loads(post_json)
        #print(post_data)
        try:
            text_data = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        except:
            text_data = ""
        text_data = text_data.split('#')
        hashtags = ""
        image_url = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
        for j in range(len(text_data)):
            if(j > 0):
                tmp = text_data[j]
                tmp = tmp.split(' ') 
                if(len(tmp) <= 2):
                    hashtags += str(" ") + text_data[j]                 
                else: 
                    text_data[0] += str(' ') + text_data[j]
        text = text_data[0]
        urlretrieve(str(image_url),image_DIR)
        image_id = post
        try: 
            #comment_count = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['count']
            comment_list = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
            comment_count = len(comment_list)
        except:
            comment_count = 0 
            comment_list = []
        #print(comment_list[0]['node']['text'])
        #print(comment_count)
        comments = ['N/A','N/A','N/A','N/A','N/A']
        for j in range(min(comment_count, 5)):
            #tmp = comment_list[i]['node']['text'].split('#')
            #tmp = ' '.join(tmp)
            comments[j] = comment_list[j]['node']['text']
            #comments[i] = tmp    
        print(text) #add try and except for no text -> do later. 
        print(hashtags)
        print(comments)
        fields = [str(i+1).encode('utf-8'), text.encode('utf-8'), hashtags.encode('utf-8')] 
        for j in comments:
            fields.append(j.encode('utf-8'))
        # creating a csv writer object 
        csvwriter.writerow(fields)
