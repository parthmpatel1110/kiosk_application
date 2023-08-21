from flask import Flask, render_template, request, redirect, url_for, send_file, session
import csv
from datetime import datetime
import pickle
import os


app = Flask(__name__)
app.secret_key = 'volavolavolavola' 
CSV_FILE = 'feedback_data.csv'
feedback_data = {}
field_names = ['Mobile No.','time','food' , 'cleanliness', 'service']
passwordDict = {"patel" : "patel"}


def savedata(feedback_data):
    if os.path.exists('feedback_data.pkl'):
        with open('feedback_data.pkl', 'rb') as fp:
            filedata = pickle.load(fp)
        
        for key,value in feedback_data.items():
            filedata[key] = value
        
        with open('feedback_data.pkl', 'wb') as fp:
            pickle.dump(filedata, fp)
            feedback_data = {}
            # print(filedata)
    else:
        with open('feedback_data.pkl', 'wb') as fp:
            pickle.dump(feedback_data, fp)
            feedback_data = {}
    return

def loaddata():
    if os.path.exists('feedback_data.pkl'):
        with open('feedback_data.pkl', 'rb') as fp:
            filedata = pickle.load(fp)
    else:
        filedata = {}
    return filedata

@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('thank_you.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    food = request.form.get('food')
    print("food=", food)
    cleanliness = request.form.get('cleanliness')
    service = request.form.get('service')
    mobile_number = request.form.get('mobile_number')
    feedback_data.pop(mobile_number, None)
    feedback_data[mobile_number] = [mobile_number,datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,  food, cleanliness, service]
    savedata(feedback_data)
    return render_template('thank_you.html')

@app.route('/view_feedback', methods=['GET', 'POST'])
def view_feedback():
    if request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('username')
        if username in passwordDict:
            if password == passwordDict[username]:
                session['download_initiated'] = True
                feedback_data = loaddata()
                
                food = [0,0]
                CLEANLINESS = [0,0]
                SERVICE = [0,0]
                for key,val in feedback_data.items():
                    if(val[2] == "thumbs_up"):
                        food[0] = food[0] + 1
                    elif(val[2] == "thumbs_down"):
                        food[1] = food[1] + 1

                    if(val[4] == "thumbs_up"):
                        SERVICE[0] = SERVICE[0] + 1
                    elif(val[4] == "thumbs_down"):
                        SERVICE[1] = SERVICE[1] + 1

                    if(val[3] == "thumbs_up"):
                        CLEANLINESS[0] = CLEANLINESS[0] + 1
                    elif(val[3] == "thumbs_down"):
                        CLEANLINESS[1] = CLEANLINESS[1] + 1
              
                labels = ["thumbs_up","thumbs_down"]
 
                return render_template(
                    template_name_or_list='view_feedback.html',
                    fooddata=food,
                    labels=labels,
                    cleaninessdata=CLEANLINESS,
                    servicedata = SERVICE
                )
    return render_template('password_prompt.html')

@app.route('/download_feedback_csv')
def download_csv():
    if 'download_initiated' in session and session['download_initiated']:
        feedback_data = loaddata()
        with open(CSV_FILE, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Mobile Number', 'Timestamp', 'Food', 'CLEANLINESS', 'SERVICE'])
            for mobile_number, data in feedback_data.items():
                writer.writerow([data[0],data[1],data[2],data[3],data[4]])
        return send_file(CSV_FILE, as_attachment=True)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    # app.run(port=3000, debug=True)
    app.run()