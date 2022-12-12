import time
import hashlib  
from PIL import Image
import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(font_scale=10)
PUBLIC_KEY = 'cc4e5692a3f7e7f48ec7b924e636cf3b'
BOLD ='\033[1m'
END ='\033[0m'

def get_single_hero_profile(name):
    """
    Get the profile of searched marvel hero
    Parameters
    ---
    name: string
        Input string for interested marvel character name
    
    """
    url = 'http://gateway.marvel.com/v1/public/characters?nameStartsWith=' 
    option = '&limit=1&orderBy=-modified&'
    m = hashlib.md5() 
    ts = str(time.time())
    ts_byte = bytes(ts, 'utf-8')  
    m.update(ts_byte) 
    m.update(b'cc695d675d0bcda21f1e70dc37be9a0dc59511c9')
    m.update(b"cc4e5692a3f7e7f48ec7b924e636cf3b")
    hasht = m.hexdigest() 
    payload = {'ts': ts, 'apikey': PUBLIC_KEY, 'hash': hasht}
    r = requests.get(url+str(name)+option, params=payload)
    result = r.json()
    if result['data']['count'] == 0:
        print('Ooooops there is no match, please try again (e.g. Spider-Man, Hulk). ')
    else:
        name = result['data']['results'][0]['name']
        description = result['data']['results'][0]['description']
        appear_comic = result['data']['results'][0]['comics']['available']
        appear_series = result['data']['results'][0]['series']['available']
        appear_stories = result['data']['results'][0]['stories']['available']
        appear_events = result['data']['results'][0]['events']['available']
        urls = result['data']['results'][0]['urls']
        wiki_link = ''
        for i in urls:
            if i['type'] =='detail':
                wiki_link = i['url']
        img_url = result['data']['results'][0]['thumbnail']['path']+'.jpg'
        im = Image.open(requests.get(img_url, stream=True).raw)
        new_img = im.resize((500,500))
        print(BOLD + 'NAME: ' +END +name)
        print(BOLD + 'DESCRIPTION: ' +END +description)
        print(BOLD + 'APPEARS IN COMICS: ' +END +str(appear_comic)+' times')
        print(BOLD + 'APPEARS IN SERIES: ' +END +str(appear_series)+' times')
        print(BOLD + 'APPEARS IN STORIES: ' +END +str(appear_stories)+' times')
        print(BOLD + 'APPEARS IN EVENTS: ' +END  +str(appear_events)+' times')
        if wiki_link !='':
            print(BOLD + 'MORE INFO: '+ END +wiki_link)
        plt.axis('off')
        plt.imshow(new_img)
        plt.show()  

def get_popular_hero_using_inital(letter):
    '''
    get popular 20 marvel heros using initals

    Parameters
    ---
    letter: char
        Input char for interested marvel character initials
    '''
    if len(str(letter)) > 1:
        print('Ooooops only accepts single letter/number, please try again (e.g. s, b).')
    else:
        url = 'http://gateway.marvel.com/v1/public/characters?nameStartsWith=' 
        option = '&limit=20&orderBy=-modified&'
        m = hashlib.md5() 
        ts = str(time.time())
        ts_byte = bytes(ts, 'utf-8')  
        m.update(ts_byte) 
        m.update(b'cc695d675d0bcda21f1e70dc37be9a0dc59511c9')
        m.update(b"cc4e5692a3f7e7f48ec7b924e636cf3b")
        hasht = m.hexdigest() 
        payload = {'ts': ts, 'apikey': PUBLIC_KEY, 'hash': hasht}
        r = requests.get(url+str(letter)+option, params=payload)
        result = r.json()
        heros = result['data']['results']
        for i in heros:
            name = i['name']
            description = i['description']
            appear_comic = i['comics']['available']
            appear_series = i['series']['available']
            appear_stories = i['stories']['available']
            appear_events = i['events']['available']
            urls = i['urls']
            wiki_link = ''
            for j in urls:
                if j['type'] =='detail':
                    wiki_link = j['url']
            img_url = i['thumbnail']['path']+'.jpg'
            im = Image.open(requests.get(img_url, stream=True).raw)
            new_img = im.resize((250,250))
            print(BOLD + 'NAME: ' +END +name)
            print(BOLD + 'DESCRIPTION: ' +END +description)
            print(BOLD + 'APPEARS IN COMICS: ' +END +str(appear_comic)+' times')
            print(BOLD + 'APPEARS IN SERIES: ' +END +str(appear_series)+' times')
            print(BOLD + 'APPEARS IN STORIES: ' +END +str(appear_stories)+' times')
            print(BOLD + 'APPEARS IN EVENTS: ' +END  +str(appear_events)+' times')
            if wiki_link !='':
                print(BOLD + 'MORE INFO: '+ END +wiki_link)
            plt.axis('off')
            plt.imshow(new_img)
            plt.show()  

def get_popular_hero_stats_with_initials(letter):
    '''
    get popular heros' statistics with the searched letter

    Parameters
    ---
    letter: char
        Input char for interested marvel character initials
    '''
    if len(str(letter)) > 1:
        print('Ooooops only accepts single letter/number, please try again (e.g. s, b).')
    else:
        url = 'http://gateway.marvel.com/v1/public/characters?nameStartsWith=' 
        option = '&limit=100&orderBy=-modified&'
        m = hashlib.md5() 
        ts = str(time.time())
        ts_byte = bytes(ts, 'utf-8')  
        m.update(ts_byte) 
        m.update(b'cc695d675d0bcda21f1e70dc37be9a0dc59511c9')
        m.update(b"cc4e5692a3f7e7f48ec7b924e636cf3b")
        hasht = m.hexdigest() 
        payload = {'ts': ts, 'apikey': PUBLIC_KEY, 'hash': hasht}
        r = requests.get(url+str(letter)+option, params=payload)
        result = r.json()
        heros = result['data']['results']
        
        for i in range(len(heros)):
            if i == 0:
                name = heros[i]['name']
                appear_comic = heros[i]['comics']['available']
                appear_series = heros[i]['series']['available']
                appear_stories = heros[i]['stories']['available']
                temp = [[name, appear_comic, appear_series, appear_stories]]
                df = pd.DataFrame(temp, columns = ['character', 'comics', 'series' , 'stories'])
            else:
                name = heros[i]['name']
                appear_comic = heros[i]['comics']['available']
                appear_series = heros[i]['series']['available']
                appear_stories = heros[i]['stories']['available']
                temp = [name,appear_comic,appear_series,appear_stories]
                df.loc[len(df)] = temp
        df = df.sort_values(by=['comics', 'series','stories'],ascending=False).reset_index(drop = True)
        df1 = df.iloc[:8, :]
        df2 = df1.melt(id_vars = ['character'], value_vars = df1.columns.drop('character').tolist())
        ax = sns.catplot(data = df2, x = 'variable',y = 'value', hue = 'character', kind ='bar', height = 60, aspect = 21/8, palette = sns.color_palette("ch:s=-.2,r=.6"))
        ax.set(xlabel='Character', ylabel='Number of occurrences')
        plt.show()
