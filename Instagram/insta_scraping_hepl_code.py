from selenium import webdriver
driver = webdriver.Chrome(executable_path=r'C:\Users\HEPL-IT\chromedriver.exe')
import time
import pandas as pd
from bs4 import BeautifulSoup as bsoup
import json
import numpy as np
time.sleep(10)
username = 'moonbakes.co'
url = 'https://www.instagram.com/{}/?__a=1'.format(username)
print(url)
driver.get(url)
html_source = driver.page_source
soup = bsoup(html_source,"html.parser")
json_string = json.loads(soup.text)
user_id = json_string['graphql']['user']['id']
query = 'id'
next_max_id = ""
nxt = True
final_df = pd.DataFrame()
while nxt:
    url2 = 'https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables=%s"%s":"%s","first":100,"after":"%s"%s' %('{','id',user_id,next_max_id,'}')
    print(url2)
    driver.get(url2)
    html_source = driver.page_source
    soup = bsoup(html_source,"html.parser")
    json_string = json.loads(soup.text)
    for x in json_string['data']['user']['edge_owner_to_timeline_media']['edges']:
        df= pd.DataFrame.from_dict(x, orient ='index')
        final_df = pd.concat([df,final_df])
    if json_string['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']:
        next_max_id = json_string['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        
    else:
        nxt = False
    time.sleep(20)
        
final_df['caption'] = final_df['edge_media_to_caption'].apply(lambda x: x['edges'][0]['node']['text'])
final_df.drop(['edge_media_to_caption'],axis=1,inplace=True)
final_df['Number_of_comments'] = final_df['edge_media_to_comment'].apply(lambda x: x['count'])
final_df.drop(['edge_media_to_comment'],axis=1,inplace=True)
final_df['Number_of_likes'] = final_df['edge_media_preview_like'].apply(lambda x: x['count'])
final_df.drop(['edge_media_preview_like'],axis=1,inplace=True)
final_df['owner_id'] = final_df['owner'].apply(lambda x: x['id'])
final_df.drop(['owner'],axis=1,inplace=True)
final_df['index'] = [x for x in range(len(final_df))]
final_df = final_df.set_index('index')
finals_df = pd.DataFrame()
for index,row in final_df.iterrows():
    if row['Number_of_comments'] == 0:
        pass
    else:
        url3 =  'https://www.instagram.com/graphql/query/?query_hash=33ba35852cb50da46f5b5e889df7d159&variables={"shortcode":"%s","first":%s,"after":""}' %(row['shortcode'],row['Number_of_comments'])
        print(url3)
        driver.get(url3)
        html_source = driver.page_source
        soup = bsoup(html_source,"html.parser")
        json_string = json.loads(soup.text)
        for x in json_string['data']['shortcode_media']['edge_media_to_comment']['edges']:
            df= pd.DataFrame.from_dict(x, orient ='index')
            df['shortcode'] = row['shortcode']
            finals_df = pd.concat([df,finals_df])
            print(finals_df)
            time.sleep(10)
final = pd.merge(final_df,finals_df,on='shortcode',hgtow='outer')
final['commentor_id'] = final['owner'].apply(lambda x: x['id'] if x==x else np.nan)
final['commentor_profile_pic'] = final['owner'].apply(lambda x: x['profile_pic_url'] if x==x else np.nan)
final['username_commentor'] = final['owner'].apply(lambda x: x['username'] if x==x else np.nan)
final.drop('owner',axis=1,inplace=True)
final.to_excel("sanchu_animalhospital_instagram.xlsx")
