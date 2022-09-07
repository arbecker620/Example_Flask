from flask import Flask
from flask import Flask, request, jsonify

app = Flask(__name__)

import os 
import pymongo
from pymongo import MongoClient

client = MongoClient("mongo:27017")

db = client.test
storage = db.storage


def database_new_entry(new_result):
    global storage
    if storage.find({'Name':new_result['Name']}).count() > 0:
        availability_flag= True
    student_details = {
        'Name': new_result['Name'], 
        'grds': new_result
    }

    entry_status = storage.insert_one(student_details)
    return entry_status

def database_update_entry(key_val,new_result):
    global storage
    entry_status = storage.update_one(
    {'Name':key_val},
            {
            "$set": {'grds':new_result}
            }
        )
    print('inside database_update_entry', key_val, new_result)
    return entry_status
data = {}

@app.route('/')
def hello():
    return "hello world" 
    return jsonify({"message":"hello world"})

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        print(result)
        print(result['Name'])
        global data
        if storage.find({'Name': result['Name']}).count()>0:
            availability_flag=True
            Queryresult = storage.find_one({'Name': result['Name']})
            pass_dict = Queryresult['grds']
        else:
            availability_flag=False

        if avaliability_flag==False: #not (result['Name'] in data.keys()):
            data[result['Name'] ]=result
            print('data',data)
            print("result['Name']",data[result['Name']])
            entry_status=database_new_entry(result)
            return render_template("result.html",result = result)
        else:
            return jsonify({"edit": "it was amazing"})


@app.route('/whatever',methods = ['POST', 'GET'])
def whatever():

    return jsonify({"string": "whatever"})






if __name__ == '__main__':
    app.run(debug = True)