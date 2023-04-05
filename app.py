import boto3
from dynamo import Dynamo
from telegram import Telegram
from standard import Standard
import time

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

mydb = Dynamo(dynamodb)
mytg = Telegram()


# Create table if it does not exist
table_name = "content_c"
table_exists = mydb.exists(table_name)
if not table_exists:
    mydb.create_table(table_name)

# Fetch content from standard RSS feed.
mystandard = Standard()
url = "https://www.standardmedia.co.ke/rss/sports.php"
posts = mystandard.fetch_content(url)

# Save Posts in DynamoDB.
mydb.write_batch(posts)

# get posts that are yet to be posted
new_posts = mydb.scan_new_posts()


# format and send message
# update post status
for post in new_posts:
    post_id = post['id']
    post_title = post['title']
    post_summary = post['summary']
    post_link = post['link']
    message = f"*{post_title}*\n{post_summary}\n[link]({post_link})"
    response = mytg.send_message(message)
    if response:
        mydb.update_post_status(post_id)
    time.sleep(1)
