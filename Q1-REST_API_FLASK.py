import requests
import json
import pandas as pd

import flask
from flask import Response
app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def rootPath():
  session = requests.Session()
  allComments = session.get("https://jsonplaceholder.typicode.com/comments")
  allPosts = session.get("https://jsonplaceholder.typicode.com/posts")

  allComments = json.loads(allComments.text)
  allPosts = json.loads(allPosts.text)

  allComments = pd.DataFrame.from_dict(allComments)
  allPosts = pd.DataFrame.from_dict(allPosts)
  allPosts.rename(columns={'id':'postId'}, inplace=True)

  allComments_SUM = allComments.groupby(['postId']).size()
  allComments_SUM = pd.DataFrame({'postId':allComments_SUM.index, 'total_number_of_comments':allComments_SUM.values})
  
  TopPosts = pd.merge( allPosts, allComments_SUM, on="postId")
  TopPosts.drop("userId", axis=1, inplace=True)
  TopPosts.rename(columns={'postId':'post_id'}, inplace=True)
  TopPosts.rename(columns={'title':'post_title'}, inplace=True)
  TopPosts.rename(columns={'body':'post_body'}, inplace=True)
  TopPosts.sort_values("total_number_of_comments", ascending=False, inplace=True, kind="mergesort")

  result = json.dumps( json.loads(TopPosts.to_json(orient="records")), indent=2 )

  return Response( result, status=200, content_type='text/plain; charset=utf-8', mimetype='text/plain' )

app.run()

