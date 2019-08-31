#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .event_parser import EventParser
import io

from cloudevents.sdk.event import v01

class TwitterEventToCloudEvent(EventParser):    

    logger = None

    def __init__(self, logger=None):
        self.logger = logger
    
    def extract_twitter_data(self, event=None):
        parsed_data = {}

        try:
            parsed_data['id']       = str(event['id'])
            parsed_data['data']     = str(event['created_at'])
            parsed_data['usuario']  = str(event['user'])

            if 'extended_tweet' in event:
                parsed_data['texto'] = str(event['extended_tweet']['full_text'])
            else:
                parsed_data['texto'] = str(event['text'])

            if 'retweeted_status' in event:
                parsed_data['retweeted'] = True
                parsed_data['quote_count'] = str(event['retweeted_status']['quote_count'])
                parsed_data['reply_count'] = str(event['retweeted_status']['reply_count'])
                parsed_data['retweet_count'] = str(event['retweeted_status']['retweet_count'])
                parsed_data['favorite_count'] = str(event['retweeted_status']['favorite_count'])
            else:
                parsed_data['retweeted'] = False

            if 'quoted_status' in event:
                parsed_data['quoted'] = True
            else:
                parsed_data['quoted'] = False

            parsed_data['location'] = str(event['user']['location'])
            parsed_data['lang']     = str(event['lang'])
            parsed_data['geo']      = str(event['geo'])
            parsed_data['coordinates'] = str(event['coordinates'])
            parsed_data['place']    = str(event['place'])
            parsed_data['hashtags'] = str(event['entities']['hashtags'])
            parsed_data['urls']     = str(event['entities']['urls'])
            parsed_data['user_mentions'] = str(event['entities']['user_mentions'])

        except Exception as e:
            error_message = 'Erro parseando twitter. '
            
            if hasattr(e , 'message'):
                error_message = error_message + e.message
            else:
                error_message = error_message + str(e)

            logger.error(error_message)
            exit(1)

        return parsed_data

    def cloud_event(self,event_body=None):
        event = (
            v01.Event().
            SetContentType("application/json").
            SetData(event_body).
            SetEventID("my-id").
            SetSource("from-galaxy-far-far-away").
            SetEventTime("tomorrow").
            SetEventType("cloudevent.greet.you")
        )
        self.logger.debug("CloudEvent: " + str(event))
        return event

    def parse_event(self,event=None):
        data = self.extract_twitter_data(event)
        return self.cloud_event(event_body=data)