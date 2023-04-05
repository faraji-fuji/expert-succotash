import boto3
import logging
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from pprint import pprint

logger = logging.getLogger(__name__)


class Dynamo:
    """Encapsulate Amazon DynamoDB table with posts data"""

    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = None

    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table
        in a member variable.

        :param table_name: The name of the table to check.
        :return: True when the table exists, otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response['Error']['Code'],
                    err.response['Error']['Message']
                )
                raise
        else:
            self.table = table
        return exists

    def create_table(self, table_name):
        """
        Creates an Amazon DynamoDB table that can be used to store posts data.
        The table uses the id of the post as the partition key and is_posted
        as the sort key.

        :param table_name: The name of the table to create.
        :return: Newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'},  # partition key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10})
            self.table.wait_until_exists()
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s", table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.table

    def list_tables(self):
        '''
        Lists Amazon DynamoDB tables for the current account.

        :return: The list of tables.
        '''
        try:
            tables = []
            for table in self.dyn_resource.tables.all():
                print(table.name)
                tables.append(table)
        except ClientError as err:
            logger.err(
                "Couldn't list tables. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return tables

    def write_batch(self, posts):
        """
        Fills an Amazon DynamoDB table with the specified data, using the Boto3
        Table.batch_writer() function to put the items in the table.
        Inside the context manager, Table.batch_writer builds a list of
        requests. On exiting the context manager, Table.batch_writer starts sending
        batches of write requests to Amazon DynamoDB and automatically
        handles chunking, buffering, and retrying.

        :param posts: The data to put in the table. Each item must contain at least
                       the keys required by the schema that was specified when the
                       table was created.
        """
        try:
            for post in posts:
                self.table.put_item(
                    Item=post,
                    ConditionExpression='attribute_not_exists(id)')
        except ClientError as err:
            # logger.error(
            #     "Couldn't load data into table %s. Here's why: %s: %s", self.table.name,
            #     err.response['Error']['Code'], err.response['Error']['Message'])
            pass

    def scan_new_posts(self):
        '''
        Get a list of new posts from the DynamoDB.

        :return: A list of new posts.
        '''
        try:
            response = self.table.scan(
                FilterExpression=Attr('is_posted').eq('false'))
        except ClientError as err:
            logger.error("Couldn't scan for new posts. Here's why: %s: %s.",
                         err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Items']

    def update_post_status(self, id):
        '''
        Update the post status of a post. Set is_posted attribute to true.

        :param id: The id of the post to update.
        '''
        try:
            response = self.table.update_item(
                Key={'id': id},
                UpdateExpression="set is_posted=:s",
                ExpressionAttributeValues={':s': 'true'})
        except ClientError as err:
            logger.error(
                "Couldn't update post in table %s. Here's why: %s: %s.",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return True
