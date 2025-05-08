from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")

w = WorkspaceClient(host=URL, token=TOKEN)

for c in w.clusters.list():
  print(c.cluster_name)

d = w.dbutils.fs.ls('/')

for f in d:
  print(f.path)