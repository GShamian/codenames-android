import kivy 
import client
from kivy import *
from io import open
from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label 
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.clock import Clock
#from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivymd.toast.kivytoast import toast
from kivymd.theming import ThemeManager
from kivymd.app import MDApp



class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass

class ThirdScreen(Screen):

    spy_amount = kivy.properties.NumericProperty(0)
    players_amount = kivy.properties.NumericProperty(0)

    def add_spy(self):
        if(self.spy_amount == 4):
            self.spy_amount = 0
        self.spy_amount += 1
        print(self.spy_amount)

    def delete_spy(self):
        if(self.spy_amount == 0):
            self.spy_amount = 1
        self.spy_amount -= 1
        print(self.spy_amount)

    def my_value(self, value):
        self.players_amount = value

    def play(self):
        client.createLobby(self.players_amount, self.spy_amount)
    pass

class FourthScreen(Screen):
    token_code = kivy.properties.StringProperty('')

    def print_token(self, tokdef = ''):
        self.token_code = tokdef
        if(self.token_code != ''):
            print(self.get_token())

    def get_token(self):
        return self.token_code
        
    pass

class FifthScreen(Screen):

    def rolePopup(self): 
          
        layout = GridLayout(cols = 1, padding = 10) 
        popupLabel = Label(text = "Role: ") 
        popupLabel2 = Label(text = "Location: ") 
  
        layout.add_widget(popupLabel) 
        layout.add_widget(popupLabel2)       
  
        popup = Popup(title ='Role', 
                      content = layout, 
                      size_hint =(None, None), size =(200, 200))   
        popup.open()
    pass


class RoleScreen(Screen):
    pass


class SwitchingScreenApp(MDApp):
    screen_manager = kivy.properties.ObjectProperty(None)

    def __init__(self, **kwargs):
        self.title = "SpyFall"
        self.theme_cls.theme_style = "Dark"
        super().__init__(**kwargs)

    def build(self):
        SwitchingScreenApp.screen_manager = ScreenManager()
        
        welcome_screen = FirstScreen(name="_first_screen_")
        options_screen = SecondScreen(name="_second_screen_")
        create_screen = ThirdScreen(name="_third_screen_")
        connection_screen = FourthScreen(name="_fourth_screen_")
        playground_screen = FifthScreen(name="_fifth_screen_")
        
        self.screen_manager.add_widget(welcome_screen)
        self.screen_manager.add_widget(options_screen)
        self.screen_manager.add_widget(create_screen)
        self.screen_manager.add_widget(connection_screen)
        self.screen_manager.add_widget(playground_screen)
        return self.screen_manager

if __name__ == "__main__":
    
    SwitchingScreenApp().run()
    