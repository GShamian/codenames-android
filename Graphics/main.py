import kivy 
from kivy.app import App 
from kivy.lang import builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass

class MyScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.current = '_first_screen_'

    def screen_switch_one(self, dt):
        self.current = '_first_screen_'

    def screen_switch_two(self, dt):
        self.current = '_second_screen_'

class SwitchingScreenApp(App):
    sm = ObjectProperty(None)

    def build(self):
        SwitchingScreenApp.sm = ScreenManager()
        
        ws = FirstScreen(name="_first_screen_")
        os = SecondScreen(name="_second_screen_")

        self.sm.add_widget(ws)
        self.sm.add_widget(os)
        return self.sm

if __name__ == "__main__":
    SwitchingScreenApp().run()        