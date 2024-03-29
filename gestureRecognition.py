# Nikhil Surapaneni
# TreeHacks

import pygame
import cv2
import mediapipe as mp
import time
import numpy as np
import pickle
import argparse
import serial

# User defined constants
WIDTH, HEIGHT = 640, 480
RECORD_TIME = 10

data = []

# Define the function to calculate the angle between three points
def calculate_angle(point1, point2, point3):
    """
    Calculate the angle between three random points
    """
    point1 = np.array(point1)
    point2 = np.array(point2)  # This is the joint point
    point3 = np.array(point3)
    
    vector1 = point1 - point2
    vector2 = point3 - point2
    
    cosine_angle = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # Ensure the cosine value is within the valid range
    
    angle = np.arccos(cosine_angle)
    angle = np.degrees(angle)  # Convert to degrees
    
    return angle

parser = argparse.ArgumentParser()
parser.add_argument("--gesture", help="Gesture to be recorded", type=str, default=None)
parser.add_argument("--knn", help="Filename of pickled KNN", type=str, default=None)
parser.add_argument("--data_dir", help="Directory to save data to", type=str, default=None)
parser.add_argument("--port", help="Port for Arduino connection", type=str, default=None)
args = parser.parse_args()

# for future arduini use
arduino_serial = None
if args.port:
    arduino_serial = serial.Serial(args.port, 230400)
    print("The port %s is available" % arduino_serial)

if args.knn:
    knn_file = open(args.knn, 'rb')     
    knn = pickle.load(knn_file)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, max_num_hands=1)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)  # Font for displaying text

start = time.time()
world_landmarks = []
gesture = ""

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        clock.tick(60)
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        # Process the image and detect hands
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Calculate and display angle for a specific joint as an example
                try:
                    wrist = [hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,
                             hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z]

                    index_mcp = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x,
                                 hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y,
                                 hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].z]

                    index_pip = [hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x,
                                 hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y,
                                 hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].z]

                    # Calculate the angle
                    angle = calculate_angle(wrist, index_mcp, index_pip)
                    gesture = f"Angle: {angle:.2f}"  # Display the calculated angle
                except Exception as e:
                    print(f"Error calculating angle: {e}")
                
                # Draw hand landmarks on the original image
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        
        # Convert the image from BGR to RGB, rotate and flip for correct orientation
        image = cv2.cvtColor(np.rot90(image), cv2.COLOR_BGR2RGB)
        image = pygame.surfarray.make_surface(image)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        
        # Render the image and the gesture text on the screen
        screen.blit(image, (0, 0))
        gesture_text = font.render(gesture, True, (255, 255, 255))
        screen.blit(gesture_text, (10, 10))
        
        pygame.display.update()

        # Handle quitting the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                quit()

    cap.release()

