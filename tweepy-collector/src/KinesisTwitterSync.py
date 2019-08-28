from TwitterSync import TwitterSync
import boto3
import json

class KinesisTwitterSync(TwitterSync):

    stream_name = None
    kinesis_client = None
    logger = None

    def __init__(self, stream_name=None, region=None, logger=None):
        self.stream_name = stream_name
        self.kinesis_client = boto3.client('kinesis', region_name=region)
        self.logger = logger

    def persist(self,document=None):
        self.logger.info('Enviando Documento : ' + str(document))
        try:
            tweet_id = str(document['id'])
            put_response = self.kinesis_client.put_record( StreamName=self.stream_name, 
                                                            Data=json.dumps(document), 
                                                            PartitionKey=tweet_id)

            self.logger.info('Documento Enviado para Kinesis - ' + str(put_response))
            return put_response
        except Exception as e:
            error_message = "Erro Enviando Documento para Kinesis: "
            if (e, 'message'):
                error_message = error_message + str(e.message)
            else:
                error_message = error_message + str(e)

            self.logger.error(error_message)