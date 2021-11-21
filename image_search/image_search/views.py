from typing import final
from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect, render
import json
from django.http import JsonResponse
import matplotlib.pyplot as plt
# from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
from keras.models import Model, load_model
import pickle
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions




# model = load_model('./DataSet/model_9.h5')
# model_2048 = load_model('./DataSet/2048_img_model.h5')

# with open('./DataSet/word_to_idx.pkl','rb') as f:
#     word_to_idx = pickle.load(f)

# with open('./DataSet/idx_to_word.pkl','rb') as f:
#     idx_to_word = pickle.load(f)



def home(request):
    return render(request,'index.html')


def process_img(request):

    if request.method == 'POST':
        f = request.FILES['file']
        myfile = f.read()

        image = cv2.imdecode(np.frombuffer(myfile,np.uint8),cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        photo = cv2.resize(image,(224,224))
     
        caption = predict_caption(photo)

        print(caption)
        data = {"caption":caption}
        return JsonResponse(data)
    # else:
    #     return redirect("/")




def scrap_img(caption):
    pass





def predict_caption(photo):
    # global model
    # global model_2048
    # global word_to_idx
    # global idx_to_word

    model = load_model('./DataSet/model_9.h5')
    model_2048 = load_model('./DataSet/2048_img_model.h5')

    with open('./DataSet/word_to_idx.pkl','rb') as f:
        word_to_idx = pickle.load(f)

    with open('./DataSet/idx_to_word.pkl','rb') as f:
        idx_to_word = pickle.load(f)


    max_len = 35
    photo = encode_image(photo,model_2048)
    


    in_text = "startseq"
    for i in range(max_len):
        sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
        sequence = pad_sequences([sequence],maxlen=max_len,padding='post')
        
        ypred = model.predict([photo,sequence])
        ypred = ypred.argmax() #WOrd with max prob always - Greedy Sampling
        word = idx_to_word[ypred]
        in_text += (' ' + word)
        
        if word == "endseq":
            break

    final_caption = in_text.split()[1:-1]
    final_caption = ' '.join(final_caption)

    return final_caption


def preprocess_img(img):
    img = np.expand_dims(img,axis=0)
    # Normalisation
    img = preprocess_input(img)


    return img

def encode_image(img,model_2048):

    img = preprocess_img(img)
    feature_vector = model_2048.predict([img])
    
    # feature_vector = feature_vector.reshape((-1,))
    #print(feature_vector.shape)
    return feature_vector