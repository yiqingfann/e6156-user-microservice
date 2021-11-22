from collections import defaultdict
import boto3
import json

from context import get_aws_access_key_info

requests_need_to_be_notified = {
    'POST /api/users': "arn:aws:sns:us-east-2:080252012198:sns_user_created"
}

class SNSNotificationHandler():

    @classmethod
    def get_sns_client(cls):
        aws_access_key_info = get_aws_access_key_info()
        sns_client = boto3.client(
            "sns",
            region_name = aws_access_key_info["region_name"],
            aws_access_key_id = aws_access_key_info["aws_access_key_id"],
            aws_secret_access_key = aws_access_key_info["aws_secret_access_key"]
        )
        return sns_client
    
    @classmethod
    def create_sns_topic(cls, topic_name):
        sns_client = cls.get_sns_client()
        response = sns_client.create_topic(Name = topic_name)
        sns_topic_arn = response["TopicArn"]
        return sns_topic_arn
    
    @classmethod
    def get_sns_topics(cls):
        sns_client = cls.get_sns_client()
        response = sns_client.list_topics()
        topics = response["Topics"]
        return topics

    @classmethod
    def publish_sns_message(cls, sns_topic_arn, message):
        sns_client = cls.get_sns_client()
        response = sns_client.publish(
            TargetArn = sns_topic_arn,
            Message = message
        )
        print(f"Publish response = {json.dumps(response)}")

    @classmethod
    def notify_if_any(cls, request):
        sns_topic_arn = requests_need_to_be_notified.get(f"{request.method} {request.path}", None)
        if sns_topic_arn is None:
            return

        message = f"{request.method} {request.path} {request.get_json()}"
        cls.publish_sns_message(sns_topic_arn, message)
