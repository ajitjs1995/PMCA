from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import BaseDialog

Builder.load_string(
    """
#: import gch kivy.utils.get_color_from_hex

<ProfilePreview>
    auto_dismiss: True
    orientation: 'vertical'
    adaptive_size: True

    MDLabel:
        text: root.title if root.title != '' else " "
        theme_text_color: 'Custom'
        text_color: 1, 1, 1, 1
        padding: [dp(5), dp(5)]
        adaptive_height: True

        canvas.before:
            Color:
                rgba: gch('3a3b3c') if root.view == "profile" else [0,0,0,0]
            Rectangle:
                size: self.size
                pos: self.pos

    FitImage:
        id: image
        source: root.image
        size_hint: None, None
        width: btn_box.width
        height: btn_box.width

    MDBoxLayout:
        id: btn_box
        md_bg_color: [1, 1, 1 , 1] if root.view == "profile" else [0,0,0,0]
        adaptive_height: True
        size_hint_x: None
        width: self.minimum_size[0] + dp(40)

        Widget:

        DialogIconButton:
            icon: 'android-messages' if root.view == "profile" else ""

        DialogIconButton:
            icon: 'phone' if root.view == "profile" else ""

        DialogIconButton:
            icon: 'video' if root.view == "profile" else ""

        DialogIconButton:
            icon: 'information-outline' if root.view == "profile" else "delete-forever"
            on_release: None if root.view == "profile" else root.del_image(image.source) 

        Widget:

<DialogIconButton@MDIconButton>
    theme_text_color: 'Custom'
    text_color: self.theme_cls.accent_color
"""
)


class ProfilePreview(MDBoxLayout, BaseDialog):

    title = StringProperty()

    image = StringProperty()

    view = StringProperty()

    def fire(self, title, image):
        if title == '':
            self.view = "chat"
        else:
            self.view = "profile"
        self.title = title
        self.image = image
        self.open()
    def del_image(self,del_path):
        print(del_path)
