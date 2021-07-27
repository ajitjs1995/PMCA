from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
import time
kv = '''
<Content>:
    adaptive_height: True
    # size: 20, 80
    spacing: dp(10)
    MDSpinner:
        size_hint: (None, None)
        size: (dp(46), dp(46))
        pos_hint: {'x': 1, 'y': .5}
        active: True
        palette:
            [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],             [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],             [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],             [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
    MDLabel:
        text: " Collecting Data...."
        pos_hint: {'x': 1, 'y': .5}
        

            
'''
class Content(MDBoxLayout):
    Builder.load_string(kv)

class Dialog_case(MDBoxLayout):       
    def open_dlg(self):
        dialog = None
        
        self.dialog = MDDialog(
        # text="This will reset your device to its default factory settings.",
        type= "custom",
        content_cls=Content()
        )
        self.dialog.open()
       
    def close_dlg(self):
        self.dialog.dismiss()
