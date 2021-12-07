from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import cv2, os, urllib.request, pickle
import numpy as np
from django.conf import settings
from .extract_train import extract_embeddings
from .extract_train import train_model
import datetime
from .antispoofing.anti_spoofing import AntiSpoofing


tz_hcm = datetime.timezone(datetime.timedelta(hours=7))

# load our serialized face detector model from disk
protoPath = os.path.sep.join([settings.BASE_DIR, "facial_models\\face_detection_model\\deploy.prototxt"])
modelPath = os.path.sep.join([settings.BASE_DIR,"facial_models\\face_detection_model\\res10_300x300_ssd_iter_140000.caffemodel"])
# # detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load our serialized face embedding model from disk
embedderPath = os.path.join(settings.BASE_DIR,'facial_models\\face_detection_model/openface_nn4.small2.v1.t7')
# # embedder = cv2.dnn.readNetFromTorch(embedderPath)

# load the actual face recognition model along with the label encoder
recognizerPath = os.path.sep.join([settings.BASE_DIR, "facial_models\\output\\recognizer.pickle"])
# # recognizer = pickle.loads(open(recognizer, "rb").read())

lePath = os.path.sep.join([settings.BASE_DIR, "facial_models\\output\\le.pickle"])
# # le = pickle.loads(open(le, "rb").read())

datasetPath = os.path.sep.join([settings.BASE_DIR, "media\\datasets"])
user_list = [ f.name for f in os.scandir(datasetPath) if f.is_dir() ]

class FaceDetect(object):
	def __init__(self):
		# initialize data train in file, for initialize variable
		extract_embeddings.init_data()
		extract_embeddings.embeddings()
		train_model.model_train()
  
		print('--------- t met qua r, chay auto load dum t cai -------------')
		# initialize variable, then detect face for attendence
		self.detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
		self.embedder = cv2.dnn.readNetFromTorch(embedderPath)
		self.recognizer = pickle.loads(open(recognizerPath, "rb").read())
		self.le = pickle.loads(open(lePath, "rb").read())

		# initialize the video stream, then allow the camera sensor to warm up
		self.vs = VideoStream(src=0).start()
		# start the FPS throughput estimator
		self.fps = FPS().start()

	def __del__(self):
		self.vs.stop()
		self.fps.stop()
  
		self.vs.stream.release()
		cv2.destroyAllWindows()

	def get_frame(self):
		# grab the frame from the threaded video stream
		frame = self.vs.read()
		frame = cv2.flip(frame,1)

		AntiSpoofing.anti_spoofing(frame)
		# init student
		result ={}
  
		# resize the frame to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		frame = imutils.resize(frame, width=600)
		(h, w) = frame.shape[:2]

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		self.detector.setInput(imageBlob)
		detections = self.detector.forward()


		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections
			if confidence > 0.7:
				# compute the (x, y)-coordinates of the bounding box for
				# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI
				face = frame[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

				# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

				# construct a blob for the face ROI, then pass the blob
				# through our face embedding model to obtain the 128-d
				# quantification of the face
				faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
					(96, 96), (0, 0, 0), swapRB=True, crop=False)
				self.embedder.setInput(faceBlob)
				vec = self.embedder.forward()

				# perform classification to recognize the face
				preds = self.recognizer.predict_proba(vec)[0]
				j = np.argmax(preds)
				proba = preds[j]
				name = self.le.classes_[j]


				# perform classification to recognize the face
				preds = self.recognizer.predict_proba(vec)[0]
				j = np.argmax(preds)
				proba = preds[j]
				detect_face_find = self.le.classes_[j]

				if detect_face_find != 'Unknown':
					detect_face_find = detect_face_find.split('_', 1)
					# draw the bounding box of the face along with the
					# associated probability
					text = "{}: {:.2f}%".format(detect_face_find, proba * 100)
					y = startY - 10 if startY - 10 > 10 else startY + 10
		
					result['student_code'] = detect_face_find[0]
					result['check_time'] = datetime.datetime.now(tz_hcm).strftime("%m-%d-%Y, %H:%M:%S")
		
					# self.facial_landmarks(frame)
					cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 2)

		# update the FPS counter
		self.fps.update()
		ret, jpeg = cv2.imencode('.jpg', frame)
		return jpeg.tobytes()
		