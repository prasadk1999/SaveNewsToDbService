import psycopg2
from BetterIndiaNewsScraping.better_india_scraper import better_india_news
from indian_express_scraper import *
from BetterIndiaNewsScraping import *
import sys
from traceback import format_exc


def store_news(conn, all_news):

    # create cursor to interact with database
    cur = conn.cursor()
    # get all the news in array of News class's object
    print("News scraped:", len(all_news))
    # loop the array
    cnt = 1
    for i in all_news:
        try:
            print("News {}".format(cnt))
            # check if the news exists in the database.

            cur.execute(
                "SELECT * from news_articles where headline='{}'".format(i.headline.replace("'", r"''")))

            # if the news does not exist in the database, then insert it into the database
            if(cur.rowcount == 0):
                cur.execute("select nextval('get_unique_number')")
                news_id = cur.fetchone()[0]

                cur.execute("""INSERT INTO news_articles VALUES ({},'{}','{}','{}','{}','{}','{}','{}')""".format(
                    news_id, i.article_link, i.timestamp, i.headline.replace("'", r"''"), i.subheadline.replace("'", r"''"), i.section, i.newspaper_name, i.article_image_url))

                print("Article id={} inserted".format(news_id))
            cnt = cnt+1
        except:
            print("Wheww..", sys.exc_info()[0], "occurred.")
            print("Exception:", format_exc())
            break
    conn.commit()
    # conn.close()
    #print("Connection closed")


if __name__ == "__main__":
    conn = psycopg2.connect(database="News", user="postgres", password="postgres",
                            host="database-1.caitjoidtak3.us-east-1.rds.amazonaws.com", port="5432")
    print("Opened database successfully")
    # store_indian_express_news(conn)
    store_news(conn, indian_express_news())
    print("Scraped Indian Express news")
    print("Scraping Better India News")
    store_news(conn, better_india_news())
    conn.close()
    print("Connection closed")
