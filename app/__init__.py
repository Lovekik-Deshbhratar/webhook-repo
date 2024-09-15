from flask import Flask

from app.webhook.routes import webhook

from app.extensions import mongo

from flask_cors import CORS




# Creating our flask app
def create_app():

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config["MONGO_URI"] = "mongodb+srv://lovekikdeshbhratar:Lovekik1234@cluster0.ioirz.mongodb.net/webhook?retryWrites=true&w=majority"
    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
