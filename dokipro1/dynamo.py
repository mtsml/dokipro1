import os
import boto3
import dokipro1.const as const


def conn_dynamodb(table_nm):
    session = boto3.session.Session(
        region_name=const.AWS_REGION,
        aws_access_key_id=const.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=const.AWS_SECRET_ACCESS_KEY
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table_nm)

    return table


def set_user_info(items):
    table = conn_dynamodb(const.AWS_DYNAMO_TABLE_NM)

    response = table.put_item(
            Item=items
        )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Error: ', response)
    else:
        print('Successed: ', items['user_id'])


def del_user_info(key):
    table = conn_dynamodb(const.AWS_DYNAMO_TABLE_NM)

    response = table.delete_item(
            Key=key
        )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Error: ', response)
    else:
        print('Successed: ', key['user_id'])


def upd_user_info(key, point, timestamp):
    table = conn_dynamodb(const.AWS_DYNAMO_TABLE_NM)

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


def upd_display_name(key, display_name):
    table = conn_dynamodb(const.AWS_DYNAMO_TABLE_NM)

    response = table.update_item(
        Key=key,
        UpdateExpression="set display_name = :d",
        ExpressionAttributeValues={ 
            ':c': display_name
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Error: ', response)
    else:
        print('Successed: ', key['user_id'])


def get_user_info_all():
    table = conn_dynamodb(const.AWS_DYNAMO_TABLE_NM)

    response = table.scan()

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Error: ', response)
    else:
        print('Successed: ', response['Items'])
        return response['Items']