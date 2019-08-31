import tweepy
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from parser.twitter_cloud_event_parser import TwitterEventToCloudEvent

class TwitterCloudEventListener(tweepy.StreamListener):
    sync = None
    logger = None
    
    def __init__(self, sync, logger):
       self.sync = sync         
       self.logger = logger
    
    def on_data(self, data):
        self.logger.debug("Postagem Recebida")        
        
        try:
            event_parser = TwitterEventToCloudEvent(logger=self.logger) 
            parsed_data = event_parser.parse_event(json.loads(data))  
            
            self.logger.debug(parsed_data)  
            self.sync.persist(parsed_data) 
        except Exception as e:
            error_message = ""
            if hasattr(e, 'message'):
                error_message = e.message                    
            else:
                error_message = str(e)
            
            self.logger.error('Error parsing tweet Data: {}'.format(error_message))
            self.logger.error(data)   
            return    

    def on_error(self, status_code):
        if ( ( status_code in [420, 429] ) | ( status_code >= 500)) :
            self.logger.error("Twitter Stream Error: " + str(status_code))            
            self.logger.error("Disconnecting from Twitter Stream")
            return False
        else: 
            self.logger.debug("Healing from Twitter Error. Reconnecting")   
            return True       