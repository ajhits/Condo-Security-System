from flask import Flask, render_template, Response, session
from Database.database import createRegister,createHistory,deleteRegistered,readHistory,deleteHistory
# import RPi.GPIO as GPIO
import cv2
import time
import os
#fingerprint
import time
import shutil
import threading

# from pyfingerprint.pyfingerprint import PyFingerprint

# # Initialize the fingerprint sensor
# fingerprint = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

import random
import string
import time

OTP_EXPIRATION_SECONDS = 60

# papalitan nlang po index dito
cctv_feedsa = 2
camera_regface = 0


def setup():
    # Check if the fingerprint sensor is found
    # if not fingerprint.verifyPassword():
    #     print("Fingerprint sensor not found!")
    #     return False

    print("Place finger on the sensor to enroll or verify...")
    return True
#LOCK
# Set up GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

# GPIO.setup(21, GPIO.OUT)	#lock
# GPIO.setup(12, GPIO.OUT)  # For controlling GPIO 12 (Buzzer)

# # TRIGGER
# GPIO.setup(17, GPIO.OUT)

# # ECHO
# GPIO.setup(27, GPIO.IN)


from flask import Flask, render_template,Response,jsonify,request,redirect,url_for
from Jojo_loRecognition.Face_Recognition import Face_Recognition as Jolo

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.debug = True  # Enable debug mode

# LOCK
@app.route('/high')
def set_high():
    # GPIO.output(21, GPIO.HIGH)
    return render_template('Admin/index.html')

#LOCK
@app.route('/low')
def set_low():
    # GPIO.output(21, GPIO.LOW)
    return render_template('Admin/index.html')

@app.route('/unlock', methods=["GET"])
def unlock():
    # import time
    # GPIO.output(21, GPIO.LOW)
    # time.sleep(3)
    # GPIO.output(21, GPIO.HIGH)
    return jsonify('Unlocked')

@app.route('/on')
def buzzer_on():
    # GPIO.output(12, GPIO.HIGH)
    return render_template('Admin/index.html')
@app.route('/off')
def buzzer_off():
    # GPIO.output(12, GPIO.LOW)
    return render_template('Admin/index.html')

@app.route("/alert", methods=['GET'])
def alarm():
    
    # # TRIGGER
    # GPIO.output(17,False)
    # time.sleep(0.5)
    # GPIO.output(17,True)
    # time.sleep(0.00001)
    # GPIO.output(17,False)
    
    # # ECHO
    # pulse_start,pulse_end = 0,0
    # while GPIO.input(27) == 0:
    #     pulse_start = time.time()
        
    # while GPIO.input(27) == 1:
    #     pulse_end = time.time()
        
    # distance = (pulse_end-pulse_start) * 17150
    # inches = round(distance / 2.54, 1)
    
    
    # print("sonar test: ",inches)
    
    # if inches > 10.0:
    #     GPIO.output(12,GPIO.HIGH)

        
    #     return jsonify(
    #         {
    #             'message': "Force Entry!",
    #             'warning': True
    #         },200)
    
    # GPIO.output(12,GPIO.LOW)
    # return jsonify(
    #         {
    #             'message': "No worry ",
    #             'warning': False
    #         },200)
    return jsonify(
            {
                'message': "No worry ",
                'warning': False
            },200)

@app.route('/enroll', methods=["GET"])
def enroll():
    # # Wait for a finger to be detected
    # while not fingerprint.readImage():
    #     pass

    # # Convert the fingerprint image into a template
    # fingerprint.convertImage(0x01)

    # # Store the template on the next available ID
    # position = fingerprint.storeTemplate()
    # if position != -1:
    #     print("Fingerprint enrolled successfully at position", position)
    #     return jsonify("Fingerprint Enrolled Succesfully")
    # else:
    #     print("Failed to store fingerprint template")
    #     return jsonify("Fingerprint Not Enrolled")
    
    return jsonify("Fingerprint Enrolled Succesfully")
    
