import tweepy
import json
import logging
import argparse
#from MongoTwitterSync import MongoTwitterSync   
from KinesisTwitterSync import KinesisTwitterSync     
from TwitterStreamListenner import TwitterStreamListenner
import os


def config_parser():
    parser = argparse.ArgumentParser(description='Coletor de Dados do Twitter')

    parser.add_argument('config', type=str, 
                        help='Path do arquivo de configuracoes')
    
    return parser.parse_args()


def get_application_environment():
    return os.environ['APPLICATION_ENVIRONMENT']

# helper que configura a autenticação da api do Twitter
def config_twitter_api():
    api = None
    try:
        auth1 = tweepy.auth.OAuthHandler(os.environ['TWITTER_CONSUMER_TOKEN'], 
                                         os.environ['TWITTER_CONSUMER_SECRET'])
        auth1.set_access_token( os.environ['TWITTER_API_KEY'] ,
                                os.environ['TWITTER_API_SECRET'] )
        api = tweepy.API(auth1)
        logger.info("Twitter API Conectada com Sucesso")
    except Exception as e:
        if hasattr(e, 'message'):
            logger.error("Erro ao configurar Twitter API: " + str(e.message) )
        else:
            logger.error("Erro ao configurar Twitter API: " + str(e))
    finally:    
        return api



# helper que configura o client do Mongodb
def config_mongo_sync(config):
    mongo_sync = None
    try:
        mongo_sync = MongoTwitterSync(host=config['MONGODB']['MONGODB_URI'],
                                    port=config['MONGODB']['MONGODB_PORT'],
                                    database=config['MONGODB']['MONGODB_DATABASE'],
                                    logger=logger,
                                    user=config['MONGODB']['MONGODB_USER'],
                                    password=config['MONGODB']['MONGODB_PASSWORD'],
                                    collection=config['MONGODB']['MONGODB_COLLECTION'])                                  
        logger.info("MongoDB Conectado com sucesso")                            
    except Exception as e:
        logger.error("Erro ao conectar ao Mongo: " + str(e) )
    finally:
        return mongo_sync


def config_kinesis_sync(config):
    kinesis_sync = None
    try:
        kinesis_sync = KinesisTwitterSync(stream_name='twitter_data_landing_stream', region='us-east-2', logger=logger)
        logger.info("Kinesis Configurado com sucesso")                            
    except Exception as e:
        logger.error("Erro ao conectar ao Kinesis: " + str(e) )
    finally:
        return kinesis_sync

# helper que configura o logger da aplicação
def config_log(config):    
    # create logger
    logger = logging.getLogger('posts_collector')
    logger.setLevel(config['LOG']['LOG_LEVEL'])
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(config['LOG']['LOG_LEVEL'])
    # create formatter
    formatter = logging.Formatter(config['LOG']['LOG_FORMAT'])
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

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
    logger = config_log(config)
    # configura a api do Twitter 
    auth   = config_twitter_api()
    #mongo_sync = config_mongo_sync(config) 
    kinesis_sync = config_kinesis_sync(config)   

    #listener = TwitterStreamListenner(sync=mongo_sync, logger=logger)
    listener = TwitterStreamListenner(sync=kinesis_sync, logger=logger)
    searchStream = tweepy.Stream(auth=auth.auth, listener=listener)    

    query_string = config['SEARCH']['STRING']
    searchStream.filter(track=query_string, languages=['pt'])  
