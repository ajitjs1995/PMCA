from main_imports import MDScreen
from libs.applibs import utils
from kivy.properties import BooleanProperty, StringProperty
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
# Python imports
import sys
import requests
import json
import os
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))



utils.load_kv("login.kv")

class Login_Screen(MDScreen):
    login_check = False
    web_api_key = "AIzaSyDWO1Ko5GRUbt1QmEES09T0hQ3rkBmRYxE"
    # Firebase Authentication Credentials - what developers want to retrieve
    url  = "https://pmca-a03a7-default-rtdb.firebaseio.com/.json"
    auth = "QzCjigNhgwpP9dzrQKKosdRKYtnk2ButNsf2ykIa"
    file_path = 'Json_Files/UserInfo.json'
    def on_enter(self):
        file_path = self.file_path
        try:
            if os.path.getsize(file_path) != 0:
                with open(file_path) as f:
                    data = json.load(f)
                    key, value = list(data.items())[0]
                    self.login_check = True
                    self.ids.Phone.text = key            
        except FileNotFoundError:
            print("file not Found")
    def on_leave(self):
        self.ids.Phone.text = ''
        self.ids.Phone.helper_text = 'Enter 10 Numbers'

    def sign_in(self, Phone):  
        numbers= set()
        self.phone_number = Phone        
        try:
            self.login_check = False            
            request  = requests.get(self.url+'?auth='+self.auth) 
            print(request.ok,"login req status 1")           
            self.data = request.json()            
            for key,value in self.data.items():
                numbers.add(key)     
            if Phone in numbers:
                JsonStore("Json_Files/ChatHub.json")
                self.parent.change_screen("verification") 
                # print(data[Phone]['details']['Username'])
                # self.login_check=True
                # userinfo = {Phone:data[Phone]['details']}
                # try:
                #     with open(self.file_path,'w') as f:
                #         json.dump(userinfo,f)
                #         print("UserInfo file is modified...")
                # except KeyError:
                #     print("the data is not stored...")
            else:
                self.parent.change_screen("login")
                self.ids.Phone.helper_text = str(Phone) + ' User Does Not Exist'
                self.ids.Phone.text = str(Phone) + ' '      
        except requests.exceptions.RequestException:  # This is the correct syntax
            print("You are Offline")
            with open(self.file_path,'r') as D:
                data = json.load(D)
            for key,value in data.items():
                numbers.add(key)
            if Phone in numbers:
                self.parent.change_screen("home")
    def validate(self,Password):
        D = False
        login_data = self.data
        Actual_pass = login_data[self.phone_number]['details']['Password']
        print("This is password ......................",Actual_pass)
        print(Password[1:])
        if Actual_pass == Password:
            # self.parent.change_screen("home") 
            D = True
            userinfo = {self.phone_number:login_data[self.phone_number]['details']}
            try:
                with open(self.file_path,'w') as f:
                    json.dump(userinfo,f)
                    print("UserInfo file is modified...")
            except KeyError:
                print("the data is not stored...")
        else:
            D = False
            print(self)
            # self.parent.Bottom_msg("Please Enter Correct Password")     
        return D 


        # else:
        #     print("i am in else Login")
        #     self.ids.Phone.on_error = True