from yt_crawler import YouTubeVideoParser
import sys
import time
while True:
    try:
        crawler = YouTubeVideoParser(sys.argv[1])
    except:
        raise Exception("NO search query provided")
    try:
        parse_successful, results = crawler.get_latest_videos()
        if parse_successful:
            search_results = crawler.result_parser(results)
            crawler.update_database(search_results)
    except:
        pass
    time.sleep(60)


