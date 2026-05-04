# FOR OBJECT DECTION IN FRONT OF YOU 
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from gtts import gTTS
import pygame
import os
from datetime import datetime
import time
import speech_recognition as sr


def speech(text):
    output_dir = "./sound/"
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = os.path.join(output_dir, f"output_{timestamp}.mp3")

    output = gTTS(text=text, lang='en')
    output.save(output_file)

    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def object_detection_and_speech():
    video = cv2.VideoCapture(0)
    labels = []
    last_clear_time = time.time()
    no_items_message = "No items in front of you"

    # Initialize recognizer
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        ret, frame = video.read()
        bbox, label, conf = cv.detect_common_objects(frame)
        output_image = draw_bbox(frame, bbox, label, conf)
        cv2.imshow("Object Detection", output_image)

        current_time = time.time()
        if current_time - last_clear_time >= 5:
            labels.clear()
            last_clear_time = current_time

        for item in label:
            if item not in labels:
                labels.append(item)

        if not labels:
            print(no_items_message)
            speech(no_items_message)
        else:
            i = 0
            new_sentence = []
            for label in labels:
                if i == 0:
                    new_sentence.append(f"{label} in front of you")
                else:
                    new_sentence.append(f"and a {label}")
                i += 1

            print(" ".join(new_sentence))
            new_sentence_as_strings = [str(item) for item in new_sentence]
            text_to_speak = ' '.join(new_sentence_as_strings)
            speech(text_to_speak)

        # Listen for voice command
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            if "stop" in command.lower():
                break
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Could not request results; check your internet connection")

        # Check for 'q' key press to break the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()

#object_detection_and_speech()