@app.route('/verifys', methods=["GET"])
def verifys():
    # import time
    # # Wait for a finger to be detected
    # while not fingerprint.readImage():
    #     pass

    # # Convert the fingerprint image into a template
    # fingerprint.convertImage(0x01)

    # # Search the template in the database
    # position = fingerprint.searchTemplate()
    # if position[0] >= 0:
    #     print("Fingerprint verified! Match found at position", position[0])
    #     GPIO.output(21, GPIO.LOW)
    #     time.sleep(3)
    #     return jsonify("Fingerprint Verified!")
    # else:
    #     print("Fingerprint not verified! No match found")
    #     return jsonify("Fingerprint Not Verified!")
    
    return jsonify("Fingerprint Verified!")

   # time.sleep(2)  # Delay before attempting to read the next fingerprint
#OTP
def generate_otp(length=6):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/otp')
def otp():
    current_time = time.time()

    if 'otp' not in session or 'otp_expiration' not in session or current_time > session['otp_expiration']:
        session['otp'] = generate_otp()
        session['otp_expiration'] = current_time + OTP_EXPIRATION_SECONDS
        session.modified = True


        remaining_time = session['otp_expiration'] - current_time
        return render_template('otp.html', otp=session['otp'], remaining_time=int(remaining_time))
        

# homepage =========================================== #
@app.route('/')
def index():
    # GPIO.output(21, GPIO.HIGH)
    return render_template('index.html')
    

# homepage =========================================== #
@app.route('/opt')
def opt():
    return render_template('otp.html')

# facial Login =========================================== #
@app.route('/facial_login')
def facial_login():
    return render_template('face-login.html')

