import requests
import logging
from elasticsearch import Elasticsearch
import datetime

logging.basicConfig(level=logging.INFO, filename='Logs/app.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('api_examples')
class YouTubeVideoParser:
    server = "localhost"
    port_no = 9200
    es_index = "yt_videos"
    doc_type = "videos"
    def __init__(self, keyword):
        self.keyword = keyword
        self.url = "https://www.googleapis.com/youtube/v3/search?"
        self.search_params = {
            "part": "snippet",
            "key": self.get_api_key(),
            "type": "video",
            "q": self.keyword,
            "order": "date",
        }

    def set_published_after(self):
        try:
            publishedAfter = open('last_run.txt').read().strip()
        except:
            publishedAfter = (datetime.datetime.now() - datetime.timedelta(10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.search_params["publishedAfter"] = publishedAfter


    def get_api_key(self):
        api_key = "AIzaSyBINHabsOBVQnCSXx6J9OUSY0zyEefqXFM"
        return api_key


    def get_latest_videos(self):
        self.set_published_after()
        resp = requests.get(self.url, self.search_params)
        status_code = resp.status_code
        if status_code != 200:
            logger.warning(f"get_latest_videos:: Status code not OK, receive {status_code}")
            return False, ""

        return True, resp.json()

    def elastic_search_conn(self):
        self.es = Elasticsearch(host=self.server, port=self.port_no)
        self.es = Elasticsearch()
        mapping = {
	"mappings": {
		"videos": {
			"properties": {
				"video_title": {
					"type": "text"
				},
				"video_desc": {
					"type": "text"
				},
				"video_thumbnail": {
					"type": "text"
				},
				"video_channel": {
					"type": "text"
				},
				"video_publish_time": {
					"type": "date"
		                }
		        }
	            }
                }
            }
        self.es.indices.create(index =self.es_index, ignore=400, body = params)


    def result_parser(self, search_response):
        try:

            results = list()
            for video in search_response["items"]:
                video_details = dict()
                print (f"Type is {type(video)} and text is {video}")
                video_details["video_id"] = video["id"]["videoId"]
                video_details["video_title"] = video["snippet"]["title"]
                video_details["video_desc"] = video["snippet"]["description"]
                video_details["video_thumbnail"] = video["snippet"]["thumbnails"]["medium"]["url"]
                video_details["video_channel"] = video["snippet"]["channelTitle"]
                video_details["video_publish_time"] = video["snippet"]["publishTime"]
                publishedAfter = video["snippet"]["publishTime"]
                results.append(video_details)
            f = open("last_run.txt", 'w')
            f.write(publishedAfter)
            f.close()
            return results
        except:
            logger.error("result_parser:: Error parsing search results")

    def update_database(self, search_results):
        try:
            self.elastic_search_conn()
            for result in search_results:
                id = result['video_id']
                del result['video_id']
                self.es.index(index =self.es_index, doc_type = self.doc_type, id=id, body = result)
                print (result)

        except:
            logger.error("update_database:: Error updating database")

