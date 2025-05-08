import time
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")

w = WorkspaceClient(host=URL, token=TOKEN)

me = w.current_user.me()

print(me)