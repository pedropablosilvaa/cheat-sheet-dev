from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")

w = WorkspaceClient(host=URL, token=TOKEN)

c_id = input('ID of cluster to delete (for example, 1234-567890-ab123cd4): ')

w.clusters.permanent_delete(cluster_id = c_id)