# imports
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd
import acquire

import warnings
warnings.filterwarnings('ignore')


#################################################
def basic_clean(article):
    '''This function takes in string and converts to lower case, normalize unicode characters and
        replace anything that is not a letter, number, whitespace or a single quote.
    '''
        
    # lowercase everything
    article = article.lower()
    
    # normalize unicode characters
    article = unicodedata.normalize('NFKD', article)\
            .encode('ascii', 'ignore')\
            .decode('utf-8', 'ignore')
    # Replace anything that is not a letter, number, whitespace or a single quote.
    article = re.sub(r"[^a-z0-9'\s]", '', article)
    
    return article

#################################################
def tokenize(article):
    """ This function takes in article parameter as sting and teturns a tokenized string. """
    # Creatr an object for tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # Use tokenizer object to tokenize the parameter article here
    article =  tokenizer.tokenize(article, return_str = True)
    
    return article


#################################################
def stem(article):
    
    """ This function takes in article parameter as string and returns article with words stemmed"""
    
    # Create the nltk stemmer object, then use it
    ps = nltk.porter.PorterStemmer()
    
    # Splitting the words in article parameter
    article_splitted = article.split()
    
    # Use stemmer to stem each word in the list of words in article_splitted
    stems = [ps.stem(word) for word in article_splitted]

    # joining back all stemmed words stems here
    article = ' '.join(stems)
    
    return article


#################################################
def lemmatize(article):
    """ This function will lemmatize the article parameter as string 
        and returns string with words lemmatized.
    """
    # Create an object for lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Splitting the words in article parameter
    article_splitted = article.split()
    
    # Use lemmatizer object to lemmatize each word in the list of words in article_splitted
    lemmas = [wnl.lemmatize(word) for word in article_splitted]

    # joining back all stemmed words stems here
    article = ' '.join(lemmas)
    
    return article

#################################################
def remove_stopwords(article, extra_words = [], exclude_words = []):
    """ This function takes in article as parameter as string, optional extra_words, 
    and optional exclude_words paramters with empty lists and returns a string."""
    # Create stopword_list object in english
    stopword_list = stopwords.words('english')
    
    # Removing exclude_words from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(exclude_words)
    
    # Adding extra_words to stopword_list to remove these in my text
    stopword_list = stopword_list.union(set(extra_words))
    
    # spliting words in article
    words = article.split()
    
    # Creating a list of words from my article with stopwords removed and assign to variable
    filtered_words = [w for w in words if w not in stopword_list]
    
    # Joining words in the filtered_words back into string and assign to variable
    article_without_stopwords = ' '.join(filtered_words)

    return article_without_stopwords

#################################################
def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    df['stemmed'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(stem)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    df['lemmatized'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(lemmatize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    return df[['title', column,'clean', 'stemmed', 'lemmatized']]





