from main_imports import (MDDialog, MDFlatButton, MDGridBottomSheet, MDScreen,
                          OneLineTextDialog)

from libs.applibs import utils
from kivy.core.window import Window


from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.storage.jsonstore import JsonStore
import requests
import json
import os
import threading
import shutil
from libs.applibs.Image_up_down import Image_fire
from libs.applibs.dialog_case import Dialog_case
from libs.applibs.unread_msg_count import UnreadMsgCount


utils.load_kv("profile.kv")

class Profile_Screen(MDScreen):
    key1 =''
    Image = Image_fire()
    D = Dialog_case()
    dlg = 0
    def on_pre_enter(self, *args):
        # self.select_path('/')
        if self.dlg == 0:
            self.D.open_dlg()
            self.dlg = 1
        with open('Json_Files/UserInfo.json') as f:
            data = json.load(f)
        key, value = list(data.items())[0]
        self.key1 = key
        
        threading.Thread(target=self.runinbackground).start()
        threading.Thread(target=self.load_details).start()
    def load_details(self):
        file_path = 'Json_Files/profile.json'
        userinfo = 'Json_Files/UserInfo.json'
        try:
            if os.path.getsize(file_path) != 0:
                with open(file_path) as f:
                    data = json.load(f)
                    print(data)
                    value = data
                    self.ids.profile_image.background_normal = value
                    self.ids.profile_image.background_down = value
            else:
                # try:
                Internet_check = requests.get('https://pmca-a03a7-default-rtdb.firebaseio.com/.json')
                if Internet_check.ok == True:
                    url ="https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.key1+"/details/.json"
                    request  = requests.get(url)            
                    data = request.json()
                    path = data["Profile_pic"]
                    if path != " ":
                        self.Update_profile_image(path)
                    else:
                        print("Enternet")
                else:
                    print("I Am OFFLINE Keep ME Online")
                # except requests.exceptions.RequestException as e:  # This is the correct syntax
                #     print("You are Offline")
            if os.path.getsize(userinfo) != 0:
                with open(userinfo) as f:
                    data = json.load(f)
                    key, value = list(data.items())[0]
                    self.key1 = key
                    P_Name = data[key]['Name']
                    P_Username = data[key]['Username']
                    self.ids.profile_name.secondary_text = P_Name
                    self.ids.profile_username.secondary_text ='@'+ P_Username
                    self.ids.profile_Phone.secondary_text =key
                    self.D.close_dlg()
        except FileNotFoundError:
            print("file not Found")
    def runinbackground(self):
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )
# file Manager section---------------------------------
    def file_manager_open(self):
        print('hello.......')
        self.file_manager.show('assets\profile')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''        
        data = path
        # import shutil
        # des = "assets\img"
        # shutil.copy(path,des)
        self.Update_profile_image(path)
        self.exit_manager()
        JsonStore("Json_Files/profile.json")
        try:
            with open('Json_Files/profile.json','w') as f:
                json.dump(data,f)
                print("UserInfo file is modified...")

        except KeyError:
            print("the data is not stored...")
        toast(path)
        # self.Image.delete_Image(self.key)
        threading.Thread(target=self.Image.uploaad_profile(self.key1,path)).start()

    def Update_profile_image(self,path):
        '''This will update image in DataBase and profile section in App Also'''
        # https://pmca-a03a7-default-rtdb.firebaseio.com/9594897959/details/Profile_pic
        url1 = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.key1+"/details/.json"

        file = {
                "Profile_pic" : path
                }
        try:
            requests.patch(url1,json = file)
            self.ids.profile_image.background_normal = path
            self.ids.profile_image.background_down = path
        except requests.exceptions.RequestException as e:
            print("no internet ")
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
    # file manager ends ----------------------------------------------------- 
    
    def change_profile_data(self,widget):
        """Change text data using Dialog box.
        [widget] change this widget text"""
        dialogObj =None
        Dialog=OneLineTextDialog()
        def cancel_btn(btn):
            # use function when CANCEL btn click
            dialogObj.dismiss(force=True)
        def ok_btn(btn):
            # use function when OK btn click
            changed_name = Dialog.ids.dialog_text.text
            widget.secondary_text = changed_name
            url1 = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.key1+"/details/.json"            
            file = {
                    "Name" : changed_name
                    }
            requests.patch(url1,json = file)
            request  = requests.get(url1)            
            data = request.json()
            userinfo = {self.key1:data}
            try:
                with open('Json_Files/UserInfo.json','w') as f:
                    json.dump(userinfo,f)
                    print("UserInfo file is modified...")
            except KeyError:
                print("the data is not stored...")
            cancel_btn(btn)
        
        if not dialogObj:
            dialogObj=MDDialog(
                auto_dismiss=True,
                title= widget.secondary_text,
                type="custom",
                content_cls=Dialog,
                buttons=[
                    MDFlatButton(
                        text="CANCEL", 
                        # text_color=self.theme_cls.primary_color,
                        on_release=cancel_btn,
                    ),
                    MDFlatButton(
                        text="OK", 
                        # text_color=self.theme_cls.primary_color,
                        on_release=ok_btn,
                    ),
                ],
            )
        dialogObj.open()
        
    
    def change_profile_img(self):
        """
        method call when image click on profile_view page.
        if it's user own profile than show options of change.
        """
        bottom_sheet_menu = MDGridBottomSheet(
            animation=True,
        )
        data = {
            "Upload": "cloud-upload",
            "Camera": "camera",
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.file_manager_open(),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()
    
    def del_media(self):
        print("Deleting Media files....")
        try:
            shutil.rmtree(r"chat_media")
            self.parent.Bottom_msg("All Media Deleted Permanantly")
        except FileNotFoundError:
            self.parent.Bottom_msg("All Media Deleted")
    
    def Logout(self):
        f = open("Json_Files/UserInfo.json", "r+")  
        m = open("Json_Files/profile.json", "r+")  
        n = open("Json_Files/ChatHub.json", "r+")  
        # p = open("database.json", "r+")  
        # absolute file positioning 
        f.seek(0)  
        m.seek(0)  
        n.seek(0)  
        # to erase all data  
        f.truncate()
        m.truncate()
        n.truncate()
        self.parent.get_screen("home").New_data_list.clear()
        self.parent.get_screen("home").ids.rv.data = []
        
        self.parent.get_screen("home").ids.rv.refresh_from_data()
        print("cleared all...")
        self.parent.get_screen("home").recall.cancel()
        C = UnreadMsgCount()
        C.offline_count.clear()
        C.online_count.clear()
        d = self.parent.get_screen("home").dlg = 0
        d = self.parent.get_screen("home").username.clear()
        s = self.dlg = 0
        # print(d , s)username
        self.ids.profile_image.background_normal = "assets//img//blank_profile.png"
        self.ids.profile_image.background_down = "assets//img//blank_profile.png"
        self.parent.change_screen("login") 