# ------------------- Load camera
@app.route('/video_feed')
def video_feed():
    
    # load a camera,face detection
    camera = cv2.VideoCapture(camera_regface)
    face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


    return Response(facialDetection(camera=camera, face_detector=face_detection), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')

# ------------------- door camera
@app.route('/door_feed')
def door_feed():
    
    # load a camera,face detection
    camera = cv2.VideoCapture(camera_regface)
    return Response(doorFeed(camera=camera), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')

# ------------------- cctv2 camera
@app.route('/indoor_feed')
def indoor_feed():
    
    # palitan ng index
    camera_2 = cv2.VideoCapture(1)
    return Response(get_frame2(camera2=camera_2), mimetype='multipart/x-mixed-replace; boundary=frame')
# cctv_feed
def get_frame2(camera2):
    while True:
        success, frame = camera2.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def doorFeed(camera=None):
 
    while True:
        
        # Capture a frame from the camera
        ret, frame = camera.read()
        
        if not ret:
            break

        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')

# ------------------- Facial recognition Function
Text = "Initializing"
Name = ""
def facialDetection(camera=None, face_detector=None):
    global Text,Name
    Name=""
    Text=""
    percentage=""
    B , G , R = (0,255,255)

    
    textResult = ""
    
    # Login Attempt
    success = 0
    fail = 0                                    
    
    # Initialize the timer and the start time
    timer = 0
    start_time = time.time()
    
    while True:
        
        # Capture a frame from the camera
        ret, frame = camera.read()
        
        if not ret:
            break

        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
   
        # # checking detecting face should be 1
        # if len(faces) == 1:
        #          = faces[0]
        for (x, y, w, h) in faces:
                            
            # Check if 2 seconds have elapsed since the last send
            if timer >= 2:
                       
                # facial comparison 
                response = Jolo().Face_Compare(face=frame)
                
                try:
                    textResult = response[0]

                    if "No match detected" == response[0]:
                        fail+=1
                        B, G, R = (0, 0, 255)
                        textResult = response[0]
                        if fail == 7:
                            Text = "Access Denied"
                        
    
                        # percentage = "{:.2f}%".format(response[1])
                    else:
                        B, G, R = (0, 255, 0)
                        Name=response[0]
                        textResult = response[0]
                        Text = "Access Granted"
                        
                    # every 2 seconds display threshold value
                    percentage = "{:.2f}%".format(response[1])
                    
                except:
                    pass
                
                # Reset the timer and the start time
                timer = 0
                start_time = time.time()
            else:
                # Increment the timer by the elapsed time since the last send
                timer += time.time() - start_time
                start_time = time.time()
                
            # Get the coordinates of the face,draw rectangele and put text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (B,G,R), 2)
            cv2.putText(frame,textResult,(x,y+h+30),cv2.FONT_HERSHEY_COMPLEX,1,(B,G,R),1)

            # display percentage and calculate percentages face
            if textResult == "No match detected" or textResult == "":
                percentage = "{:.2f}%".format(400 * (w * h) / (frame.shape[0] * frame.shape[1]))
            cv2.putText(frame, percentage, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (B,G,R), 2)


        # elif len(faces) > 1:
            
        #     # If more than 1 faces 
        #     # B, G, R = (0, 0, 255)
        #     Text = "More than  face is detected"
        # else:
        #     # B, G, R = (0, 0, 0)
        #     Text = "No face is detected"    
            
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')
        
# ********************* API route Facial Recognition Result
@app.route("/GET_FacialResult", methods=["GET"])
def GET_FacialResult():
    return jsonify(Text) 

# # Finger or OTP Login ===========================================
# @app.route('/finger_otp')
# def finger_otp():
#     return render_template('fingeropt.html')

# Login as Admin =========================================== #
@app.route('/admin_login')
def admin_login():
    return render_template('login.html')

# Admin Page =========================================== #
# ------------------- Dashboard
@app.route('/admin')
def admin():
    return render_template('Admin/index.html')

@app.route('/fingerotp')
def fingerotp():
    return render_template('fingeropt.html')

@app.route('/finger')
def finger():
    return render_template('finger-login.html')

# ------------------- Controls
@app.route('/admin/Controls')
def control():
    return render_template('Admin/controls.html')
#CCTV
def generate_frames():
    cctv = cv2.VideoCapture('rtsp://admin:REEBullets007@192.168.1.18/live/ch2')
# Set camera resolution
    cctv.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cctv.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    while True:
        success, frame = cctv.read()  # Read the video stream
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Generate frame bytes for streaming

@app.route('/cctv_feed')
def cctv_feed():
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Stream the frames


# ------------------- Historic Data
@app.route('/admin/Historic')
def historic():
    result=readHistory()
    return render_template('Admin/historic.html',data=result)

# ------------------- Register
@app.route('/admin/register')
def register():
    return render_template('Admin/register.html')

# ------------------- Family Name Register
@app.route('/admin/Name_Family')
def nameFamily():
    return render_template('Admin/family-name-reg.html')


# =====================  route for registered faces
path = f"Jojo_loRecognition/Registered-Faces/"

# ********************* API for submit 
@app.route('/submit_family', methods=['POST'])
def submit_family():
    global path
    
    # print(str(request.form.get('fullname')))
    # return jsonify({ "message": "goods" })

    # Define the path to the folder you want to create
    path = f"Jojo_loRecognition/Registered-Faces/{str(request.form.get('fullname'))}"
    
    # delete the foldfer path
    shutil.rmtree(path)
            
    # create new path
    os.makedirs(path)
    
    return redirect(url_for('Finger_register'))

    # if os.path.exists(path):
        
    #     if createRegister(name=str(request.form.get('fullname')),type="Family") == "Data inserted successfully!":
        
    #         # delete the foldfer path
    #         shutil.rmtree(path)
            
        
    #         # create new path
    #         os.makedirs(path)
    #         return redirect(url_for('Finger_register'))
        
    # else:
    #     if createRegister(name=str(request.form.get('fullname')),type="Family") == "Data inserted successfully!":
    #         os.makedirs(path)
    #         # route to facial registration
    #         return redirect(url_for('Finger_register'))

@app.route('/submit_guest', methods=['POST'])
def submit_guest():
    global path
    
    # print(str(request.form.get('fullname')))
    # return jsonify({ "message": "goods" })

    # Define the path to the folder you want to create
    path = f"Jojo_loRecognition/Registered-Faces/{str(request.form.get('fullname'))}"
    
    # Check if the folder already exists
    if os.path.exists(path):
        return jsonify({'error': f"Folder {path} already exists"}), 400
    else:
        if createRegister(name=str(request.form.get('fullname')),type="Guest") == "Data inserted successfully!":
            os.makedirs(path)
            # route to facial registration
            return redirect(url_for('Finger_register'))

# ------------------- Guest Name Register
@app.route('/admin/Name_Guest')
def nameGuest():
    return render_template('Admin/guest-name-reg.html')
@app.route('/admin/cam')
def cam():
    return render_template('Admin/cam.html')

# ------------------- Finger Register
@app.route('/admin/Finger_register')
def Finger_register():
    return render_template('Admin/finger-register.html')

# ------------------- Facial Register
@app.route('/admin/Facial_Register')
def Facial_Register():
    return render_template('Admin/face-register.html')

# load facial detection

result = "capturing..."

@app.route('/facial_register')
def facial_register():
    
     # load a camera,face detection
    camera = cv2.VideoCapture(camera_regface)
    face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    return Response(
        facialRegister(
        camera=camera, 
        face_detector=face_detection,
        path=path
        ),mimetype='multipart/x-mixed-replace; boundary=frame')

#  Facial Register Function
def facialRegister(camera=None, face_detector=None, path=None):
    global result
    capture=1
    result = "Capture " + str(capture)
    
    # Initialize the timer and the start time
    timer = 0
    start_time = time.time()
   
    while True:
        
        # Capture a frame from the camera
        ret, frame = camera.read()
        
        # check if camera is working
        if not ret:
            break
     
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
        # Detect faces in the frame
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=20, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE) 
        
        # check if there is 1 face detected
        # NOTE: if more than 1 it wont detected and the timer will restart
        if len(faces) == 1:
        
    
            if timer >= 0.5:
                
                if not len(os.listdir(path))==10:
                    cv2.imwrite(path + "/" +str(capture)+".png", frame)
                    capture+=1
                    result = "Capture " + str(capture)

                    print(result)
                else:
                    
                    result = "Training"

                    print(result)
                    # # facial training
                    # result=Jolo().Face_Train()
                    threading.Thread(target=trainingtraining,args=()).start()

                    
                    
                timer = 0
                start_time = time.time()
            else:
                timer += time.time() - start_time
                start_time = time.time()
                
            # Get the coordinates of the face
            (x, y, w, h) = faces[0]
            
            # Draw a rectangle around the face and pt text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)    
        
        
        _, frame_encoded  = cv2.imencode('.png', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_encoded.tobytes() + b'\r\n')

# ********************* API for Facial Register status
@app.route("/update_variable", methods=["GET"])
def update_variable():
    return jsonify(result)


# ------------------- Facial Training
@app.route('/Training')
def Training():
    return render_template('loading.html')


# ********************* API for Facial training

def trainingtraining():
    global result
    result = Jolo().Face_Train()

@app.route("/facialTraining", methods=["GET"])
def facialTraining():

    # result = Jolo().Face_Train()
    return jsonify(result)

    # # Replace this with the code that generates the new value of the variable
    # if result == "Successfully trained":
    #     print(result)
    #     return jsonify(result)
    # else:
        
    #     return jsonify("Don't Interrupt Training Process")

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Database API

# ********************* API for create History
@app.route('/createHistoryS', methods=['GET'])
def createHistoryS():
    CHCH = createHistory(name=Name)
    return jsonify({"message":CHCH})

# ********************* API for delete History
@app.route('/deleteHistoryS', methods=['GET'])
def deleteHistoryS():
    dele = deleteHistory()
        
    return jsonify(dele)

# ********************* API for delete Guest List
@app.route('/deleteGuest', methods=['GET'])
def deleteGuest():
    result = deleteRegistered()

    
    if not result== "No matching record found.":
        threading.Thread(target=trainingtraining,args=()).start()
    
    return jsonify(result)




if __name__ == '__main__':
    app.run(
        # host='192.168.174.11',
        host='0.0.0.0',
        debug=True,
        port=8001)

