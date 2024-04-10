from django.shortcuts import render,HttpResponse,redirect
from .models import Files,TxtFiles
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
import cv2
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyaspeller import YandexSpeller
import os
# Create your views here.
#correct method
import cv2
import numpy as np
from keras.models import load_model
import os
from textblob import TextBlob
from django.http import FileResponse
import mimetypes
from django.http import HttpResponseNotFound, FileResponse


model=load_model('a_96_96.h5')
ClassLabels='abcdefghijklmnopqrstuvwxyz'
ClassLabels=[i for i in ClassLabels]

# model=load_model('/content/CNN_MODEL.h5')
# CnnModel.summary()
def image_read(image):
    image = cv2.imdecode(image,cv2.IMREAD_COLOR)
    # image=cv2.resize(image,(300,100))
    # cv2.imshow("image",image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return image

def gray_image(image):
    gray =cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def image_threshold(image):
    ret,binary = cv2.threshold(image,0,255,  cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV )
    return binary

def image_dilate(image):
    rec_kernal=cv2.getStructuringElement(cv2.MORPH_RECT,(6,4))
    dilated = cv2.dilate(image, rec_kernal, iterations=4)
    return dilated

def image_contours(image):
    contours,hierachy = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont=[]
    for i in contours:
        x,y,w,h=cv2.boundingRect(i)
        cont.append([x,y,w,h])
    sorted_count=list(sorted(cont, key=lambda x:x[0]))
    return sorted_count

def extract(image):
    letters=[]
    letters.clear()
    INPUT_IMAGE=image_read(image)
    GRAY=gray_image(INPUT_IMAGE)
    THRESHOLD=image_threshold(GRAY)
    DILATE=image_dilate(THRESHOLD)
    CONTOURS=image_contours(DILATE)
    clone=INPUT_IMAGE.copy()
    # cv2_imshow(DILATE)

    print('LENGTH OF WORD CONTOURS: ',len(CONTOURS))

    del THRESHOLD, DILATE
    for words in CONTOURS:
        x,y,w,h = words
        img=clone[y:y+h,x:x+w]

        THRESHOLD2=image_threshold(gray_image(img))
        rect_kernals=cv2.getStructuringElement(cv2.MORPH_RECT,(4,4))
        DILATE2=cv2.dilate(THRESHOLD2,rect_kernals,iterations=2)
        CONTOURS2=image_contours(DILATE2)

        print('LENGTH OF CHAR CONTOURS: ',len(CONTOURS2))
        del THRESHOLD2, DILATE2
        cv2.rectangle(INPUT_IMAGE,(x,y),(x+w,y+h),(0,255,0),1)

        for char in CONTOURS2:
            x,y,w,h=char
            img2=img[y:y+h,x:x+w]

            THRESHOLD3=image_threshold(gray_image(img2))
            rect_kernals=cv2.getStructuringElement(cv2.MORPH_RECT,(1,3))
            DILATE3=cv2.dilate(THRESHOLD3,rect_kernals,iterations=2)
            CONTOURS3=image_contours(DILATE3)
            

            for result in CONTOURS3:
                x,y,w,h=result
                img3=img2[y:y+h,x:x+w]

                empty_img = np.full((32,32,1),255, dtype=np.uint8) # a white image used for resize with filling
                x,y = 3,3                    # starting indecies
                resized = cv2.resize(img3, (16,22), interpolation=cv2.INTER_CUBIC)
                grays = gray_image(resized)
                empty_img[y:y+22, x:x+16,0] = grays.copy()
                cl=cv2.cvtColor(empty_img,cv2.COLOR_GRAY2RGB)
                

                pre=cl.astype(np.float32)/255
                pre=np.expand_dims(pre,axis=0)
                pre=np.argmax(model.predict(np.array(pre)))
                pre=ClassLabels[pre]
            
                letters.append(pre)
            
            letters.append(' ')
        letters.append('\n')
    print(letters)
    return letters


# def output(request):
#     speller=YandexSpeller()
#     output=[{'data':speller.spelled(''.join(letters))}]
#     print(type(output))
#     return JsonResponse(data=output,safe=False)


def camera(request):

    # Access the webcam
    camera = cv2.VideoCapture(0)
    camera.set(3,6280)
    camera.set(4, 5020)

    # Capture the image
    while True:

        return_value, image = camera.read() 

    # Save the image
        # cv2.imwrite('image.jpg', image)

        # # Display the image (optional)
        # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # plt.show()
        cv2.imshow('video',image)
        if cv2.waitKey(1) & 0xFF == ord('c'): 
            cv2.imwrite('image.jpg', image)

        # Display the image (optional)
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.show()
            break

    # Release the camera
    camera.release()
    # return redirect('upload')

def home(request):
    user=request.user.id
    txtfiles=TxtFiles.objects.filter(user_id=user)
    return render(request,'index.html',context={'txt_files':txtfiles})

def upload(request):
    if request.method=='POST':
        id=request.user.id
        files=request.FILES['files']
        print('files:',type(files),files)
        print(files)
        if files!=None:
            model=Files.objects.create(user_id=id,file=files)
            model.save()
            data = model.file.read() 
            nparr = np.frombuffer(data, dtype=np.uint8)
            messages.success(request,'successfully file uploaded')
            result=extract(nparr)
            print(result)
            speller=YandexSpeller()
            output=[{'data':speller.spelled(''.join(result))}]
            print(output)
        else:
            messages.error(request,'please upload data!')
        return JsonResponse(data=output,safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def txtfile(request):
    if request.method=='POST':
        content=request.POST.get('content')
        file_name=request.POST.get('file_name')
        file_path=os.path.join('media/txt_files',f'{str(file_name)}.txt')
        with open(file_path,'w') as file:
            file.write(content)
            # print('python file:',type(file),file)
        if content and file_name != None:
            files=TxtFiles(user_id=request.user.id,name=file_name+'.txt',content=content) 
            files.save()
            messages.success(request,'File saved successfully')
            return redirect('home')
            
        else:
            messages.warning(request,'Invalid data')
        return JsonResponse({'message': 'File saved successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def fileview(request):
    user=request.user.id
    txt_files=TxtFiles.objects.filter(user_id=user)
    data=list(txt_files.values())
    # print(data)
    # print(data[-1])
    return JsonResponse(data=data[-1],safe=False)



def download(request,file_name):
    file_path=os.path.join(settings.MEDIA_ROOT,'txt_files',file_name)
    print(file_path)

    if not os.path.exists(file_path):
        return HttpResponseNotFound("The requested file does not exist.")
    
    try:
        with open(file_path, 'rb') as file:
            response = HttpResponse(file,content_type='text')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    except:
        return HttpResponseNotFound("The requested file does not exist.")    


def delete(request,file_name):
    file_path=os.path.join(settings.MEDIA_ROOT,'txt_files',file_name)
    file_db=TxtFiles.objects.filter(name=file_name)
    
    if os.path.exists(file_path) and file_db.exists():
        os.remove(file_path)
        file_db.delete()
        messages.success(request,'successfully deleted file!')
        return redirect('home')
        # return messages.success(request,"file deleted successfully")
    else:
        return HttpResponseNotFound("The requested file does not exist.")


def edit(request,file_name):
    if file_name!=None:
        result=TxtFiles.objects.filter(name=file_name)
        data=[{'content':i.content} for i in result]
        return JsonResponse(data=data,safe=False)
    else:
        return JsonResponse({'message':'File not found are unable to edit the file'},status=400)
