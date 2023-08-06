from decouple import config
from wcfmclient.session import session

options = {
    "username": config("username"),
    "password": config("password"),
    "url": config("url"),
    "session": session
}
