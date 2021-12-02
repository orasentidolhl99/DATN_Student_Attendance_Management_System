# from django.test import TestCase
# Create your tests here.
import pickle, json
import os

le = "./facial_models/output/le.pickle"
recognizers = "./facial_models/output/recognizer.pickle"
embeddings = "./facial_models/output/embeddings.pickle"

data = pickle.loads(open(embeddings, "rb").read())

# data['embeddings'].clear()
# data['names'].clear()

print(len(data['embeddings']), len(data['names']))

# for item in data['embeddings']:
#     print(item)

# dataset = "media\\datasets"
# user_list = [ f.name for f in os.scandir(dataset) if f.is_dir() ]

# print(user_list)