from django.shortcuts import render
from django.core.files.storage import default_storage

from app1.models import Image
from app1.forms import ImageForm


import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

model_file=load_model(filepath='static/vgg19.h5',
                      custom_objects={'Functional':tf.keras.models.Model})

class_dict={'Tacterial_spot': 0,
             'Early_blight': 1,
             'Late_blight': 2,
             'Leaf_Mold': 3,
             'Septoria_leaf_spot': 4,
             'Spider_mites Two-spotted_spider_mite': 5,
             'Target_Spot': 6,
             'Tomato_Yellow_Leaf_Curl_Virus': 7,
             'Tomato_mosaic_virus': 8,
             'healthy': 9}


# Image preparation 
def prepare(filepath):
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    img_array = img_array / 255
    new_array = cv2.resize(img_array, (224, 224))
    return new_array.reshape(-1, 224, 224, 3)
def prediction(img):
    pred_result=np.argmax(model_file.predict(img))
    disease_category=list(class_dict)
    return disease_category[pred_result]



def Home(request):
    if request.method=='POST':
        file=request.FILES['img']
        file_name=default_storage.save(file.name,file)
        file_url=default_storage.path(file_name)

        img=prepare(file_url)
        result=prediction(img)
        print(result)
        context={'result':result,'img_url':file_url}
        return render(request, 'app1/index.html', context=context)

    else:
        return render(request, 'app1/index.html')
    
    return render(request, 'app1/index.html',)

















# Create your views here.
# def Home(request):


#     image_database=Image.objects.last()
#     # print(type(image_database.img))
#     img=prepare(image_database)
#     result=prediction(img)
#     print(result)
#     form=ImageForm(request.POST, request.FILES)
#     if request.method=='POST':

#         if form.is_valid:
#             form.save()
#             return render(request, 'app1/index.html',context={'form':form,'image_database':image_database})
        

#         print('ok')

#     return render(request, 'app1/index.html',context={'form':form,'image_database':image_database})

