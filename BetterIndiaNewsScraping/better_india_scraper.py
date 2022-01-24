from bs4 import BeautifulSoup
import requests
import pandas as pd
from requests.api import head
from model import *


def better_india_news():
    better_india_array = []
    main_url = "https://www.thebetterindia.com/topics/"
    website = requests.get(main_url)

    # getting list of sections
    soup = BeautifulSoup(website.content, 'html.parser')

    list_of_topics_links = []
    topics = soup.select('.elementor-button-wrapper')
    # gettin all the topic links in list_of_topics_links array
    for t in topics:
        list_of_topics_links.append(t.select_one('a')['href'])

    for topic_link in list_of_topics_links:

        section_page_request = requests.get(topic_link)
        section_page_soup = BeautifulSoup(
            section_page_request.content, 'html.parser')

        # section name
        section_name = section_page_soup.select_one(
            '.page-description').get_text()

        articles_list = section_page_soup.select('article')
        list_of_articles_link = []
        # gettting all the articles link in array
        for al in articles_list:
            list_of_articles_link.append(
                al.select_one('.entry-title a')['href'])

        for article_link in list_of_articles_link:
            article_image_url = ''
            article_timestamp = ''
            article_headline = ''
            article_subheadline = ''

            article_page_request = requests.get(article_link)
            article_page_soup = BeautifulSoup(
                article_page_request.content, 'html.parser')

            # article_image_url
            article_image_url = article_page_soup.select_one(
                '._tbi-featured-img img')['data-gmsrc']
            article_image_url

            # article_timestamp
            article_timestamp = article_page_soup.find(
                'li', {'itemprop': 'datePublished'}).find('label').get_text()
            article_timestamp

            # article_headline
            article_headline = article_page_soup.find(
                'h1', class_='entry-title').get_text()
            # print("{}:{}".format(section_name, article_headline))

            # article_subheadline
            if(article_page_soup.find('p', class_='tbi-subtitle') != None):
                article_subheadline = article_page_soup.find(
                    'p', class_='tbi-subtitle').get_text()

            better_india_array.append(News(article_link, article_timestamp, article_headline,
                                      article_subheadline, section_name, "Better India", article_image_url))

    return better_india_array
