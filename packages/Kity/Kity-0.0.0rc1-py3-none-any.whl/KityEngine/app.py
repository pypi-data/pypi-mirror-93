#Main app Initializer
import kivy
from kivy.app import App as kivyapp
from kivy.uix.label import Label as label_widget
from kivy.uix.widget import Widget
from kivy.lang import Builder as builder

class MyLayout(Widget):
    pass

class KityEngineApp(kivyapp):
    kitywidget=label_widget(text='')
    kf=None
    def AddWidget(self,widget=None):
        self.kitywidget = None
        if widget:
            self.kitywidget = widget
        else:
            self.kitywidget=label_widget(text='')
    def edit_title(self,title=None):
        self.heading_custom=None
        if title is None:
            self.heading_custom="KityEngine"
        else:
            self.heading_custom=title
    def builder_data(self,kf):
        self.kf=kf
    def build(self):
        self.title=self.heading_custom
        file=self.kf
        if file is None:
            pass
        else:
            builder.load_file(file)
        now=MyLayout() if file is not None else self.kitywidget
        return now 

class App():
    def __init__(self,title=None,prog=None):
        self.KityEngine=KityEngineApp()
        self.KityEngine.edit_title(title)
        if prog is None:
            pass
        else:
            self.KityEngine.builder_data(prog)
    def AddWidget(self,widget):
        self.KityEngine.AddWidget(widget=widget)
    def run(self):
        self.KityEngine.run()
