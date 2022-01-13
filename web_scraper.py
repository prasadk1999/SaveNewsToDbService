import psycopg2
from indian_express_scraper import *
import sys
from traceback import format_exc


def save_news_to_database():
    all_news = []
    # create connection with database
    conn = psycopg2.connect(database="News", user="postgres", password="postgres",
                            host="database-1.caitjoidtak3.us-east-1.rds.amazonaws.com", port="5432")

    print("Opened database successfully")

    # create cursor to interact with database
    cur = conn.cursor()
    # get all the news in array of News class's object
    all_news = indian_express_news()
    print("News scraped:", len(all_news))
    # loop the array
    cnt = 1
    for i in all_news:
        try:
            print("News {}".format(cnt))
            # check if the news exists in the database.
            #print("News headline:{}".format(i.headline))
            cur.execute(
                "SELECT * from news_articles where headline='{}'".format(i.headline.replace("'", r"''")))
            # if the news does not exist in the database, then insert it into the database
            if(cur.rowcount == 0):
                cur.execute("select nextval('get_unique_number')")
                news_id = cur.fetchone()[0]
                # print("News Id:", news_id)
                # print("Type:", type(i.subheadline))
                # print("Replaced Subheadline:", i.subheadline.replace("'", r"\'"))
                # i.subheadline = i.subheadline.replace("'", "\'")
                # print("Subheadline", i.subheadline)
                cur.execute("""INSERT INTO news_articles VALUES ({},'{}','{}','{}','{}','{}','{}','{}')""".format(
                    news_id, i.article_link, i.timestamp, i.headline.replace("'", r"''"), i.subheadline.replace("'", r"''"), i.section, i.newspaper_name, i.article_image_url))
                # conn.commit()
                print("Article id={} inserted".format(news_id))
            cnt = cnt+1
        except:
            print("Wheww..", sys.exc_info()[0], "occurred.")
            print("Exception:", format_exc())
            break
    conn.commit()
    conn.close()
    print("Connection closed")


if __name__ == "__main__":
    save_news_to_database()
