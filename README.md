# Fetch tool usage
```
positional arguments:
  N                     an URL to process

options:
  -h, --help            show this help message and exit
  -m METADATA, --metadata METADATA
                        Extract meta for this URL
  -c, --clone           Clone webpage(s) with resources
No URLs arg and meta provided, exiting
```

Input webpages HTML is saved to ./fetch_pages folder and meta information to ./fetch_meta folder

# Basic requirements & architecture
The task of creating the fetch tool is looking similar to what web crawlers or spiders do. Implementing a straightforward
scenario would be easy but naive from the point of view of modern anti scraping tools and dynamic webpages. It would be 
interesting to consider these resources before starting implementation:
1. https://medium.com/geekculture/web-scraping-101-tools-techniques-and-best-practices-417e377fbeaf
2. https://gologin.com/blog/web-scraping-service-cloudflare-bypass#Way_8_Privacy_Browsers_For_Web_Scraping_Protection

After carefully considering the resources and analyzing information I came to the following big view of an extensible
tool design(See arch.png):
1. Crawler class can be extended for any programmer needs but basic version can provide singe page parsing
2. Request class basically stores setting of what we can do: method type, headers, cookies etc
3. Response stores output of performed request according to given settings
4. Loader classes act to perform Requests by reading request data and using suitable tools: simple built in behaviour or more complex JS rendering and Cloudfare bypassing(not implemented)
5. A Response object reaches its Crawler and gets processed. Here we could extract all useful data i.e page content, links, images. A Crawler can supply newly found links to request handling again.
6. Crawled data is passed to Handler objects which actually perform further processing i.e save to disk or meta data collection
7. All of this orchestrated by FetchService class which has a request queue inside and async processing of Crawlers and their handlers

# Current version and future development
Current implementation has a limited set of features but designed to be easily extensible and ready for new functionality.
I have made only simplistic versions of Crawler and Loader classes. The SimpleLoader can do only GET requests but others 
can be easily added. My approach gives an ability to use multiple growing points to develop more complex features. 
For example the framework can be used for website testing purposes if needed. Crawler class potentially can accept not only
URLs but also actions to be performed on dynamic web pages: inputs, clicks, scrolls etc. Testing scenarios can be played and 
checked using improved Crawlers. In case scaling and load balancing needed we could move request queue to separate service(RabbitMQ) and connect
multiple FetchServices and Loaders to the queue. Each instanec of FetchService can run in a separate process taking crawl
configs from a DB. Loaders could be implemented in similar manner allowing to create a bot net if Loaders and website renderers.
Since the time was limited I couldn't finish tests :(

# Usage in Docker
```
# To build
docker build -t fetch-app .
# To run:
docker run -v $(pwd):/app fetch-app:latest http://www.google.com

```