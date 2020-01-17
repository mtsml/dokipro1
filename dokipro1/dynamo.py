import os
import boto3


# AWS
AWS_REGION = 'ap-northeast-1'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_DYNAMO_TABLE_NM = 'dokipro1'


def conn_dynamodb(table_nm):
    session = boto3.session.Session(
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table_nm)

    return table


def set_user_info(items):
    table = conn_dynamodb(AWS_DYNAMO_TABLE_NM)

    response = table.put_item(
            Item=items
        )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Error: ', response)
    else:
        print('Successed: ', items['user_id'])


def del_user_info(key):
    table = conn_dynamodb(AWS_DYNAMO_TABLE_NM)

    response = table.delete_item(
            Key=key
        )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Error: ', response)
    else:
        print('Successed: ', key['user_id'])


def upd_user_info(key, point, timestamp):
    table = conn_dynamodb(AWS_DYNAMO_TABLE_NM)

    response = table.update_item(
        Key=key,
        UpdateExpression="set message_count = message_count + :c, love_point = love_point + :p, last_datetime = :d",
        ExpressionAttributeValues={ 
            ':c': 1,
            ':p': point,
            ':d': timestamp
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Error: ', response)
    else:
        print('Successed: ', key['user_id'])


def get_user_info_all():
    table = conn_dynamodb(AWS_DYNAMO_TABLE_NM)

    response = table.scan()

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Error: ', response)
    else:
        print('Successed: ', response['Items'])
        return response['Items']