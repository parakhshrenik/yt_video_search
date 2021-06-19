# Kontainerized YouTube Video Search
**Disclaimer** :This search is just meant for educational purposes or personal use only and not for commercial use. Please go thorugh Google's terms and conditions before using this. The author does not take any responsibility for breach of any Google Terms & Conditions. 

With that _out of the way_ let's get started. This is a tool to get YouTube video details based on a keyword. 
The videos are shown in a paginated and reverse chronological order. 

Use the `/seach` API to search for the video details. Use `HTTP GET ` to use the same with the following parameters:
 - page : This indicates the page number. The number of videos returned per page is 10
 - search_query : This indicates the search query based on which the response would be provided
 
Use the `count` API to fetch the total matches for a given search query. The said api takes only one parameter. The accepted method for making this API call is `HTTP GET`

* [Containers](#containers)
* [Libraries](#libraries)
* [Getting Started](#how_to)
    * [Running Elasticsearch](#running-elasticsearch)
    * [The Crawler](#the-crawler)
    * [APIs](#apis)


## Containers 
The tool has three containers for which the images are build from the base images: 
- Python:3.8 : This base image is use for both running the crawler and the api exposed to search for videos from the database. 
- elasticsearch:6.4.0 : This base image is used directly as the database for storing all the relevant search results by the __crawler__

## Libraries 
The following python libraries are used :
- flask
- requests
- elasticsearch


 ## Getting Started
 In order to get started, docker must be installed on the system. After cloning the repository, the first step would be to install the elasticsearch container 
 
 ### Running Elasticsearch
 In order to run the elasticsearch container, the base image is used. The port mapping is done such that the host expose 9200 and the container exposes 9300
 ```buildoutcfg
docker run -d --name elasticsearch --net somenetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:6.4.0
```
### The Crawler
People call me ___THE CRAWLER___  
Because I keep crawling Youtube Everyminute to look for new videos on a given topic/search query. 
"The crawler" makes use of Google APIs to continuously searching for newer videos. After every search, the last video's published date and time is stored is a text file. While making subsequent calls, the last run is checked and the crawler only looks for videos published after that.  
The crawler container is built by using `Python:3.8` image as the base image. 
After the repository is cloned go to the crawler directory
```buildoutcfg
cd yt_video_search/crawler
docker build -t <image_name> .
```
Once the image is built after installing all the dependencies, run the newly built image
```
docker run <image_name>
```
To check the the container is running, run the below command :
```buildoutcfg
docker ps
```

### APIs
The APIs exposed by this tool are 
* search
* count
As mentioned above, the search API expects _page_ and _search_query_ as parameters both of which are __compulsory__. And the _count_ API expects the _search_query_ as parameter. 
 After the repository is cloned go to the apis directory
 ```buildoutcfg
cd yt_video_search/apis
dokcer build -t <image_name> .
```
Once the image is built after installing all the dependencies, run the newly built image
```
docker run <image_name>
```
To check the the container is running, run the below command :
```buildoutcfg
docker ps
```

After verifying all the three above containers are runnning, use cURL or POSTMAN to make API calls. 
An example curl query on localhost might look like :
```buildoutcfg
curl 'localhost:8080/search?page=1&search_query=cricket'
```


