import requests
import json
import pandas as pd

import flask
from flask import request, Response
app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def rootPath():
  session = requests.Session()
  allComments = session.get("https://jsonplaceholder.typicode.com/comments")
  allComments = json.loads(allComments.text)
  allCommentsDf = pd.DataFrame.from_dict(allComments).astype(str)

  commentsCol = list( allComments[0].keys() )
  for one in request.args:
    if one in commentsCol:
      print( "Found: " + one + " == " + request.args[one] )
      allCommentsDf = allCommentsDf[ allCommentsDf[one].values == request.args[one] ]
    else:
      print( "NO: " + one )

  allCommentsDf = json.dumps( json.loads(allCommentsDf.to_json(orient="records")), indent=2 )
  return Response( allCommentsDf, status=200, content_type='text/plain; charset=utf-8', mimetype='text/plain' )

app.run()

