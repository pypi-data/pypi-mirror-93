import m3u8, json
from requests import get
from requests.sessions import SessionRedirectMixin

API_URL = 'https://www.parliament.vic.gov.au/video-streaming/v7/scripts/akamai_desktop.json?_=1612478772960'

class Stream(object):
    def __init__(self):
        self.__get_api_data(API_URL)

    def __get_api_data(self, url):
        self.api_data = json.loads(get(url).text)
    
    def lower_stream(self):
        return self.__get_stream('Assembly Live Broadcast - Desktop')

    def upper_stream(self):
        return self.__get_stream('Council Live Broadcast - Desktop')

    def comm_stream(self):
        return self.__get_stream('Committee Live Broadcast - Desktop')

    def __get_stream(self, title):
        for stream in self.api_data:
            if(stream['title'] == title):
                return stream

print(Stream().lower_stream)
