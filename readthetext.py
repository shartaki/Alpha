import pytesseract
import cv2
from PIL import Image
import pyttsx3

def initialize_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    return engine

def capture_and_read_text():
    language = 'en'
    engine = initialize_engine()
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    
    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('z'):
                cv2.imwrite(filename='saved_img.jpg', img=frame)
                webcam.release()
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                string = pytesseract.image_to_string('saved_img.jpg')
                print(string)
                engine.setProperty('rate', 125)
                engine.say("Hi")
                engine.say(string)
                engine.runAndWait()
                print("Image saved!")
                cv2.destroyAllWindows()
                break
        
        except KeyboardInterrupt:
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
