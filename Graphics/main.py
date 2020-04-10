import kivy 
from kivy.app import App 
from kivy.lang import builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty, \
    NumericProperty,\
    StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass

class ThirdScreen(Screen):
    spy_amount = NumericProperty(0)
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
    pass

class FourthScreen(Screen):
    token_code = StringProperty('')
    def print_token(self, tokdef = ''):
        self.token_code = tokdef
        if(self.token_code != ''):
            print(self.get_token())
    def get_token(self):
        return self.token_code
    pass


class SwitchingScreenApp(App):
    sm = ObjectProperty(None)
    

    def build(self):
        
        SwitchingScreenApp.sm = ScreenManager()
        
        ws = FirstScreen(name="_first_screen_")
        os = SecondScreen(name="_second_screen_")
        crs = ThirdScreen(name="_third_screen_")
        cos = FourthScreen(name="_fourth_screen_")
        
        self.sm.add_widget(ws)
        self.sm.add_widget(os)
        self.sm.add_widget(crs)
        self.sm.add_widget(cos)
        return self.sm

if __name__ == "__main__":
    
    SwitchingScreenApp().run()
    