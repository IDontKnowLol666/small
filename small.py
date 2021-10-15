tion
import cv2
import numpy as np
import pygame.mixer as mix
from timezone import timezone as time, data
from gpiozero import Servo

k = cv2.waitKey(1)
img_counter = 0

video_capture = cv2.VideoCapture(0)

jolene_image = face_recognition.load_image_file("mebasically.png")
jolene_face_encoding = face_recognition.face_encodings(jolene_image)[0]

dad_image = face_recognition.load_image_file("dad.JPG")
dad_face_encoding = face_recognition.face_encodings(dad_image)[0]

mom_image = face_recognition.load_image_file("mom.jpg")
mom_face_encoding = face_recognition.face_encodings(mom_image)[0]

christine_image = face_recognition.load_image_file("christine1.jpg")
christine_face_encoding = face_recognition.face_encodings(christine_image)[0]

belen_image = face_recognition.load_image_file("43.jpg")
belen_face_encoding = face_recognition.face_encodings(belen_image)[0]

known_face_encodings = [
    jolene_face_encoding,
    dad_face_encoding,
    mom_face_encoding,
    christine_face_encoding,
    belen_face_encoding
]
known_face_names = [
    "Jolene",
    "Dad",
    "Mom",
    "Christine",
    "belen"
]
servo = Servo(17)
while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"
        center_coordinates = top + right // 2, bottom + left // 2
        radius = top // 2  # or can be h / 2 or can be anything based on your requirements

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            if name == 'belen':
                mix.init()
                mix.music.load('intruder_in_kitchen.mp3')
                mix.music.play()

        cv2.rectangle(frame, (left - 10 , top - 50), (right + 10, bottom + 55), (0, 0, 255), 2)
        center = right + left // 2

        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cv2.putText(frame, name, (left + 20, bottom), font, 1.0, (255, 255, 255), 1)

        def range1(start, end):
            return range(start, end + 1)

        if center < 400:
            servo.min()
            time.sleep(0.5)

        if center > 600:
            servo.max()
            time.sleep(0.5)

video_capture.release()
cv2.destroyAllWindows()
