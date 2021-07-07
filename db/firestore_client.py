from google.oauth2 import service_account
from google.cloud import firestore
from system import Configurator
from datetime import datetime
import uuid


class FirestoreClient:
   
    def __init__(self, config: Configurator):
        self.configurator = config
        credentials = service_account.Credentials.from_service_account_file(
            self.configurator.get('gcp.service_account'),
            scopes=self.configurator.get('gcp.scopes'))
        self.db = firestore.Client(project=self.configurator.get('gcp.project'), credentials=credentials)

    def save_user_running(self, user_id, distance, pace, time):
        kind = "user_running_stat"
        doc_ref = self.db.collection(u'user_running_stat').document(user_id).collection(u'stat').document(str(uuid.uuid4()))
        created_ad = datetime.utcnow().timestamp()
        doc_ref.set({
            'distance':distance,
            'pace':pace,
            'time':time,
            'createdAt':created_ad
        })

    