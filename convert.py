import json

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
import ast
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

## 次


f = open("result.txt", "r")
client = language.LanguageServiceClient()
name = True
numcount = 0
while 1:
    line = f.readline()
    if name:
        print(line)
        name = False
    else:
        hi = ast.literal_eval(line)
        total_sentiment_score = 0
        total_reviewers = 0
        for review in hi['reviews']:
            print(review['reviewer'])
            if review['text']:
                total_reviewers = total_reviewers + 1
                document = types.Document(
                            content=review['text'],
                            type=enums.Document.Type.PLAIN_TEXT)
                sentiment = client.analyze_sentiment(document=document).document_sentiment
                total_sentiment_score = total_sentiment_score + sentiment.score
        print(f"total reviews: {total_reviewers}")
        if not total_reviewers == 0:
            print(f"total score: {total_sentiment_score}")
            print(f"average score: {total_sentiment_score/total_reviewers}")
        print('------------------------------------')
        name = True
    if not line:
        break
    pass # do something

