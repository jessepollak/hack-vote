import os
from flask import Flask, request, redirect, g, render_template, jsonify
import twilio.twiml

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)

numbers = set()
projects = []

@app.route('/')
def index():
    return render_template('index.html', projects=projects)

@app.route('/list')
def list():
    return jsonify(projects=projects)

app.route('/vote')
def vote():
    from_number = request.args.get('From', None)
    # number exists
    if from_number in numbers:
        resp = twilio.twiml.Response()
        resp.sms('Thanks, but you already voted!') 
    else:
        try:
            ident = int(request.args.get('Body', ''))
            projects[ident]['votes'] += 1
            numbers.add(from_number)
            resp = twilio.twiml.Response()
            resp.sms('Thanks for the vote!') 
        except (ValueError, IndexError):
            resp = twilio.twiml.Response()
            resp.sms("That isn't a valid project id.") 

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
