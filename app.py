# from flask import Flask, render_template, redirect, url_for
# #https://medium.com/@nikovrdoljak/deploy-your-flask-app-on-azure-in-3-easy-steps-b2fe388a589e
# app=Flask(__name__)

# @app.route('/')
# def welcome():
#   return render_template("test.html")

# @app.route('/success/<int:score>')
# def success(score):
#   return "The person has passed and score is {}".format(str(score));

# if __name__ == '__main__':
#   app.run()
#FLASK_APP=app.py flask run
from flask import Flask,render_template,Response
import cv2
import mediapipe as mp
app=Flask(__name__)
cap=cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def generate_frames(picture):
    while True:

        ## read the camera frame
        success,img=cap.read()
        if not success:
            break
        else:
          imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          results = hands.process(imgRGB)
          if results.multi_hand_landmarks:
            print(results.multi_hand_landmarks)
            for handLms in results.multi_hand_landmarks:
              mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
              if not picture:
                  yield(mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS))
          ret,buffer=cv2.imencode('.jpg',img)
          img=buffer.tobytes()
        if picture :
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')



@app.route('/')
def index():
    return render_template('test.html')

@app.route('/video')
def video():
    return Response(generate_frames(True),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/text')
def text():
    return Response(generate_frames(False),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)