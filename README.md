# DigiGloveTreeHacks
Seamless human-computer interaction between user's hand and webcam

## Inspiration
The inspiration for this project stems from the growing need for more natural and intuitive ways for humans to interact with computers and digital environments. As technology becomes increasingly integrated into daily life, traditional input methods like keyboards and mice are sometimes insufficient for the nuanced interactions that modern applications demand. Gesture recognition offers a way to bridge the gap between humans and computers by allowing computers to understand and respond to natural human movements. By leveraging advanced computer vision techniques and machine learning models, such as those provided by the Google MediaPipe framework, developers can interpret hand gestures in real-time, making human-computer interaction more intuitive and engaging.

## What it does
The enhanced script combines gesture recognition via webcam using MediaPipe's hand tracking capabilities with real-time angle calculations between joints of the hand, and visualizes the results using PyGame. Additionally, it incorporates the ability to interact with external hardware through a serial connection, like an Arduino, for even more complex applications (which can be enhanced later on for future use). 

## How we built it
Used OpenCV for image processing, MediaPipe for hand tracking, Pygame for visualization, and PySerial for Arduino communication.

## Challenges we ran into
The biggest challenge I ran into was integrating the real-time angle calculations into the PyGame simulation. Constructing a function to calculate the joint angles in an accurate, consistent manner required a bit of research intro linear algebra that I did not expect to do beforehand. 

## Accomplishments that we're proud of
I am proud that I was able to integrate multiple different libraries from OpenCV to Google Mediapipe to form a visualization tool that opens the door for new forms of human-computer interaction and aims to pave the way for a future where technology can seamlessly integrate into the fabric of human activity,  enriching our interactions with the digital world.

## What we learned
I learned a lot more about how to apply CV libraries in order to enable gesture recognition and gained insight into how ML models such as KNN can leverage hand landmark data to better predict gestures as well.

## What's next for DigiGlove
I plan to continue improving the dynamic accuracy and responsiveness of DigiGlove. I hope to continue experimenting with how it may be used in tandem with arudino microcontrollers to collect real-time data and move away from its current static state. 


