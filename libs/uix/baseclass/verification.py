from main_imports import MDScreen
from libs.applibs import utils

utils.load_kv("verification.kv")

class Verification_Screen(MDScreen):
    def redirect_p(self,p):
        D = self.parent.get_screen("login").validate(p)
        if D == True:
            self.parent.change_screen("home")
            self.ids.pa.text = ''
        else:
            self.parent.Bottom_msg("Please Enter Correct Password")
            self.ids.pa.text = ''
