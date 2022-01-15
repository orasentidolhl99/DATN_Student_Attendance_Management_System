from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import model_from_json
import cv2, os
import numpy as np
from django.conf import settings


# Load Path
cascadeClassifierPath = os.path.sep.join(
    [settings.BASE_DIR, "facial_models\\antispoofing_models\\haarcascade_frontalface_default.xml"])
antispoofingPath = os.path.sep.join(
    [settings.BASE_DIR, "facial_models\\antispoofing_models\\antispoofing_model.json"])
loadweightsPath = os.path.sep.join(
    [settings.BASE_DIR, "facial_models\\antispoofing_models\\antispoofing_model.h5"])

# Load Face Detection Model
face_cascade = cv2.CascadeClassifier(cascadeClassifierPath)
# Load Anti-Spoofing Model graph
json_file = open(antispoofingPath,'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load antispoofing model weights 
model.load_weights(loadweightsPath)


class AntiSpoofing(object):
	def anti_spoofing(frame):
		try:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			for (x, y, w, h) in faces:  
				face = frame[y-5:y+h+5, x-5:x+w+5]
				resized_face = cv2.resize(face,(160, 160))
				resized_face = resized_face.astype("float") / 255.0
				resized_face = img_to_array(resized_face)
				resized_face = np.expand_dims(resized_face, axis=0)
				# pass the face ROI through the trained liveness detector
				# model to determine if the face is "real" or "fake"
				preds = model.predict(resized_face)[0]
				if preds > 0.8:
					label = 'Fake'
					cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
					cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
		except Exception as e:
			print(str(e))