from flask import Flask, Response, jsonify
from flask_pymongo import PyMongo
from PIL import Image

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/knowledgepitaraDB"
mongo = PyMongo(app)


@app.route("/")
def home_page():
    files = mongo.db.uploads.chunks.find()
    for k in files:
        d = [i for i in mongo.db.uploads.files.find({'_id': k['files_id']})]
        if any(d):
            filename = d[0]['filename']
            open(r"F:\lokesh\resume_script\files\{}".format(filename), 'wb').write(k['data'])
            print("filename == ", filename)
    return jsonify({"file": [i for i in files]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
