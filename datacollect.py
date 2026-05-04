import cv2
import numpy as np
from PIL import Image
import os
import speech_recognition as sr
import pyttsx3

def collect_and_train_faces():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Function to speak out text
    def speak(text):
        engine.say(text)
        engine.runAndWait()

    # Function to get voice input for the name
    def get_voice_input():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Please say the name:")
            speak("Please say the name")
            audio = recognizer.listen(source)
            try:
                name = recognizer.recognize_google(audio)
                print(f"Name recognized: {name}")
                return name
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                return get_voice_input()
            except sr.RequestError:
                print("Could not request results; check your network connection.")
                return None

    # Function to get image IDs and corresponding face data
    def get_image_id(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        faces = []
        ids = []
        for image_path in image_paths:
            face_image = Image.open(image_path).convert('L')
            face_np = np.array(face_image, 'uint8')
            name = os.path.split(image_path)[-1].split(".")[1]
            ids.append(name)
            faces.append(face_np)
            cv2.imshow("Training", face_np)
            cv2.waitKey(1)
        return ids, faces

    # Initialize video capture
    video = cv2.VideoCapture(0)

    # Load the Haar Cascade for face detection
    #facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Get the name from voice input
    name = get_voice_input()

    # Check if the name was recognized
    if name:
        count = 0
        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                count += 1
                cv2.imwrite(f'datasets/users.{name}.{count}.jpg', gray[y:y+h, x:x+w])
                cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)

            cv2.imshow("frame", frame)
            k = cv2.waitKey(1)
            if count >= 500:  # Ensure to capture up to 500 images
                break

        video.release()
        cv2.destroyAllWindows()
        print("Dataset collection Done.")

        # Train the face recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        path = "datasets"

        names, facedata = get_image_id(path)
        # Convert names to unique integer IDs
        unique_names = list(set(names))
        name_id_map = {name: idx for idx, name in enumerate(unique_names)}
        ids = [name_id_map[name] for name in names]

        recognizer.train(facedata, np.array(ids))
        recognizer.write("Trainer.yml")
        cv2.destroyAllWindows()
        print("Training completed.")
    else:
        print("Failed to recognize name via voice input.")

# Call the function to collect and train faces
#collect_and_train_faces()
