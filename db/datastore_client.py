from google.oauth2 import service_account
from google.cloud import datastore
from system import Configurator
from datetime import datetime



class DatastoreClient:
   
    def __init__(self, config: Configurator):
        self.configurator = config
        credentials = service_account.Credentials.from_service_account_file(
            self.configurator.get('gcp.service_account'),
            scopes=self.configurator.get('gcp.scopes'))
        self.datastore_client = datastore.Client(project=self.configurator.get('gcp.project'), credentials=credentials)
    
    def save_user_running(self, user_id, action):
        kind = "user_running_stat"
        created_ad = datetime.utcnow().timestamp()
        complete_key = self.datastore_client.key(kind, user_id)
        entity = datastore.Entity(key=complete_key)
        entity.update({
            'user':user_id,
            'action':action,
            'createdAt':created_ad
        })
        self.datastore_client.put(entity)

    def get_user_action(self, user_id):
        kind = "line_user_action"
        key = self.datastore_client.key(kind,user_id)
        user = self.datastore_client.get(key)

        if user is not None:
            return user['action']
    
    def remove_user_action(self,user_id):
        kind = "line_user_action"
        key = self.datastore_client.key(kind,user_id)
        self.datastore_client.delete(key)

    def save_user_travel_assistace_mode(self, user_id):
        kind = "line_user_travel_assistace"
        created_ad = datetime.utcnow().timestamp()
        complete_key = self.datastore_client.key(kind, user_id)
        entity = datastore.Entity(key=complete_key)
        self.datastore_client.put(entity)

    def get_user_travel_assistace_mode(self, user_id):
        kind = "line_user_travel_assistace"
        key = self.datastore_client.key(kind,user_id)
        user = self.datastore_client.get(key)
        return user is not None
    
    def remove_user_travel_assistace_mode(self, user_id):
        kind = "line_user_travel_assistace"
        key = self.datastore_client.key(kind,user_id)
        self.datastore_client.delete(key)





  
