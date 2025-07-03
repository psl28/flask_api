from api import app, db

with app.app_context():
    db.create_all()

#This code is used to creates the tables in our database. It creates tables based on what we have provided in our UserModels.
#with app.app_context() ensures that we have an application context to be active