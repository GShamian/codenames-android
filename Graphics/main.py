from kivy.config import Config
MAX_SIZE = (500, 1050)
Config.set('graphics', 'width', MAX_SIZE[0])
Config.set('graphics', 'height', MAX_SIZE[1])
from kivy.core.window import Window
import kivy
import Global
import client
import time
import threading
import time
from kivy import *
from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label 
from kivy.uix.popup import Popup
from kivymd.theming import ThemeManager
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget

Global.background_music.play()
sm = ScreenManager()
Playground_Screen = kivy.properties.ObjectProperty(None)

class MainScreen(Screen):
    def on_enter(self):
        if(Global.isFirstGame == 'true'):
            sm.remove_widget(sm.get_screen('playground'))
            Global.isFirstGame = 'false'

    def isAdmin_change(self, flag):
        Global.isAdmin = flag
    def push_button_sound(self):
        Global.button_sound.play()

class OptionsScreen(Screen):
    def push_button_sound(self):
        Global.button_sound.play()

    def change_music_volume(self, value):
        Global.background_music.volume = value/10

    def change_sound_of_push_volume(self, value):
        Global.button_sound.volume = value/10
    

class CreateLobbyScreen(Screen):
    playground_screen = 0
    label_spyamount = kivy.properties.ObjectProperty(None)

    def push_button_sound(self):
        Global.button_sound.play()

    def appear_token(self):
        Global.data = client.createLobby(Global.players_amount, Global.spy_amount)
        Global.token = Global.data[0]
        self.token_layout.token_button.font_size = 60
        self.token_layout.token_button.texture_update()
        self.token_layout.token_button.text = Global.token
        self.play_button_layout.play_button.disabled = False
        Playground_Screen = PlaygroundScreen(name = 'playground')
        sm.add_widget(Playground_Screen)
        
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
        Global.button_sound.play()    

    def enter_game(self, tokdef = ''):
        self.token_code = tokdef
        if(self.token_code != ''):
            Global.data = client.connect(self.get_token())
            Global.token = self.get_token()
            if(Global.data == 'invalid token'):
                layout = GridLayout(cols = 1, padding = 15, spacing = 15) 
                label__text = Label(text = 'Invalid Token.\nTry Again') 
                layout.add_widget(label__text) 
                popup = Popup(title ='Error', 
                             content = layout, 
                             size_hint =(None, None), size =(200, 100))   
                popup.open()
            else:
                Playground_Screen = PlaygroundScreen(name = 'playground')
                sm.add_widget(Playground_Screen)
                sm.current = 'playground'

    def get_token(self):
        return self.token_code.upper()
    pass

class PlaygroundScreen(Screen):
    locations = []
    role = ''
    key_location = ''
    scrn = ''

    def push_button_sound(self):
        Global.button_sound.play()

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
            my_button = Button(text=self.locations[i], on_press=self.location_press, background_normal = 'Playground Menu/empty_location_logo.png', background_down = 'Playground Menu/empty_location_logo.png')
            self.grid.add_widget(my_button)
        print(self.key_location)

    def game_process(self):
        gameCheck_status = threading.Thread(target=self.gameOver_update, daemon=True)
        gameCheck_status.start()

    def gameOver_update(self):
        while(Global.gameOver == 'true'):
            Global.gameOver = client.checkGameStatus(Global.token)
            time.sleep(1)
        Global.gameOver = 'true'
        self.gameOver_popup()
        
    def location_press(self, instance):
        if(self.role == 'spy'):
            client.checkLocation(Global.token, instance.text)

    def gameOver_popup(self):
        layout = GridLayout(cols = 1, padding = 10) 
        label_gameOver = Label(text = 'Game Over') 
       
        layout.add_widget(label_gameOver) 
 
        popup = Popup(title ='Congratz', 
                      content = layout, 
                      size_hint =(None, None), size =(250, 200))   
        popup.bind(on_dismiss=self.goto_Main)
        popup.open()

    def goto_Main(self, instance):
        Global.isFirstGame = 'true'
        sm.current = 'main'

    def rolePopup(self): 
        layout = GridLayout(cols = 2, padding = 10)
        label__role_text = Label(text = 'Role: ') 
        label_role = Label(text = self.role.upper()) 
        label__location_text = Label(text = 'Location: ') 
        label__location = Label(text = self.key_location.upper()) 

        layout.add_widget(label__role_text) 
        layout.add_widget(label_role)
        if(self.role == 'peaceful'):
            layout.add_widget(label__location_text)
            layout.add_widget(label__location)
  
        popup = Popup(title ='Role', 
                      content = layout, 
                      size_hint =(None, None), size =(350, 300))   
        popup.open()
        self.game_process()

class SpyFallApp(MDApp):
    def __init__(self, **kwargs):
        self.title = 'SpyFall'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        super().__init__(**kwargs)

    def build(self):
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(OptionsScreen(name='options'))
        sm.add_widget(CreateLobbyScreen(name='createlobby'))
        sm.add_widget(ConnectScreen(name='connect'))
        return sm

if __name__ == '__main__':
    SpyFallApp().run()
    