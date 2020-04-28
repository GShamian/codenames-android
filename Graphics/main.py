import kivy
import Global
import client
from kivy import *
from io import open
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label 
from kivy.uix.popup import Popup
from kivymd.theming import ThemeManager
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader


Global.sound1.play()

class ScreenManagement(ScreenManager):
    create_scrn = kivy.properties.ObjectProperty(None)

class MainScreen(Screen):
    def isAdmin_change(self, flag):
        Global.isAdmin = flag
    def push_button_sound(self):
        Global.sound2.play()

class OptionsScreen(Screen):
    def push_button_sound(self):
        Global.sound2.play()

    def change_music_volume(self, value):
        Global.sound1.volume = value/10

    def change_sound_of_push_volume(self, value):
        Global.sound2.volume = value/10
    

class CreateLobbyScreen(Screen):
    playground_screen = 0
    label_spyamount = kivy.properties.ObjectProperty(None)

    def push_button_sound(self):
        Global.sound2.play()

    def appear_token(self):
        Global.data = client.createLobby(Global.players_amount, Global.spy_amount)
        Global.token = Global.data[0]
        self.token_layout.token_button.text = Global.token
        
    def add_spy(self):
        if(Global.spy_amount == 4):
            Global.spy_amount = 0
        Global.spy_amount += 1
        self.ids.lbl_spy.text = str(Global.spy_amount)
        print(Global.spy_amount)

    def delete_spy(self):
        if(Global.spy_amount == 0):
            Global.spy_amount = 1
        Global.spy_amount -= 1
        self.ids.lbl_spy.text = str(Global.spy_amount)
        print(Global.spy_amount)

    def my_value(self, value):
        Global.players_amount = value

class ConnectScreen(Screen):
    token_code = kivy.properties.StringProperty('')

    def push_button_sound(self):
        Global.sound2.play()    

    def enter_game(self, tokdef = ''):
        self.token_code = tokdef
        if(self.token_code != ''):
            Global.data = client.connect(self.get_token())

    def get_token(self):
        return self.token_code
    pass

class PlaygroundScreen(Screen):
    locations = []
    role = ""
    key_location = ""

    def push_button_sound(self):
        Global.sound2.play()

    def enter_screen(self):
        if(Global.isAdmin == False):
            self.role = Global.data[0]
            self.key_location = Global.data[1]
            self.locations = Global.data[2]
        else:
            self.role = Global.data[1]
            self.key_location = Global.data[2]
            self.locations = Global.data[3]
        for i in range(16):
            self.grid.add_widget(Button(text=self.locations[i]))

    def rolePopup(self): 
        layout = GridLayout(cols = 2, padding = 10) 
        label__role_text = Label(text = "Role: ") 
        label_role = Label(text = self.role.upper()) 
        label__location_text = Label(text = "Location: ") 
        label__location = Label(text = self.key_location.upper()) 
  
        layout.add_widget(label__role_text) 
        layout.add_widget(label_role)
        if(self.role == 'peaceful'):
            layout.add_widget(label__location_text)
            layout.add_widget(label__location)
  
        popup = Popup(title ='Role', 
                      content = layout, 
                      size_hint =(None, None), size =(250, 200))   
        popup.open()


class SwitchingScreenApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "SpyFall"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        super().__init__(**kwargs)

    def build(self):
        return ScreenManagement()

if __name__ == "__main__":
    SwitchingScreenApp().run()
    