from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.floatlayout import MDFloatLayout
from libs.applibs.profile_preview_dialog import ProfilePreview
import kivymd_extensions.akivymd



Builder.load_string(
    """
<MyAKBadgeLayout@AKBadgeLayout>
    # pos_hint: {"center_x": .5, "center_y": .5}
    badgeitem_padding: dp(5)
    bold: True
<ChatListItem>
    adaptive_height: True
    padding: dp(2)
    spacing: dp(10)
    MyAKBadgeLayout:
        id: count
        text: str(root.count_is)
        badgeitem_color: 0, 1, 0, 0.6
        # position: "left"
        offset: 0.40
        badge_disabled: False if root.count_is != 0 else True
        FitImage:
            id: img
            source: root.image
            size_hint: None, None
            size: dp(40), dp(40)
            radius: [self.width/2,]
            pos_hint: {'center_y': .5}
            on_touch_down:
                if self.collide_point(*args[1].pos): root.open_dialog()

    # MDBoxLayout:
    #     orientation: 'vertical'
    #     pos_hint: {'center_y': .5}
    #     # spacing: dp(5)
    #     adaptive_height: True
    TwoLineListItem:
        text: root.text
        secondary_text: root.secondary_text
        on_release: app.screen_manager.get_screen("home").chat_room(self.text)
       
        # MDLabel:
        #     text: root.text
        #     font_style: 'Subtitle1'
        #     adaptive_height: True
            

        # MDLabel:
        #     text: root.secondary_text
        #     font_style: 'Body2'
        #     theme_text_color: 'Secondary'
        #     adaptive_height: True
    
    # MDLabel:
    #     text: root.time
    #     font_style: 'Caption'
    #     theme_text_color: 'Secondary'
    #     adaptive_size: True
    #     pos_hint: {'center_y': .45}

"""
)


class ChatListItem(MDBoxLayout):

    text = StringProperty()

    secondary_text = StringProperty()

    image = StringProperty()

    time = StringProperty()

    count_is = NumericProperty()

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def open_dialog(self):
        ProfilePreview().fire(title=self.text, image=self.image)
