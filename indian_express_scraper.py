from bs4 import BeautifulSoup
import requests
import pandas as pd
from requests.api import head
from model import *


def indian_express_news():
    # Initialization
    indian_express_array = []
    main_url = 'https://indianexpress.com'
    articles_details = pd.DataFrame(columns=[
                                    'Section', 'Link To Page', 'Headline', 'SubHeadline', 'Timestamp', 'Main Content', 'Image URL'])

    # Requesting the website
    website = requests.get(main_url)

    # getting list of sections
    soup = BeautifulSoup(website.content, 'html.parser')
    sections = soup.find_all('ul', {'id': 'navbar'})
    sections_title = soup.select('#navbar > li')

    # filtering sections list so that unwanted sections are not added in the list
    sections_title_filtered = []
    for s in sections_title:
        if(s.find('a', {'href': '/login'}) == None and s.find('a', {'href': '/subscribe/'}) == None and s.find('a', {'href': '/'}) == None):
            sections_title_filtered.append(s.find('a'))

    section_numbers = [0, 1, 3, 4]
    for s_number in section_numbers:
        section_a_tag = sections_title_filtered[s_number]
        section_href = section_a_tag.get('href')
        # Html layout of India and Sports section is same, thus they can be scraped using same code
        if s_number == 0 or s_number == 4:
            if s_number == 0:
                section_name = 'India'
            else:
                section_name = 'Sports'
            # iterating first 1 page
            for pages in range(1, 2):
                # requesting for first page
                first_section_request = requests.get(
                    main_url+section_href+'page/'+str(pages)+'/')
                # getting object of first page
                first_section_soup = BeautifulSoup(
                    first_section_request.content, 'html.parser')

                # filter articles(only keep no-premium articles in the soup object)
                for i in first_section_soup.findAll("div", {'class': 'm-premium'}):
                    i.decompose()

                first_section_articles_list = first_section_soup.select(
                    '.articles')
                # list of articles
                len(first_section_articles_list)

                # looping the list to get content of each article

                for articles in first_section_articles_list:
                    # go to each articles page

                    article_link = articles.select_one('a')
                    article_url = article_link.get('href')
                    article_page = requests.get(article_link.get('href'))

                    article_page_soup = BeautifulSoup(
                        article_page.content, 'html.parser')
                    # get heading of the articles
                    # headline_content = article_page_soup.select(
                    #    '.heading-part')
                    if(article_page_soup.select_one('.custom-caption img') != None):
                        article_image_url = article_page_soup.select_one(
                            '.custom-caption img')['data-lazy-src']
                    else:
                        article_image_url = None

                    if(article_page_soup.find("h1", {'itemprop': 'headline'}) != None):
                        heading = article_page_soup.find(
                            "h1", {'itemprop': 'headline'}).get_text()
                    else:
                        heading = None

                    if(article_page_soup.find("h2", {'itemprop': 'description'}) != None):
                        subheading = article_page_soup.find(
                            "h2", {'itemprop': 'description'}).get_text()
                    else:
                        subheading = None
                    # subheading = headline_content[0].find(
                    #    class_='synopsis').get_text().strip('\r\n')

                    # main_body_content = article_page_soup.select('.articles')[
                    #     0]
                    # main_body_list_paragraphs = main_body_content.select('p')

                    # main_body = ""
                    # for i in main_body_list_paragraphs:
                    #     main_body = main_body+(i.get_text())
                    editor_details_timestamp = article_page_soup.find(
                        'span', {'itemprop': 'dateModified'})['content']

                    articles_details = articles_details.append({"Section": section_name,
                                                               "Link To Page": article_url,
                                                                "Headline": heading,
                                                                "SubHeadline": subheading,
                                                                "Timestamp": editor_details_timestamp,
                                                                # "Main Content": main_body,
                                                                "Image URL": article_image_url
                                                                }, ignore_index=True)
                    indian_express_array.append(
                        News(article_url, editor_details_timestamp, heading, subheading, section_name, "Indian Express", article_image_url))
        else:
            if s_number == 1:
                section_name = 'World'
                for pages in range(1, 2):
                    second_section_request = requests.get(
                        main_url+section_href+'page/'+str(pages)+'/')
                    # getting object of first page
                    second_section_soup = BeautifulSoup(
                        second_section_request.content, 'html.parser')

                    # filter articles(only keep no-premium articles in the soup object)
                    for i in second_section_soup.select('#north-east-data li'):
                        if not i.get_text(strip=True):
                            i.replace_with('')
                        if(len(i.select('.ie-premium')) > 0):
                            i.decompose()
                        if(len(i.select('.adboxtop')) > 0):
                            i.decompose()

                    a = second_section_soup.select('#north-east-data li h3 a')
                    list_of_articles_href = []

                    # add link of featured article
                    list_of_articles_href.append(second_section_soup.select(
                        '.northeast-topbox a')[0].get('href'))
                    # get a list of all the links of the articles on that page
                    for ar in a:
                        list_of_articles_href.append(ar.get('href'))

                    for article in list_of_articles_href:
                        article_page = requests.get(article)
                        article_page_soup = BeautifulSoup(
                            article_page.content, 'html.parser')

                        # get heading of the articles
                        # if(article_page_soup.select('.heading-part')!=None):
                        #     headline_content = article_page_soup.select(
                        #         '.heading-part')
                        # else:
                        #     headline_content=None

                        if(article_page_soup.select_one('.custom-caption img') != None):
                            article_image_url = article_page_soup.select_one(
                                '.custom-caption img')['data-lazy-src']
                        else:
                            article_image_url = None

                        if(article_page_soup.find("h1", {'itemprop': 'headline'}) != None):
                            heading = article_page_soup.find(
                                "h1", {'itemprop': 'headline'}).get_text()
                        else:
                            heading = None

                        if(article_page_soup.find("h2", {'itemprop': 'description'}) != None):
                            subheading = article_page_soup.find(
                                "h2", {'itemprop': 'description'}).get_text()
                        else:
                            subheading = None
                        # subheading = headline_content[0].find(
                        #     class_='synopsis').get_text().strip('\r\n')

                        # main_body_content = article_page_soup.select('.articles')[
                        #     0]
                        # main_body_list_paragraphs = main_body_content.select(
                        #     'p')

                        # main_body = ""
                        # for i in main_body_list_paragraphs:
                        #     main_body = main_body+(i.get_text())

                        editor_details_timestamp = article_page_soup.find(
                            'span', attrs={"itemprop": "dateModified"})['content']

                        articles_details = articles_details.append({'Section': 'World',
                                                                    'Link To Page': article, "Headline": heading,
                                                                    "SubHeadline": subheading,
                                                                    "Timestamp": editor_details_timestamp,
                                                                   # "Main Content": main_body,
                                                                    'Image URL': article_image_url
                                                                    }, ignore_index=True)
                        indian_express_array.append(
                            News(article_url, editor_details_timestamp, heading, subheading, section_name, "Indian Express", article_image_url))

            if s_number == 3:
                section_name = 'Opinion'
                for pages in range(1, 2):
                    third_section_request = requests.get(
                        main_url+section_href+'page/'+str(pages)+'/')
                    # getting object of first page
                    third_section_soup = BeautifulSoup(
                        third_section_request.content, 'html.parser')

                    # filter articles(only keep no-premium articles in the soup object)
                    for index, i in enumerate(third_section_soup.select('.opi-story')):
                        if not i.get_text(strip=True):
                            i.replace_with('')
                        if(len(i.select('.ie-premium')) > 0):
                            i.decompose()
                        # remove first 4 articles because they are repeated
                        if(index <= 3):
                            i.decompose()

                    articles_list_soup = third_section_soup.select(
                        '.opi-story')
                    list_of_articles_href = []

                    # add link of featured article
                    list_of_articles_href.append(
                        third_section_soup.select('.leadstory a')[0].get('href'))
                    # get a list of all the links of the articles on that page
                    for articles in articles_list_soup:
                        list_of_articles_href.append(
                            articles.select_one('h2 a')['href'])

                    # go to each article page and scrape details
                    for article in list_of_articles_href:
                        article_page = requests.get(article)
                        article_page_soup = BeautifulSoup(
                            article_page.content, 'html.parser')

                        # get heading of the articles
                        # headline_content = article_page_soup.select(
                        #     '.heading-part')
                        if(article_page_soup.select_one('.custom-caption img') != None):
                            article_image_url = article_page_soup.select_one(
                                '.custom-caption img')['data-lazy-src']
                        else:
                            article_image_url = None

                        if(article_page_soup.find("h1", {'itemprop': 'headline'}) != None):
                            heading = article_page_soup.find(
                                "h1", {'itemprop': 'headline'}).get_text()
                        else:
                            heading = None

                        if(article_page_soup.find("h2", {'itemprop': 'description'}) != None):
                            subheading = article_page_soup.find(
                                "h2", {'itemprop': 'description'}).get_text()
                        else:
                            subheading = None
                        # subheading = headline_content[0].find(
                        #     class_='synopsis').get_text().strip('\r\n')

                        # main_body_content = article_page_soup.select('.articles')[
                        #     0]
                        # main_body_list_paragraphs = main_body_content.select(
                        #     'p')

                        # main_body = ""
                        # for i in main_body_list_paragraphs:
                        #     main_body = main_body+(i.get_text())

                        editor_details_timestamp = article_page_soup.find(
                            'span', attrs={"itemprop": "dateModified"})['content']

                        articles_details = articles_details.append({'Section': 'Opinion',
                                                                    'Link To Page': article, "Headline": heading,
                                                                    "SubHeadline": subheading,
                                                                    "Timestamp": editor_details_timestamp,
                                                                   # "Main Content": main_body,
                                                                    'Image URL': article_image_url
                                                                    }, ignore_index=True)
                        indian_express_array.append(
                            News(article_url, editor_details_timestamp, heading, subheading, section_name, "Indian Express", article_image_url))
    return indian_express_array
