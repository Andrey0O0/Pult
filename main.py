from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from functools import partial
from kivy.uix.popup import Popup
import socket
from android.permissions import request_permissions, Permission



def send_p():
    global connect_ip, part

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((connect_ip, 1002))

    file = open(part, 'rb')
    image_data = file.read(2048)

    while image_data:
        client.send(image_data)
        image_data = file.read(2048)

    file.close()
    client.close()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connect_ip = None


class DizaneScreen(Screen):
    def connect(self, sm):
        try:
            global connect_ip
            client.connect((self.ids.connect_input.text, 9090))
            print(self.ids.connect_input.text)
            connect_ip = self.ids.connect_input.text
            sm.current = 'connect'
        except socket.error:
            pass


class ConnectScreen(Screen):
    def close(self, sm):
        global client
        try:
            data = ' '
            client.send(data.encode("utf-8"))
            sm.current = 'menu'
            client.close()

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except socket.error:
            client.close()
            sm.current = 'menu'


class ControlScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.one_button = True

    def pressed(self, ins):
        if ins == 'left':
            pop = self.ids.left.state
        elif ins == 'up':
            pop = self.ids.up.state
        elif ins == 'down':
            pop = self.ids.down.state
        elif ins == 'right':
            pop = self.ids.right.state

        if pop == 'down' and self.one_button:
            self.one_button = False
            self.timer = Clock.schedule_interval(partial(self.returning, ins), 0.1)
        else:
            self.one_button = True
            Clock.unschedule(self.timer)

    def returning(self, ins, *largs):
        data = 'control ' + ins
        try:
            client.send(data.encode("utf-8"))
        except:
            pass

    def clicking(self, ins):
        data = 'control ' + ins
        try:
            client.send(data.encode("utf-8"))
        except:
            pass

cors = open("sourses/cors.txt", "r")
texts_buttons = cors.read()
cors.close()
texts_buttons = texts_buttons.split(', ')


class AutoScreen(Screen):
    global texts_buttons
    texts_button = texts_buttons

    def clean(self):
        global texts_buttons
        cors = open("sourses/cors.txt", "w")
        cors.write('Empty, None, Empty, None, Empty, None, Empty, None, Empty, None, Empty, None')
        cors.close()
        texts_buttons = ['Empty', 'None', 'Empty', 'None', 'Empty', 'None', 'Empty', 'None', 'Empty', 'None',
                         'Empty', 'None']

    def reloading(self):
        global texts_buttons
        print(texts_buttons)
        self.ids.but_1.text = texts_buttons[0]
        self.ids.but_2.text = texts_buttons[2]
        self.ids.but_3.text = texts_buttons[4]
        self.ids.but_4.text = texts_buttons[6]
        self.ids.but_5.text = texts_buttons[8]
        self.ids.but_6.text = texts_buttons[10]

    def request(self):
        data = 'auto request-cord'
        try:
            client.send(data.encode("utf-8"))
        except:
            pass

    def save_data(self):
        if self.ids.number_input.text:
            if 0 < int(self.ids.number_input.text) < 7:
                number = self.ids.number_input.text
            else:
                return
            global texts_buttons
            name = self.ids.name_input.text
            e_data = '(' + self.ids.data_input.text + ')'
            n = ''
            for e in e_data:
                if e != ',' and e != ' ':
                    n += e
                elif e == ',':
                    e = '-'
                    n += e
            e_data = n

            if number == '1':
                texts_buttons[0] = name
                texts_buttons[1] = e_data
            elif number == '2':
                texts_buttons[2] = name
                texts_buttons[3] = e_data
            elif number == '3':
                texts_buttons[4] = name
                texts_buttons[5] = e_data
            elif number == '4':
                texts_buttons[6] = name
                texts_buttons[7] = e_data
            elif number == '5':
                texts_buttons[8] = name
                texts_buttons[9] = e_data
            elif number == '6':
                texts_buttons[10] = name
                texts_buttons[11] = e_data
            cors = open("sourses/cors.txt", "w")
            new_text = ''
            for el in str(texts_buttons):
                if el != '[' and el != ']' and el != "'":
                    new_text += el
            cors.write(new_text)
            cors.close()

    def open(self, number):
        global texts_buttons
        if number == '1':
            data = texts_buttons[1]
        elif number == '2':
            data = texts_buttons[3]
        elif number == '3':
            data = texts_buttons[5]
        elif number == '4':
            data = texts_buttons[7]
        elif number == '5':
            data = texts_buttons[9]
        elif number == '6':
            data = texts_buttons[11]
        if data == 'None':
            return
        data = 'auto open ' + data
        try:
            client.send(data.encode("utf-8"))
        except:
            pass


class AutoScreen_Setting(Screen):
    def cleaning(self):
        AutoScreen.clean(self)

    def save(self):
        AutoScreen.save_data(self)

    def request(self):
        AutoScreen.request(self)


class KeyboardScreen(Screen):
    def key_send(self):
        if self.ids.keyboard_input.text:
            data = 'keyboard ' + self.ids.keyboard_input.text
            try:
                client.send(data.encode("utf-8"))
                self.ids.keyboard_input.text = ''
            except socket.error:
                pass


class ShutdownScreen(Screen):
    def shutdown(self, value):
        data = 'shutdown ' + value
        try:
            client.send(data.encode("utf-8"))
        except:
            pass


part = 'Not selected'


class ImageScreen(Screen):
    def reload(self):
        global part
        self.ids.vibor.text = part

    def close(self):
        global part
        part = 'Not selected'
        self.ids.vibor.text = part

    def send_image(self):
        global part
        if part != 'Not selected':
            data = 'image'
            client.send(data.encode("utf-8"))

            send_p()


class ThreeMyPopup(Popup):
    def Check_path(self):
        if len(self.ids.File.selection) != 0:
            global part
            part = self.ids.File.selection[0]
            self.dismiss()


class DisplayScreen(Screen):
    def laung(self, inst):
        if inst == 'Eng':
            self.ids.lang_end_label.text = 'Eng'
            self.ids.eng_b.background_color = [.09, .31, .56, 1]
            self.ids.rus_b.background_color = [.06, .21, .38, 1]
        elif inst == 'Rus':
            self.ids.lang_end_label.text = 'Rus'
            self.ids.rus_b.background_color = [.09, .31, .56, 1]
            self.ids.eng_b.background_color = [.06, .21, .38, 1]

        data = self.ids.lang_end_label.text
        try:
            client.send(data.encode("utf-8"))
        except socket.error:
            pass

class PultApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.request_android_permissions()
        self.icon = 'sourses/icon.png'
        Builder.load_file("con.kv")
        sm = ScreenManager(transition=RiseInTransition())
        sm.add_widget(DizaneScreen(name='menu'))
        sm.add_widget(ConnectScreen(name='connect'))
        sm.add_widget(ControlScreen(name='control'))
        sm.add_widget(AutoScreen(name='auto'))
        sm.add_widget(AutoScreen_Setting(name='auto_setting'))
        sm.add_widget(KeyboardScreen(name='keyboard'))
        sm.add_widget(ShutdownScreen(name='shutdown'))
        sm.add_widget(ImageScreen(name='image'))
        sm.add_widget(DisplayScreen(name='display'))
        Clock.schedule_interval(partial(self.Examination, sm), 10)
        return sm

    def request_android_permissions(self):
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

    def Examination(self, sm, *args):
        if sm.current != 'menu':
            try:
                data = 'Examination'
                client.send(data.encode("utf-8"))
            except socket.error:
                client.close()
                sm.current = 'menu'


PultApp().run()
