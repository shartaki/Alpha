import cv2
import os
import pyttsx3
import time # add this for 15 sec 
# Function to get unique names from the dataset
def get_unique_names(path):
    imagePath = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    names = set()
    for imagePaths in imagePath:
        name = os.path.split(imagePaths)[-1].split(".")[1]
        names.add(name)
    return list(names)

def face_recognition():
    # Initialize text-to-speech engine
    engine = pyttsx3.init()

    # Path to dataset
    dataset_path = "C:/Users/shart/Personal_Assistant/personal assistant/datasets"
    name_list = get_unique_names(dataset_path)

    video = cv2.VideoCapture(0)

    #facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("Trainer.yml")
    start_time = time.time()  ##new line for 15 sec ##
    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            serial, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 85 and serial < len(name_list):
                name = name_list[serial]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
                cv2.putText(frame, name, (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 155), 2)
                engine.say(f"hello,{name}")
                engine.runAndWait()
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
                cv2.putText(frame, "UNKNOWN PERSON", (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 155), 2)
                engine.say("Unknown person in front of you")
                engine.runAndWait()
        cv2.imshow("frame", frame)
        if time.time() - start_time > 15:  # Run for 15 seconds
            break
        k = cv2.waitKey(1)
        if k == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
    print("Face recognition Done.................")

#Call the function to run the code
#face_recognition()
