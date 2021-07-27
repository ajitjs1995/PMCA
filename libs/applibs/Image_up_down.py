from datetime import time
import time as Time
import pyrebase
import firebase_admin
from firebase_admin import storage as admin_storage, credentials, firestore

import json
import os
import sys
import shutil
class Image_fire:
    root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    config = {
        "apiKey": "AIzaSyDWO1Ko5GRUbt1QmEES09T0hQ3rkBmRYxE",
        "authDomain": "pmca-a03a7.firebaseapp.com",
        "databaseURL": "https://pmca-a03a7-default-rtdb.firebaseio.com",
        "projectId": "pmca-a03a7",
        "storageBucket": "pmca-a03a7.appspot.com",
        "messagingSenderId": "547106992726",
        "appId": "1:547106992726:web:dec56ad3156f948090c1f7",
        "measurementId": "G-DPR677SP1X"
    }
    fire = pyrebase.initialize_app(config)
    storage =fire.storage()   
    
    def upload_Image(self,path_cloud,img_path):
        local_path = 'chat_media\sent'
        destination = os.path.join(self.root_dir, local_path)
        self.storage.child(path_cloud).put(img_path)
        print("Uploaded....")
        file_path = shutil.copy(img_path, destination)
        os.rename(file_path,destination+'/'+path_cloud[9:len(path_cloud)-1]+'.jpg')
        print("copied to .... ", destination)
    def uploaad_profile(self,path_cloud,img_path):
        try:
            self.delete_Image(path_cloud)
        except:
            pass
        self.storage.child(path_cloud).put(img_path)
        print("profile Updated..")
        url = self.storage.child(path_cloud).get_url(" ")
        print("This is img url--->",url)

    def download_Image(self,down_url,local_path,I_name):
        d_path = os.path.join(self.root_dir, local_path)
        print("cloud path ------> ", down_url[0:len(down_url)-1]+'@')
        print("Download started........")
        down_url = down_url[0:len(down_url)-1]+'@'
        self.storage.child(down_url).download(filename = I_name,path = d_path)
        print("Image Downloaded...",d_path)
        try:
            # Time.sleep(5)
            print("file ---> ",I_name,d_path+"/"+I_name+".jpg") 
            shutil.move(I_name, d_path+"/"+I_name+".jpg")
            self.delete_Image(down_url)
            print("............Moving Done......") 
        except FileNotFoundError:
            # self.download_Image(down_url,local_path,I_name)
            print("............Moving not Done......") 

    def delete_Image(self,del_url):

        cred = credentials.Certificate(json.load(open('Json_Files\pmca-a03a7-firebase-adminsdk-usgxo-fff132abb2.json')))
        admin = firebase_admin.initialize_app(cred, {"storageBucket": "pmca-a03a7.appspot.com"})
        bucket = admin_storage.bucket()
        blob = bucket.blob(del_url)
        print(blob)
        blob.delete()
        print("Deleted....")
    # upload_Image(path_cloud,img_path)
    # delete_Image(path_cloud)
    # def fb_download(self):
    #     self.credentials = credentials.Certificate(json.load(open('Json_Files\pmca-a03a7-firebase-adminsdk-usgxo-fff132abb2.json')))
    #     self.app = firebase_admin.initialize_app(
    #         self.credentials,
    #         {"storageBucket": f"{self.credentials.project_id}.appspot.com"},
    #     )
    #     self.db = firestore.client()
    #     self.bucket = admin_storage.bucket()
    #     local_path = 'chat_media'
    #     root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
    #     d_path = os.path.join(root_dir, local_path)
    #     upath = 'Transfer/5TpAcitgDW3TpPopCC55QP@'
    #     filename= 'XuCdZeiVHjkwyHGpXTLooe@.png'
    #     blob = self.bucket.blob(upath)
    #     blob.upload_from_filename(filename)
    # # fb_download()