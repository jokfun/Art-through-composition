import os
from os.path import isfile, join
import shutil
from PIL import Image
import tqdm
import numpy as np
import imageio

TEMPFOLDER = "composition_folder_temp"

def smaller(path,resizevalue):
    """
        Create a folder of resized images that will be used to generate the new image.
        Create a list of the average pixels of each image

        Required parameters :
        path : the path of the folder where images are stored
        resizevalue : resizing an image. An image will be equal to 1 pixel
    """

    #Create a folder in which ephemeral images will be stored
    try:
        shutil.rmtree(TEMPFOLDER)
    except Exception as e:
        print(e)
    if not os.path.exists(TEMPFOLDER):
        os.makedirs(TEMPFOLDER)

    print("Listing files from",path)
    try:
        onlyfiles = [f for f in os.listdir(path) if isfile(join(path, f))]
    except Exception as e:
        print(e)
        quit()

    print("Number of pictures :",len(onlyfiles))

    if path[-1] != "/" or path[-1]!="\\":
        path = path +"/"

    result = np.array([])
    files = []
    print("Creating new folder with resized img..")
    for i in tqdm.trange(len(onlyfiles)):
        try:
            img = Image.open(path+onlyfiles[i]).convert('RGB')
            img = img.resize((resizevalue, resizevalue), Image.ANTIALIAS)
            name = TEMPFOLDER+"/"+str(i)+".PNG"
            files.append(name)
            img.save(name)

            img = list(img.getdata())
            img = np.mean(np.array(img))
            result = np.append(result,img)

        except Exception as e:
            print("Error with",path+onlyfiles[i])

    return result,files

def composer(source,path,resizevalue):
    """
        Required parameters :
        source : The original image that will be modified
        path : the path of the folder where images are stored
        resizevalue : resizing an image. An image will be equal to 1 pixel
    """

    meanc,onlyfiles = smaller(path,resizevalue)
    sourcename = source.split("/")[-1].split("\\")[-1].split(".")[0]

    try :
        source = Image.open(source).convert('RGB')
        width, height = source.size

        X = width
        Y = height

        #Resizing the image to fit an integer composite number
        if width%resizevalue!=0:
            X = width-(width%resizevalue)
        if height%resizevalue!=0:
            Y = height-(height%resizevalue)
        source = source.resize((X, Y), Image.ANTIALIAS)

        #We need to reload the image to get a 3-dimensional matrix.
        source.save("resize.PNG")
        arr = imageio.imread("resize.PNG")

        #The new image 
        target = Image.new("RGB",(X,Y))

        posX,posY = 0,0
        print("Creating the new images..")
        for i in tqdm.trange(0,Y,resizevalue):
            for j in range(0,X,resizevalue):

                #We're looking for the image that most closely matches a certain area
                test = np.mean(arr[i:i+resizevalue,j:j+resizevalue])
                idx = (np.abs(meanc - test)).argmin()

                addImg = Image.open(onlyfiles[idx])
                target.paste(addImg,(j,i))

        #Save the image
        name = sourcename+"_composition.JPG"
        target.save(name)
        print("New image is created as",name)

        shutil.rmtree(TEMPFOLDER)
        os.remove("resize.PNG")

    except Exception as e:
        print(e)