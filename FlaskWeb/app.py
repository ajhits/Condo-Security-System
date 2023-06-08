import cv2
import time

from flask import Flask, render_template,Response,jsonify
# from Jojo_loRecognition.Face_Recognition import Face_Recognition as Jolo

app = Flask(__name__)


# load a camera,face detection
camera = cv2.VideoCapture(0)
face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# homepage =========================================== #
@app.route('/')
def index():
    return render_template('index.html')

# facial Login =========================================== #
@app.route('/facial_login')
def facial_login():
    return render_template('face-login.html')

# ------------------- Load camera
@app.route('/video_feed')
def video_feed():
        return Response(facialDetection(camera=camera, face_detector=face_detection), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')

# ------------------- Facial recognition Function
Text = "Initializing"
def facialDetection(camera=None, face_detector=None):
    global Text
    
    Text=""
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
            # if timer >= 2:
                       
            #     # facial comparison 
            #     response = Jolo().Face_Compare(face=frame)
                
            #     try:
            #         textResult = response[0]

            #         if "No match detected" == response[0]:
            #             fail+=1
            #             B, G, R = (0, 0, 255)
            #             textResult = response[0]
            #             if not fail == 3:
            #                 Text = "Access Denied"
            #         else:
            #             B, G, R = (0, 255, 0)
            #             textResult = response[0]
            #             Text = "Access Granted"
                    
            #     except:
            #         pass
                
            #     # Reset the timer and the start time
            #     timer = 0
            #     start_time = time.time()
            # else:
            #     # Increment the timer by the elapsed time since the last send
            #     timer += time.time() - start_time
            #     start_time = time.time()
                
            # Get the coordinates of the face,draw rectangele and put text
            
        
            cv2.rectangle(frame, (x, y), (x+w, y+h), (B,G,R), 2)
            cv2.putText(frame,textResult,(x,y+h+30),cv2.FONT_HERSHEY_COMPLEX,1,(B,G,R),1)

        # elif len(faces) > 1:
            
        #     # If more than 1 faces 
        #     # B, G, R = (0, 0, 255)
        #     Text = "More than 1 face is detected"
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


# Login as Admin =========================================== #
@app.route('/admin_login')
def admin_login():
    return render_template('login.html')

# Admin Page =========================================== #
# ------------------- Dashboard
@app.route('/admin')
def admin():
    return render_template('Admin/index.html')

# ------------------- Controls
@app.route('/admin/Controls')
def control():
    return render_template('Admin/controls.html')

# ------------------- Historic Data
@app.route('/admin/Historic')
def historic():
    return render_template('Admin/historic.html')

# ------------------- Register
@app.route('/admin/register')
def register():
    return render_template('Admin/register.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5000)