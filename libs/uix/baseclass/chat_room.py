from main_imports import  MDScreen, UrlRequest, MDGridBottomSheet
from kivymd.uix.chip import MDChip
from kivymd.uix.filemanager import MDFileManager
from libs.applibs.df import Example
#kivy Imports
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.animation import Animation

from libs.applibs import utils #helps to add file with there class name 
from libs.applibs.profile_preview_dialog import ProfilePreview
from libs.applibs.Image_up_down import Image_fire

#python Import 
import json
import os
import requests
import threading
import datetime
import shortuuid
# import shutil
import time as Time
Clock.max_iteration = 20
utils.load_kv("chat_room.kv")


class Chat_Room_Screen(MDScreen):
    chat_room_no = '' #use to store chat person number
    owner_no = '' # Use to store OWN number
    url = ""      #Use to store MSG Url
    check_set = set() 
    compare_set =set() # compare set live 
    local_set =set() #compare local set
    Image = Image_fire()
    new_data = {}
    
    def on_enter(self, *args):
        # On Entering the Chat Screen this method runs
        self.owner_no = self.parent.get_screen("home").loginId #OWNer Number
        self.use = self.ids.profile_bar.title
        self.chat_room_no = self.get_key(self.use)
        file = requests.get('https://pmca-a03a7-default-rtdb.firebaseio.com/'+self.owner_no+'/chats/'+self.chat_room_no+'/.json')
        data = file.json()  
        with open('Json_Files/ChatHub.json','r') as f:
            chats = json.load(f)
        self.new_data = chats
        self.new_data[self.chat_room_no] = data
        with open('Json_Files/ChatHub.json','w') as C:
            json.dump(self.new_data,C)
              
        # with open('Json_Files/database.json','r') as f: 
        #     numbers_show = json.load(f)
        if os.path.getsize('Json_Files/ChatHub.json') != 0: #if chat is not empty
            if chats=="None":
                print("no dont have")
                # self.search_chat_room(self.chat_room_no)
            else:
                chat_data = ''
                if self.chat_room_no != str :
                    try:
                        chat_data = chats[self.chat_room_no]
                    except KeyError:
                        pass         
                else:
                    try:
                        numb=self.get_key(self.chat_room_no)
                        chat_data = chats[numb]            
                    except:
                        pass
                if chat_data != '':
                    for key,value in chat_data.items(): # identify the Recieved and sent Msgs                        
                        #print("This is date",key)                    
                        self.local_set.add(key)                    
                        v = value
                        vl = v[-1]                    
                        if vl == "1":
                            self.rx_msg(v,key)
                        elif vl == "0":
                            self.send_msg(v,key)
                        else:
                            self.media_image(v,key)
                        #print("This is time",key)
                        #print("This is msg",v)
                else:
                    pass
                self.up_set()
        else: 
            print("no Chat data Available")
        self.recall = Clock.schedule_interval(self.threading_method, 1) #every 1 sec all this method 
    def threading_method(self,*args):
        #this method use threading in background and call the refresh method
        threading.Thread(target=self.refresh_chat_data).start()

    def up_set(self):
        # use to update all the Urls global Variables
        self.url = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats/"+self.chat_room_no+"/.json"            
        self.url_date = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats/"+self.chat_room_no+"/"+str(datetime.date.today())+".json"            
        self.check = UrlRequest(url=self.url,on_success=self.res,on_progress=print("url : ",self.url ))            
    def get_key(self,use):
        #use to get keys 
        with open('Json_Files/database.json','r') as f:
            data = json.load(f)
        for key, value in data.items():
            if use == value:
                return key
        return "key does not exist"
    def chat_textbox(self):
        """
            MDCard size change when MSGbox use multilines.
            MDCard y axis size incress when MSGbox y axis size incress
        """
        fixed_Y_size = self.ids.root_chatroom.size[1]/3
        msg_textbox=self.ids.msg_textbox.size
        
        if msg_textbox[1] <= fixed_Y_size:
            
            self.ids.send_card.size[1]=msg_textbox[1]
            #print(msg_textbox)
        else:
            self.ids.send_card.size[1]=fixed_Y_size
        
        
    def media_image(self,image_path,i):
        #print(image_path,i,self.ids.rv.viewclass)
        self.img_path = image_path
        self.ids.rv.viewclass = 'Img'
        if i == ' ':
            now = datetime.datetime.now()
            i = now.strftime("%H:%M:%S")
        if image_path[-1]=='@':
            #write code to put in UI
            image_path = image_path[0:len(image_path)-1]+'.jpg'
            time = i[-8:-3]+" "+i[-10:-8]+"-"+i[5:7]+"-"+i[0:4]
            pre_data = {"text":"","side":"right","time":time,"img":image_path,"status":"img"}
            self.ids.rv.data.append(pre_data)
            #print("if done..",pre_data)
            self.ids.rv.viewclass = 'Card'
        elif image_path[-1]=='#':
            #write code to put in UI
            image_path = image_path+'.jpg'
            time = i[-8:-3]+" "+i[-10:-8]+"-"+i[5:7]+"-"+i[0:4]
            pre_data = {"text":"","side":"left","time":time,"img":image_path,"status":"img"}
            self.ids.rv.data.append(pre_data)
            #print("if done..",pre_data)
            self.ids.rv.viewclass = 'Card'
        else:
            #update to the Database and put in UI
            image_path1 = image_path + '@'
            # print("Image Date time: ",now," Name: ",image_path1)
            time = i[-8:-3]+" "+i[-10:-8]+"-"+i[5:7]+"-"+i[0:4]
            # self.ids.all_msgs.spacing =  "130dp"   
            pre_data = {"text":"","side":"right","time":time,"img":image_path,"status":"img"}
            self.ids.rv.data.append(pre_data)            
            self.ids.rv.viewclass = 'Card'                        
            Img_nam = shortuuid.uuid()
            self.Img_name = Img_nam            
            self.image_threading_method()
            time = i
            date = datetime.date.today()
            date = str(date)
            #print(date,time, " ---> " ,self.Img_name+'@')
            threading.Thread(target=self.update_database(date,time,self.Img_name+'@')).start()
            
    def image_threading_method(self,*args):
        #this method use threading in background and call the refresh method
        # Image = Image_fire()
        cloud_path = 'Transfer/'+self.Img_name+'@'
        img_path =self.img_path
        # Image.upload_Image(cloud_path,img_path)
        threading.Thread(target=self.Image.upload_Image(cloud_path,img_path)).start()
    # def image_store_local(self,original_path,I_name):
    #     # Use this to store sent Image in chat_media/sent/ folder
    #     target_path = 'chat_media\sent\I_name'
    #     shutil.copyfile(original_path, target_path)
    #     # threading.Thread(target=Image.upload_Image(cloud_path,img_path)).start()


    def send_msg(self,msg_data,i):
        """
            When send button use to send msg this function call
            and clear MSGbox 
        """        
        if msg_data[-1] == '0' or msg_data[-1] == '1':
            msg_data = msg_data
        else:
            msg_data = msg_data + '0'
        #print(" i am in send msg",i[:-8]," ",i[-8:-3])
        time = i[-8:-3]+" "+i[-10:-8]+"-"+i[5:7]+"-"+i[0:4]
        msg_data = msg_data[0:len(msg_data)-1] # this is Msg
        
        pre_data = {"text":msg_data,"side":"right","time":time,"img":"","status":"msg"}
        self.ids.rv.data.append(pre_data)
        
        self.ids.msg_textbox.text=""
        #print("This is sent end....")
    def send_msg_btn(self,msg_data,i):
        if i == '':
            now = datetime.datetime.now()
            i = now.strftime("%H:%M:%S")
        if msg_data.strip() != "":
            # Time 
            time = i[-8:-3]+" "+i[-10:-8]+"-"+i[5:7]+"-"+i[0:4]
            pre_data = {"text":msg_data.strip(),"side":"right","time":time,"img":"","status":"msg"}
            self.ids.rv.data.append(pre_data)            
            self.ids.msg_textbox.text=""
            date = datetime.date.today()
            date = str(date)
            time = i
            self.update_database(date,time,msg_data)
        else:
            self.parent.Bottom_msg("Msg Could not be Empty")
    def update_database(self,date,time,msg):
        if msg[-1]=='@':
            msg_o = 'chat_media/sent/'+msg +'#'
            #print("msg_o ----> ", msg_o)
        else:
            msg_o = msg.strip()+'0'        
            #print(msg)
        same_date = {
                date + time: msg_o
                }
        #print('send_data ---->', same_date)
        try:
            """
            # This is if the chat data is separated by date
            if date == self.check_set:
                print("i am going to requests")
                requests.patch(self.url_date,json = same_date)
                # UrlRequest(url=url,req_body=file,on_success=print("data transfer"))
            else:
                """
            s = requests.patch(self.url,json = same_date)
            #print("Try Patch Request--->",s.ok)
            # write a code to save or send the same msg to RXer
            # msg = msg[:len(msg)-1]+'#'
            self.RXer_update(date,time,msg)
            # RXer code ends here
            self.parent.Bottom_msg("Updated")
        except requests.exceptions.RequestException as e:
            #print("---From Upadte_database---",self.url)
            self.search_chat_room(self.chat_room_no)
            s_url ="https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats/"+self.chat_room_no+"/.json"
            s = requests.patch(s_url,json = same_date)
            #print("Except patch ---->",s.ok)
            # msg = msg[:len(msg)-1]+'#'
            self.RXer_update(date,time,msg)
            self.parent.Bottom_msg("Please Turn On Internet..")
        # self.refresh_chat_data()
    def RXer_update(self,date,time,msg):
        """
        This function Helps to reflect same msg to other side
        """
        #print("in Rx_Upsdate...")
        if msg[-1]=='#':
            msg_r = 'chat_media/'+msg
        else:
            msg_r = msg.strip()+"1"
        r_chat = requests.get("https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.chat_room_no+"/chats/.json")
        # print()
        if r_chat.ok==True and r_chat.json() == "None":
            patch={
                   date + time: msg_r
                }
            data = {
                self.owner_no:patch
            }
            c_url = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.chat_room_no+"/chats/.json"
            #print("making patch in RX---")
            requests.patch(c_url,json = data)
        elif r_chat.ok == True and self.owner_no in r_chat.json().keys():
    
            url = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.chat_room_no+"/chats/"+self.owner_no+"/.json"
            data_d = {
                date + time: msg_r
            }
            #print("Rx ---->", data_d)
            requests.patch(url,json = data_d) 
            # json_data = r_chat.json()            
        elif r_chat.ok == True and self.owner_no not in r_chat.json().keys():
    
            url = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.chat_room_no+"/chats/"+self.owner_no+"/.json"
            data_d = {
                date + time: msg_r
            }
            #print("Rx ---->", data_d)
            requests.patch(url,json = data_d)            
            # json_data = r_chat.json()           
    def res(self,*args):
        # print("Result: after success", self.check.result.keys())
        if self.check.result != None:
            for c in  self.check.result.keys():
                self.check_set.add(c)
            #print(self.check_set)
    # def got_json(self,req, result):
    #     for key, value in req.resp_headers.items():
    #         self.compare_set.append('{}: {}'.format(key, value))
    #     #print(self.compare_set.count())
    def refresh_chat_data(self, *args):
        # self.event = Clock.schedule_interval(self.do_checks, 0.3)
        try:
            # req = UrlRequest('https://pmca-a03a7-default-rtdb.firebaseio.com/'+self.owner_no+'/chats.json', got_json)
            fil = requests.get('https://pmca-a03a7-default-rtdb.firebaseio.com/'+self.owner_no+'/chats/'+self.chat_room_no+'/.json')
            data = fil.json()
            if data != None:
                for d in data:
                    self.compare_set.add(d)
                if len(self.local_set)<len(self.compare_set):
                    # Appending New msg in chat Room
                    key1 = self.compare_set.difference(self.local_set)
                    for key in key1:
                        key1 = key
                    Msg_data = data[key1]
                    self.local_set.add(key1)
                    #print("data is more ",data[key1])
                    if Msg_data[-1] == "1" or Msg_data[-1] == '#':
                        self.rx_msg(Msg_data,key1)                    
                else:
                    print("all is normal")
            
        except requests.exceptions.RequestException:
            self.parent.Bottom_msg("Please Turn On Internet..")
       
    def rx_msg(self,msg_data,i):
        """
            This recieves msg from data base or local file 
        """
        if msg_data[-1] == '1':
            msg_data = msg_data[0:len(msg_data)-1] # this is Msg
            status = "msg"
            image_path = ""
        elif msg_data[-1] == '#':
            I_name = msg_data[11:]
            cloud_path = 'Transfer/'+ I_name
            target_path = msg_data[:11]
            self.Image.download_Image(cloud_path,target_path,I_name)
            image_path = msg_data+".jpg" # this is Img
            msg_data = ""
            status = "img"
            #print("sleep startes")
            # Time.sleep(2)
            #print("This is Img path from DB--->",image_path)
        time = i[-8:-3]+" "+i[-10:-8]+"-"+i[5:7]+"-"+i[0:4]
        pre_data = {"text":msg_data,"side":"left","time":time,"img":image_path,"status":status}
        self.ids.rv.data.append(pre_data)
        
        self.ids.msg_textbox.text=""
    def search_chat_room(self,number):
        # Use this fuction for search chat room or blank chat room
        self.u_url = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats/.json"        

        data = {
            number : " "
        }
        requests.patch(self.u_url,json = data)
        
        #print("This is the search chat_room of ",number)

    def feachers(self):
        """
        method call when plus btn click .
        
        """
        fm = Example()
        bottom_sheet_menu = MDGridBottomSheet(
            animation=True,
        )
        data = {
            "Upload": "cloud-upload",
            "Camera": "camera",
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],#       
                lambda x, y=item[0]: fm.file_manager_open(), #self.parent.get_screen("profile").file_manager_open(),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()
    
    def open_dialog(self,text,img):
        ProfilePreview().view = "chat"
        ProfilePreview().fire(title=text, image=img)
        # ProfilePreview().view = "profile"

    def scroll_bottom(self):
        rv = self.ids.rv
        box = self.ids.all_msgs
        #print(rv.height,box.height,"<-->",rv.scroll_y)
        if rv.height < box.height:
            Animation.cancel_all(rv, 'scroll_y')
            Animation(scroll_y=0, t='out_quad', d=.5).start(rv)

    def on_leave(self, *args):
        self.ids.rv.data = []
        url1 = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats.json"  
        self.recall.cancel()      
        try:
            all_chats = requests.get(url1)
            chats_data = all_chats.json()
            with open('Json_Files/ChatHub.json','w') as C:
                json.dump(chats_data,C)
        except requests.exceptions.RequestException:  # This is the correct syntax
            # Offline code goes here.. Load the ChatHub.json file to Screen
            print("You are Offline")              