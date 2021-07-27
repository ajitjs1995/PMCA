from main_imports import ImageLeftWidget, MDScreen, TwoLineAvatarListItem
from libs.applibs import utils
from kivy.clock import Clock
from libs.applibs.profile_preview_dialog import ProfilePreview
from libs.applibs.dialog_case import Dialog_case
from libs.applibs.unread_msg_count import UnreadMsgCount

# import 
# Python imports
import threading
import sys
import requests
import random
import json
import os
utils.load_kv("home.kv")

class Home_Screen(MDScreen):
    loginId = ''
    internet = 1
    url = 'https://pmca-a03a7-default-rtdb.firebaseio.com/'
    chat_file = 'Json_Files/ChatHub.json'
    file_path = 'Json_Files/UserInfo.json'
    database = 'Json_Files/database.json'
    username = set()
    chat_number_list = set()
    D = Dialog_case()
    New_data_list = []
    dlg = 0
    def on_pre_enter(self, *args):
        if self.dlg == 0:
            self.D.open_dlg()
            self.dlg = 1
        #print("I am in Pre Enter --------------------------------->")
        try:
            if os.path.getsize(self.file_path) != 0:
                with open(self.file_path) as f:
                    data = json.load(f)
                    key, value = list(data.items())[0]
                    self.loginId = key
                url1 = self.url+self.loginId+'/chats.json'
                #print("i am from home page",self.loginId," url: ",url1)
                try:
                    all_chats = requests.get(url1)
                    chats_data = all_chats.json()
                
                # To store All Chats in local json file(ChatHub.json)
                    with open(self.chat_file,'w') as C:
                        json.dump(chats_data,C) 
                    
                # This is for looking which chat numbers present
                    # for i in chats_data : 
                    #     print("chats numbers",i)
                except requests.exceptions.RequestException:  # This is the correct syntax
                    # Offline code goes here.. Load the ChatHub.json file to Screen
                    # print("You are Offline")
                    self.parent.Bottom_msg("Please Turn On Internet..")
                    # twolineW= TwoLineAvatarListItem(text=f"Hamster",
                    #     secondary_text="@username",
                    #     on_touch_up=self.chat_room)

                    # twolineW.add_widget(ImageLeftWidget(source="assets//img//hamster_icon.png"))
            
                    # self.screen_manager.get_screen("home").ids.chat_tab.add_widget(twolineW)
            else:
                print("file is empty")
        except FileNotFoundError:
            print("file not Found")        
    def on_enter(self, *args):
        #print("I am in on Enter --------------------------------->")
        
        try:
            request = requests.get("https://www.google.com/")
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            #print("You are Offline")
            self.parent.Bottom_msg("Please Turn On Internet..")
            self.internet = 0
        chat_number_data = set()
        if self.internet == 1:
            with open(self.file_path) as f:
                data = json.load(f)
                key, value = list(data.items())[0]
            #print("This is url from Home/on enter---> ",self.url+key+'/chats/.json')
            all_chat_data = requests.get(self.url+key+'/chats/.json')
            all_chat_data = all_chat_data.json()
            if all_chat_data != "None":
                with open(self.database) as g:
                    data_1 = json.load(g)
                for i in all_chat_data:
                    for A in all_chat_data[i]:
                        latest_msg = all_chat_data[i][A]
                    #print("Home data --- > ",i," ",latest_msg )                    
                    chat_number_data.add(i)
                    #print(data_1[i])
                    #print(self.username)
                    if data_1[i] not in self.username:
                        #print("this is if 1----------------->")
                        self.username.add(data_1[i])
                        self.all_chats(data_1[i],latest_msg)
                        self.D.close_dlg()
            else:
                self.D.close_dlg()
                self.parent.Bottom_msg("Chats Not Found")
                #print("No data available")
        else:
            with open(self.database) as g:
                data_1 = json.load(g)
            with open(self.chat_file) as d:
                chats = json.load(d)
            for i in chats:
                for A in chats[i]:
                    latest_msg = chats[i][A]
                chat_number_data.add(i)
                if data_1[i] not in self.username:
                    self.username.add(data_1[i])
                    self.all_chats(data_1[i],latest_msg)
                    self.D.close_dlg()
        self.recall = Clock.schedule_interval(self.threading_method, 1) #every 1 sec all this method
        #print("this is on enter section of home : ",chat_number_data)
        #print("this is on enter section of home list : ",self.username)
    def all_chats(self,name,latest_msg):
        """
        All Chat that show in home chat tab. all chat are added by 
        this method. it will use in differe t in future.
        """ 
        #print("ALl chats --------------->")    
        # self.change_screen("profile")
        #Load All chat from file...add() 
        if latest_msg[-1] == '@' or latest_msg[-1] == '#':
            latest_msg = '[Image]'
        else:
            latest_msg = latest_msg[0:len(latest_msg)-1]
        
        img_number = self.get_key(name)
        # for number, names in database.items():
        #     #print("This is image name --- >",names," = ",name)
        #     if names == name:
        #         print("Match number  ----- > ",number)
        #         img_number = number
            

        # img_name = self.select_img()
        path ="https://firebasestorage.googleapis.com/v0/b/pmca-a03a7.appspot.com/o/"+img_number+"?alt=media&token="
        #print(path) 
        user_data = {
                "text": name,
                "secondary_text": latest_msg,
                "time":"9:30",
                "image": path,
                "count_is": 0
            }
        # pre_data = {'name':name,'path':path}
        self.ids.rv.data.append(user_data)
        self.New_data_list.append(user_data)
        #print("all chats Ends---------------->")
        # twolineW= TwoLineAvatarListItem(text= name,
        #     # secondary_text='i',
        #     on_press=self.chat_room)
        # twolineW.add_widget(ImageLeftWidget(source=path))        
        # self.parent.get_screen("home").ids.chat_tab.add_widget(twolineW)
    def get_key(self,val):
        with open('Json_Files/database.json') as f:
            database = json.load(f)
        for key, value in database.items():
            if val == value:
                return key
    
        return "blank_profile.png"
    def open_dialog(self,text,img):
        ProfilePreview().fire(title=text, image=img)
    def chat_room(self,text):
        """Switch to Chatroom. but username and chatroom username 
        change according to which one you touch in chat list"""
        
        name = text
        #print("Screen Name",name)
        self.parent.get_screen("chat_room").ids.profile_bar.title = str(name)
        # self.parent.get_screen("chat_room").use = name
        self.parent.change_screen("chat_room")
    def search_account(self,search_field):
        """
        this method use when search button pressed search_field
        contain data in string that you want to search on hamster server
        """
        database_path = 'Json_Files/database.json'
        try:
            if os.path.getsize(database_path) != 0:
                with open(database_path) as f:
                    data = json.load(f)                    
        except FileNotFoundError:
            print("file not Found")
        numbers = set()
        uasername = set()
        for key,value in data.items():
            numbers.add(key)
            uasername.add(value)
        # for dummy search item [------
        img_number= self.get_key(search_field)
        img_name = self.select_img()
        if search_field in uasername:
            twolineW= TwoLineAvatarListItem(text=f"{search_field}",
                secondary_text=f"@{search_field}",on_press= lambda x:self.chat_room(search_field)) # Use Lambda function here to get in chat room
            path ="https://firebasestorage.googleapis.com/v0/b/pmca-a03a7.appspot.com/o/"+img_number+"?alt=media&token="

            twolineW.add_widget(ImageLeftWidget(source=path))
            
            self.ids.search_items.add_widget(twolineW)
        # Search From Numbers------------------------ 
        # elif search_field in numbers:
        #     twolineW= TwoLineAvatarListItem(text=f"{search_field}",
        #         secondary_text=f"@{search_field}",on_press= lambda x:self.chat_room(search_field)) # Use Lambda function here to get in chat room
        #     path ="https://firebasestorage.googleapis.com/v0/b/pmca-a03a7.appspot.com/o/"+img_number+"?alt=media&token="

        #     twolineW.add_widget(ImageLeftWidget(source=path))
            
        #     self.ids.search_items.add_widget(twolineW)
        # #  ----- ] end dummy search
    def select_img(self):
        path = 'assets\profile'
        names = random.choices(os.listdir(path), k=1) #----> Randomly select 1 images
        for name in names:
            img = name
        return img
    def refresh_chat_data(self, *args):
        # self.event = Clock.schedule_interval(self.do_checks, 0.3)
        try:
            # req = UrlRequest('https://pmca-a03a7-default-rtdb.firebaseio.com/'+self.owner_no+'/chats.json', got_json)
            fil = requests.get('https://pmca-a03a7-default-rtdb.firebaseio.com/'+self.loginId+'/chats/.json')
            data = fil.json()
            with open(self.chat_file) as g:
                offline_chat_data = json.load(g)
            for chats in offline_chat_data:
                self.chat_number_list.add(chats)
            if data != None and data != "None":
                with open(self.database) as g:
                    database_info = json.load(g)
                for new_data in data:
                    if new_data not in self.chat_number_list:
                        for N in data[new_data]:
                            last_msg = data[new_data][N]
                        new_data_name = database_info[new_data]
                        #print("this is new chat number : ", new_data_name," <-> ",last_msg)
                        self.all_chats(new_data_name,last_msg)
                        self.chat_number_list.add(new_data)
                        #print("chat number Added")
                        with open(self.chat_file,'w') as C:
                            json.dump(data,C)
                    else:
                        print("All is well in Homepage")
            
        except requests.exceptions.RequestException:
            self.parent.Bottom_msg("Please Turn On Internet..")
    def new_count(self):
        C = UnreadMsgCount()
        Username_count,unread_msgs, last_msg = C.count(self.loginId)
        #print(Username_count,"----->",unread_msgs)
        for x in self.New_data_list:
            #print(x['text'])
            # if x['text'] == Username_count:
                # print(x['count_is'])
                # x['count_is'] = unread_msgs
            # print(x)
            if x['text'] == Username_count:
                # print(x['text']," : ",Username_count)
                # print(x['count_is']," : ", unread_msgs)
                x['count_is'] = unread_msgs
                x['secondary_text'] = last_msg[:-1]
                # print(self.New_data_list)
        self.ids.rv.data = self.New_data_list
        self.ids.rv.refresh_from_data()
    def threading_method(self,*args):
        #this method use threading in background and call the refresh method
        threading.Thread(target=self.refresh_chat_data).start()
        threading.Thread(target=self.new_count).start()
        # self.recall = Clock.schedule_interval(self.threading_method, 1) #every 1 sec all this method
    