from .twitter_sync import TwitterSync
from pymongo import MongoClient
from urllib.parse import quote_plus
import logging

class MongoTwitterSync(TwitterSync):    
	database = None
	collection = None
	logger = None

	def __init__(self, host, port, database, logger=None, user=None, password=None, collection=None ):
		self.logger = logger
		if  ( user is None ) | (password is None) | ( (user == "") & (password == "") ) :          
			uri = "mongodb://%s:%s" % (host, port)
		else:    
			uri = "mongodb+srv://%s:%s@%s" % (quote_plus(user), quote_plus(password), host)

		print(uri)

		client = MongoClient(uri)
		self.database   = client[database]
		self.collection = collection
            
	def persist(self,document):        
		self.logger.debug('Inserindo Documento : ' + str(document))        
		try:
			document_id = self.database[self.collection].insert_one(document).inserted_id
			self.logger.info('Documento Persistido - ' + str(document_id))
			return document_id
		except Exception as e:
			error_message = "Erro persistindo Documento: "

			if (e, 'message'):
				error_message = error_message + str(e.message)
			else:
				error_message = error_message + str(e)

			self.logger.error(error_message)