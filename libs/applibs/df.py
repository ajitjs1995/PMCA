from kivy.core.window import Window
from kivy.app import App
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
# from libs.uix.baseclass.chat_room import Chat_Room_Screen


# KV = '''
# BoxLayout:
#     orientation: 'vertical'

#     MDToolbar:
#         title: "MDFileManager"
#         left_action_items: [['menu', lambda x: app.true_call()]]
#         elevation: 10

#     FloatLayout:

#         MDRoundFlatIconButton:
#             text: "Open manager"
#             icon: "folder"
#             pos_hint: {'center_x': .5, 'center_y': .6}
#             on_release: app.file_manager_open()
# '''


class Example(MDFileManager):
    # cr =Chat_Room_Screen()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
            show_hidden_files=True,
        )

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True
    def true_call(self):
        self.file_manager.preview = True
    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.exit_manager()
        app = App.get_running_app()
        # self.preview = True
        app.screen_manager.get_screen("chat_room").media_image(path,' ')
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
