# Imports

from requests import get
import pandas as pd
from bs4 import BeautifulSoup
from time import strftime
import requests



#########################

def get_front_page_links():
    '''
    This function will get us codeup blog landing page and return a list of urls that blog posts on the page.
    '''
    # Some websites don't accept the pyhon-requests default user-agent
    headers = {'User-Agent': 'Codeup Data Science'} 

    # defining url
    url = 'https://codeup.com/blog/'


    # getting response from server
    response = get(url, headers = headers)
    soup = BeautifulSoup(response.text)
    
    # all links
    links = [link['href'] for link in soup.select('.more-link')]
    
    return links

##########################

def parse_codeup_blog_article(url):
    
    ''' This function pass url and gives title, content, and date published. '''
    
    # Some websites don't accept the pyhon-requests default user-agent
    headers = {'User-Agent': 'Codeup Data Science'} 
    
    response = get(url, headers = headers)
    
    # converting response to text
    html = response.text
    
    # Make a soup variable holding the response content
    soup = BeautifulSoup(html)
    
    # title
    title = soup.select('.et_post_meta_wrapper')[0].h1.text
    
    
    # content
    content = soup.select('.entry-content')[0].text.strip()
    content = content.replace('\n', '')
    
    # published date
    published = soup.select('.published')[0].text

    
    
    return {
        'title': title, 
         'content': content,
        'date published' : published
     } 

##########################

def get_blog_articles():
    """This function returns a DataFrame with column as title, published and content"""
    links = get_front_page_links()
    df = pd.DataFrame([parse_codeup_blog_article(link) for link in links])
    return df

##########################

def parse_news_card(card):
    'Given a news card object, returns a dictionary of the relevant information.'
    card_title = card.select_one('.news-card-title')
    output = {}
    output['title'] = card.find('span', itemprop = 'headline').text
    output['author'] = card.find('span', class_ = 'author').text
    output['content'] = card.find('div', itemprop = 'articleBody').text
    output['date'] = card.find('span', clas ='date').text
    return output

##########################

def parse_inshorts_page(url):
    '''Given a url, returns a dataframe where each row is a news article from the url.
    Infers the category from the last section of the url.'''
    category = url.split('/')[-1]
    response = requests.get(url, headers={'user-agent': 'Codeup DS'})
    soup = BeautifulSoup(response.text)
    cards = soup.select('.news-card')
    df = pd.DataFrame([parse_news_card(card) for card in cards])
    df['category'] = category
    return df

##########################

def get_inshorts_articles():
    '''
    Returns a dataframe of news articles from the business, sports, technology, and entertainment sections of
    inshorts.
    '''
    url = 'https://inshorts.com/en/read/'
    categories = ['business', 'sports', 'technology', 'entertainment']
    df = pd.DataFrame()
    for cat in categories:
        df = pd.concat([df, pd.DataFrame(parse_inshorts_page(url + cat))])
    df = df.reset_index(drop=True)
    return df










