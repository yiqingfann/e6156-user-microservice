import os

def get_db_info():
    '''
        get MySQL connection info from environment variables
    '''
    
    db_info = {
        "host": os.environ.get("DBHOST", None),
        "user": os.environ.get("DBUSER", None),
        "password": os.environ.get("DBPASSWORD", None),
    }

    return db_info

def get_google_blueprint_info():

    google_blueprint_info = {
        "client_id": os.environ.get("GBPCLIENTID", None),
        "client_secret": os.environ.get("GBPCLIENTSECRET", None),
    }
    
    return google_blueprint_info

def get_aws_access_key_info():

    aws_access_key_info = {
        "region_name": os.environ.get("AWSREGIONNAME", None),
        "aws_access_key_id": os.environ.get("AWSACCESSKEYID", None),
        "aws_secret_access_key": os.environ.get("AWSACCESSKEYSECRET", None)
    }

    return aws_access_key_info