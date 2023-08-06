import os

from google.cloud import bigquery
from google.oauth2 import service_account

SA_BQ = os.environ.get("NWK_FIN_PATH")
PROJECT_ID = "edm-network-development"


def initalize_bq_client() -> bigquery.Client:
    credentials = service_account.Credentials.from_service_account_file(SA_BQ)
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    return client
