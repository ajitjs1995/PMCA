import requests
import json

class UnreadMsgCount():        
    latest_msg = {}
    offline_count = {}
    online_count = {}
    new_count = 0
    
    def count(self,own):
        with open('Json_Files/ChatHub.json','r') as f:
            offline_chats = json.load(f)
        with open('Json_Files/database.json','r') as f:
            database_data = json.load(f)
        count = 0
        last_msg =''
        # print(self.owner_number,self.get_res.ok, self.online_data)
        d = requests.get('https://pmca-a03a7-default-rtdb.firebaseio.com/'+own+'/chats/.json')
        online_data = d.json()
        # print(online_data)
        for numbers in offline_chats:
            for key in offline_chats[numbers]:
                # print(key)
                count = 1+count
            username = database_data[numbers]
            self.offline_count[username]=count
            count=0
            # print("offline --> ",numbers,"-->",self.offline_count)
        for online in online_data:
            # print(online_data[online])
            for key in online_data[online]:
                last_msg = online_data[online][key]
                count = 1+count
            # print(online,"-->",last_msg)
                # for last in key:
                #     last_msg = last[last]
            on_user = database_data[online]
            self.latest_msg[on_user]=last_msg
            self.online_count[on_user]=count
            count=0
       
        new_count = 0
        for x in self.online_count:
            if self.online_count[x] != self.offline_count[x]:
                new_count = self.online_count[x] - self.offline_count[x]
                user = x
                print(x,"-->",new_count)
                last_msg = self.latest_msg[x]
                self.new_count = new_count
                return user, new_count, last_msg
            else:
                user = x
                new_count = 0
                last_msg = self.latest_msg[x]
                self.new_count = new_count
                return user, new_count , last_msg