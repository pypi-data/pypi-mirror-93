#Label Graphics
import kivy
from kivy.uix.label import Label as lb

class Label():
    def label(self,text=str,font_size=None):
        if font_size is None:
            font_size=15
        else:
            pass
        return lb(text=text,font_size=font_size)