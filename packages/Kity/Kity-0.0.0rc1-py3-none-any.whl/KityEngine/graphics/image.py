#Image Graphics
import kivy
from kivy.uix.image import Image as img

class Image():
    def show(self,source=str):
        return img(source=source)