import os

path = os.path.abspath(os.curdir)

class Config:
    DEBUG = True
    USER = "itdtin"
    REPO_NAME = "coinmarketcaplistener"
    GIT_API_TOKEN = os.environ.get("GIT_API_TOKEN")
