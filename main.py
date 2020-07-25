from kivy.app import App; from kivy.uix.label import Label
from kivy.uix.button import Button; from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup; from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import json; import datetime; import plyer

plyer.tts.speak(message="Hello world!")

botles = 300
with open('data.json') as f:
    data = json.loads(f.read())

class WindowManager(ScreenManager):
    pass

class StatWindow(Screen, FloatLayout):
    mon=None

    def write_to_file(self):
        with open('data.json', 'w') as f:
            f.write(json.dumps(data))

    def on_enter(self):
        if not self.mon:
            self.mon = Label(text="", size_hint=(1,.1), pos_hint={'x':0,'y':.8})
            self.tue = Label(text="", size_hint=(1,.1), pos_hint={'x':0,'y':.7})
            self.wed = Label(text="", size_hint=(1,.1), pos_hint={'x':0,'y':.6})
            self.thu = Label(text="", size_hint=(1,.1), pos_hint={'x':0,'y':.5})
            self.fri = Label(text="", size_hint=(1,.1), pos_hint={'x':0,'y':.4})
            self.sat = Label(text="", size_hint=(1,.1), pos_hint={'x':0,'y':.3})
            self.sun = Label(text="", size_hint=(1,.1), pos_hint={'x':0,'y':.2})
            self.add_widget(self.mon); self.add_widget(self.tue); self.add_widget(self.wed); self.add_widget(self.thu)
            self.add_widget(self.fri); self.add_widget(self.sat); self.add_widget(self.sun)
        self.mon.text = f"Poniedziałek: {data['1']}"; self.tue.text = f"Wtorek: {data['2']}"
        self.wed.text = f"Środa: {data['3']}"; self.thu.text = f"Czwartek: {data['4']}"
        self.fri.text = f"Piątek: {data['5']}"; self.sat.text = f"Sobota: {data['6']}"
        self.sun.text = f"Niedziela: {data['7']}"

class MainWindow(Screen, FloatLayout):
    def write_to_file(self):
        with open('data.json', 'w') as f:
            f.write(json.dumps(data))

    def add_to_result(self, instance, label, label1, label2):
        global data
        if botles-data["botles"]>0:
            data["botles"] += 1
            data[str(data["day"])]+=1

            self.write_to_file()

            label.text = f"Butelki wypite dzisiaj: {data[str(data['day'])]}"
            label1.text = f"Wypite butelki wody: {data['botles']}"
            label2.text = f"Pozostało do zmiany filtra: {botles-data['botles']}"
        else:
            pop = Popup(title='FILTR', content=Label(text="Najwyższa pora wymienić filtr"), size_hint=(.9,.7))
            pop.open()

    def reset_result(self, instance, label1, label2):
        global data
        data["botles"] = 0

        self.write_to_file()

        label1.text = f"Wypite butelki wody: {data['botles']}"
        label2.text = f"Pozostało do zmiany filtra: {botles-data['botles']}"

class WaterApp(App, FloatLayout):
    def read_from_file(self):
        with open('data.json') as f:
            drunk = json.loads(f.read())["botles"]
        return drunk

    def write_to_file(self):
        with open('data.json', 'w') as f:
            f.write(json.dumps(data))

    def on_start(self):
        global day
        if data["day"]!=day+1:
            data["day"] = day+1
            if data["day"]==1:
                for i in range(1,8):
                    data[str(i)]=0
            self.write_to_file()


    def build(self):
        global day
        import datetime as dt
        self.data = data
        self.day = dt.datetime.now().weekday()
        day = self.day
        self.botles = botles
        self.drunk = data["botles"]
        return WindowManager()

WaterApp().run()
