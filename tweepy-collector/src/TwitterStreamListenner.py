import tweepy
import json
import logging
from datetime import datetime, timedelta
from email.utils import parsedate_tz

#override tweepy.StreamListener to add logic to on_data
class TwitterStreamListenner(tweepy.StreamListener):
    sync = None
    logger = None

    def to_datetime(self, datestring):
        time_tuple = parsedate_tz(datestring.strip())
        dt = datetime(*time_tuple[:6])
        return dt - timedelta(seconds=time_tuple[-1])
    
    def __init__(self, sync, logger):
       self.sync = sync         
       self.logger = logger

    def parse_data(self, json_data=None):
        parsed_data = {}

        parsed_data['id']       = json_data['id']
        parsed_data['data']     = self.to_datetime(json_data['created_at'])
        parsed_data['usuario']  = json_data['user']

        if 'extended_tweet' in json_data:
            parsed_data['texto'] = json_data['extended_tweet']['full_text']
        else:
            parsed_data['texto'] = json_data['text']

        if 'retweeted_status' in json_data:
            parsed_data['retweeted'] = True
            parsed_data['quote_count'] = json_data['retweeted_status']['quote_count']
            parsed_data['reply_count'] = json_data['retweeted_status']['reply_count']
            parsed_data['retweet_count'] = json_data['retweeted_status']['retweet_count']
            parsed_data['favorite_count'] = json_data['retweeted_status']['favorite_count']
        else:
            parsed_data['retweeted'] = False

        if 'quoted_status' in json_data:
            parsed_data['quoted'] = True
        else:
            parsed_data['quoted'] = False
        parsed_data['location'] = json_data['user']['location']
        parsed_data['lang']     = json_data['lang']
        parsed_data['geo']      = json_data['geo']
        parsed_data['coordinates'] = json_data['coordinates']
        parsed_data['place']    = json_data['place']
        parsed_data['hashtags'] = json_data['entities']['hashtags']
        parsed_data['urls']     = json_data['entities']['urls']
        parsed_data['user_mentions'] = json_data['entities']['user_mentions']

        return parsed_data

    def on_data(self, data):
        self.logger.debug("Postagem Recebida")        
        
        try:
            parsed_data = self.parse_data(json.loads(data))  
        except Exception as e:
            error_message = ""
            if hasattr(e, 'message'):
                error_message = e.message                    
            else:
                error_message = str(e)
            
            self.logger.error('Error parsing tweet Data: {}'.format(error_message))
            self.logger.error(data)   
            return
    
        self.logger.debug(parsed_data)  
        self.sync.persist(parsed_data)        