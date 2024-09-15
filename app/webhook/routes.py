from flask import Blueprint, json, request
from datetime import datetime
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# To catch pull request data coming from github and storing required fields on moongodb
@webhook.route('/pull_request', methods=["POST"])
def pull_request():
    if request.headers['Content-Type']=='application/json':
     data=request.json
     if 'pull_request' in data:
          pull_request=data['pull_request']
          if data['action'] == 'opened':
               action = 'PULL_REQUEST_opened'
          elif data['action'] == 'closed':
               action='PULL_REQUEST_merged'
          document={
                   "request_id":pull_request.get('id'),
                   "author":pull_request.get('user',{}).get('login'),
                   "action":action,
                   "from_branch":pull_request.get('head',{}).get('ref'),
                   "to_branch":pull_request.get('base',{}).get('ref'),
                   "timestamp":datetime.utcnow()
              }
          try:
               result=mongo.db.events.insert_one(document)
               return json.dumps({'status':'success','inserted_id':str(result.inserted_id)}), 200
          except Exception as e:
              return json.dumps({'status':'error','message': str(e)}), 500
     else:
         return json.dumps({'status':'error','message':'No pull request data found'}),400
    else:
         return json.dumps({'status':'error','message':'Content-Type not supported'}),400

# To catch push data coming from github and storing required fields on moongodb
@webhook.route('/push', methods=["POST"])
def push():
    if request.headers['Content-Type']=='application/json':
         data=request.json
         if 'ref' in data and 'repository' in data:
              ref=data.get('ref','')
              branch_name=ref.split('/')[-1]
              document={
                   "request_id":data.get('after',''),
                   "author":data.get('pusher',{}).get('name',''),
                   "action":"PUSH",
                   "to_branch":branch_name,
                   "timestamp":datetime.utcnow()
              }
              try:
                result=mongo.db.events.insert_one(document)
                return json.dumps({'status':'success','inserted_id':str(result.inserted_id)}), 200
              except Exception as e:
                  return json.dumps({'status':'error','message': str(e)}), 500
         else:
              return json.dumps({'status':'error','message':'No pull request data found'}),400
    else:
         return json.dumps({'status':'error','message':'Content-Type not supported'}),400

# To display all documents stored in mongodb such as push, pull request and merged.
@webhook.route('/get_all',methods=["GET"])
def get_all():
    events = mongo.db.events.find()
    events_list = list(events)
    return json.dumps(events_list, default=str), 200