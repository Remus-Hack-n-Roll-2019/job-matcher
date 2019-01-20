import os
from flask import *
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from PDFHandler import *
from job_search.main import *
from json import *

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER)
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)

    text = pdfparser(os.path.join('static', filename))
    keywords = extract_keywords(text)
    listOfRequests = []
    for keyword in keywords:
        listOfRequests.append({ "keyword": keyword, "location": "singapore" })

    joblist = queryJobs(listOfRequests)
    joblist = matchKeywords(keywords, joblist)
    # with open("json/aadit.json") as f:
    #     joblist = json.load(f)['joblist']
    # with open("json/aadit.json", 'w') as outfile:
    #     json.dump({'joblist': joblist, 'keywords': keywords}, outfile)
    # for job in joblist:
    #     print(job['job_title'])
    #     print()
    return jsonify({'joblist': joblist, 'keywords': keywords})

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

CORS(app, expose_headers='Authorization')
