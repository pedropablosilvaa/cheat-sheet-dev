from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")

w = WorkspaceClient(host=URL, token=TOKEN)

print("Attempting to create cluster. Please wait...")

c = w.clusters.create_and_wait(
  cluster_name             = 'my-cluster-2-delete',
  spark_version            = '12.2.x-scala2.12',
  node_type_id             = 'Standard_D3_v2',
  autotermination_minutes = 15,
  num_workers              = 1
)

print(f"The cluster is now ready at " \
      f"{w.config.host}#setting/clusters/{c.cluster_id}/configuration\n")