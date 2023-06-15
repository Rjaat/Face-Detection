import cv2
# Loading pre-trained f-detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

image = cv2.imread('images\img.png')

#image to grayscale for face detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around the detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Define the desired window size
window_width = 800
window_height = 600
# Resize the image to the desired window size
resized_image = cv2.resize(image, (window_width, window_height))
# Display the image with detected faces
cv2.imshow("Detected Face", resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()