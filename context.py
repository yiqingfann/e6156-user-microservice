import os

def get_db_info():
    '''
        get MySQL connection info from environment variables
    '''
    
    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)
    
    db_info = {
        "host": db_host,
        "user": db_user,
        "password": db_password,
    }

    return db_info

def get_google_blueprint_info():

    google_blueprint_info = {
        "client_id": os.environ.get("GBPCLIENTID", None),
        "client_secret": os.environ.get("GBPCLIENTSECRET", None),
    }
    
    return google_blueprint_info
