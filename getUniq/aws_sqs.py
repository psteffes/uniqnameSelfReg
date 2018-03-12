from django.conf import settings

import boto3
import json
import logging

logger = logging.getLogger(__name__)

def add_message_to_queue(uid, email, phone):

    aws_region            = settings.AWS_REGION
    aws_access_key_id     = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    aws_queue_name        = settings.AWS_QUEUE_NAME

    sqs = boto3.resource(
        'sqs',
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    queue = sqs.get_queue_by_name(QueueName=aws_queue_name)
    
    body = {
        'uid': uid,
        'recovery_email': email,
        'recovery_phone': phone,
    }

    logger.info('Adding uid={} recovery_email={} recovery_phone={} to {}'.format(uid, email, phone, aws_queue_name))
    response = queue.send_message(
        QueueUrl=queue.url,
        DelaySeconds=10,
        MessageBody=json.dumps(body),
    )

    logger.debug('sqs_response={}'.format(response))
    return

