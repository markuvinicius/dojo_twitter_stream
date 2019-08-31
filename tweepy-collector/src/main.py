#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import json
import logging
import argparse

from sync.kinesis_twitter_sync import KinesisTwitterSync
from listener.twitter_stream_listener import TwitterStreamListener
from listener.twitter_cloud_event_listener import TwitterCloudEventListener
import os


def config_parser():
    parser = argparse.ArgumentParser(description='Coletor de Dados do Twitter')
    parser.add_argument('config', type=str, 
                                    help='Path do arquivo de configuracoes')
    
    return parser.parse_args()

def get_application_environment():
    return os.environ['APPLICATION_ENVIRONMENT']

# helper que instancia e autentica a api do twitter via Tweepy
def config_twitter_api():
    api = None
    try:
        credentials = tweepy.auth.OAuthHandler(os.environ['TWITTER_CONSUMER_TOKEN'], 
                                         os.environ['TWITTER_CONSUMER_SECRET'])
        credentials.set_access_token( os.environ['TWITTER_API_KEY'] ,
                                os.environ['TWITTER_API_SECRET'] )
        api = tweepy.API(credentials)
        logger.info("Twitter API Conectada com Sucesso")
    except Exception as e:
        if hasattr(e, 'message'):
            logger.error("Erro ao configurar Twitter API: " + str(e.message) )
        else:
            logger.error("Erro ao configurar Twitter API: " + str(e))
    finally:    
        return api

# helper que configura o client do AWS Kinesis
def config_kinesis_sync(config):
    kinesis_sync = None
    try:
        kinesis_sync = KinesisTwitterSync(stream_name=config['KINESIS']['STREAM_NAME'], 
                                            region=config['KINESIS']['AWS_REGION'], 
                                            logger=logger)
        logger.info("Kinesis Configurado com sucesso")                            
    except Exception as e:
        logger.error("Erro ao conectar ao Kinesis: " + str(e) )
    finally:
        return kinesis_sync

# helper que configura o logger da aplicação
def config_log(config):    
    
    logger = logging.getLogger('posts_collector')
    logger.setLevel(config['LOG']['LOG_LEVEL'])

    console_handler = logging.StreamHandler()
    console_handler.setLevel(config['LOG']['LOG_LEVEL'])

    log_formatter = logging.Formatter(config['LOG']['LOG_FORMAT'])
    console_handler.setFormatter(log_formatter)

    logger.addHandler(console_handler)

    return logger
    

# helper que faz a leitura do arquivo de configurações
def read_config(config_file, env="LOCAL"):
    content = {}
    try:
        with open(config_file, 'r') as f:
            content = json.load(f)
    except Exception as e:
        error_message="Erro lendo arquivo de configurações): "
        if hasattr(e , 'message'):
            error_message = error_message + e.message
        else:
            error_message = error_message + str(e)

        print(error_message)
        exit(1)

    return content[env]

#main collector execution
if __name__ == "__main__":   
    args   = config_parser() 

    # loga os parametros da linha de comando    
    app_env = get_application_environment()
    print("CONFIG_FILE    : " + args.config)
    print("APP_ENVIRONMENT: " + app_env)

    if app_env is not None and app_env != "":
        config = read_config(config_file=args.config, env=app_env)
    else:
        config = read_config(config_file=args.config)

    # configura o logger
    try:
        logger = config_log(config)    
        authentication   = config_twitter_api()
        kinesis_sync = config_kinesis_sync(config)   
        
        #listener = TwitterStreamListener( sync=kinesis_sync, logger=logger)
        listener = TwitterCloudEventListener( sync=kinesis_sync, logger=logger)
        searchStream = tweepy.Stream(auth=authentication.auth, listener=listener)    

        query_string = config['SEARCH']['STRING']
        logger.info("QUERY STRING: " + str(query_string))
        searchStream.filter(track=query_string, languages=['pt'])  
    except InterruptedError as e:
        logger.debug("Interrompendo aplicação. ")
        exit(0)            
    except Exception as e:
        error_message = "Erro Genérico. "
        
        if hasattr(e , 'message'):
            error_message = error_message + e.message
        else:
            error_message = error_message + str(e)

        logger.error(error_message)
        exit(1)
