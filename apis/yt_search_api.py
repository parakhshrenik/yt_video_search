from flask import Flask, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
import os
app = Flask(__name__)

es = Elasticsearch(host='localhost', port=9200)
es = Elasticsearch()


@app.route('/search', methods= ['GET'])
def hello_world():
    search_query = request.args.get('search_query')
    page = request.args.get('page')
    print (search_query)
    print (page)
    output = get_search_results(search_query, page)
    #output = "test"
    return str(output)

@app.route('/count', methods=['Get'])
def get_total_count():
    search_query = request.args.get('search_query')
    smart_query = {
        "query": {
            "match": {
                "video_title": {
                    "query": search_query,
                    "fuzziness": "AUTO"
                }
            }
        }
    }
    try:
        res = es.search(index="yt_videos", body=smart_query, sort='video_publish_time:desc', size = 1)
        return str(res['hits']['total'])
    except:
        return "We've hit a minor setback. See ya' soon again"


def get_search_results(search_term, page, size=10):
    smart_query =   {
        "query": {
            "match" : {
                "video_title" : {
                    "query" : search_term,
                    "fuzziness": "AUTO"
                }
            }
        }
    }
    try:
        res = es.search(index="yt_videos", body=smart_query, sort='video_publish_time:desc', from_=page, size = size)
        return format_output(res['hits']['hits'])
    except:
        return "We've hit a minor setback. See ya' soon again"


def format_output(results):
    output_str = ""
    for result in results:
        if "_source" in result:
            print ("result" + str(result) +  "\n\n\n")

            output_str += "TITLE: %s \n" %(result['_source']['video_title'])
            output_str += f"Description: %s \n" %(result['_source']['video_desc'])
            output_str += f"Thumbnail: %s \n" %(result['_source']['video_thumbnail'])
            output_str += f"Published at: %s \n" %(result['_source']['video_publish_time'])
            output_str += "\n\n\n"
    return output_str


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5050)

