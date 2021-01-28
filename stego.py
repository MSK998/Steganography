# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
# from os.path import dirname, expanduser

from PIL import Image
# ImageFile

from pathlib import Path
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label

Builder.load_string("""
<Manager>:
    MainScreen:
        name: "main"
        BoxLayout:
            orientation: 'vertical'
            Label:
                id: pathLabel
                text: ' '
            Button:
                id: pathButton
                text: 'SELECT FILE'
                on_press: root.current = 'files'

            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Message: '
                TextInput:
                    id: messageInput

            BoxLayout:
                orientation: 'horizontal'
                Button:
                    text: 'ENCODE'
                    on_press: root.encode(); messageInput.text=""
                Button:
                    text: 'DECODE'
                    on_press: root.decode()

    FileScreen:
        name: "files"
        BoxLayout:
            FileChooserListView:
                id: filechooser
                rootpath: root.return_user_home()
                on_selection: pathLabel.text = str(filechooser.selection[0])
                on_selection: root.current = 'main'
""")


class Manager(ScreenManager):
    # Convert encoding data into 8-bit binary
    # form using ASCII value of characters

    # Gets the user home folder
    def return_user_home(self):
        return str(Path.home())

    def genData(self, data):
        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    # Pixels are modified according to the
    # 8-bit binary data and finally returned
    def modPix(self, pix, data):

        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):

            # Extracting 3 pixels at a time
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]

            # Pixel value should be made
            # odd for 1 and even for 0
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            # Ninth pixel of every set tells
            # whether to stop or to read further.
            # 0 means keep reading; 1 means the
            # message is over.
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    # print(pix[-1])
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    # print(pix[-1])
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

            print(pix)

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):

            # Putting modified pixels in the new image
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def check_file_type(self, filename):
        if (filename.split('.')[1].upper() == 'JPG'):
            return 'JPEG'
        else:
            return filename.split('.')[1].upper()

    # Encode data into image
    def encode(self):
        # img = input("Enter image name(with extension): ")
        img = self.ids.pathLabel.text
        image = Image.open(img, 'r')

        # data = input("Enter data to be encoded : ")
        data = self.ids.messageInput.text

        if (len(data) == 0):
            raise ValueError('Data is empty')

        newimg = image.copy()
        self.encode_enc(newimg, data)

        # new_img_name = input("Enter the name of new image(with extension): ")
        # Sets the encoded image to the original image path
        new_img_name = img

        # Saves the image
        newimg.save(new_img_name, self.check_file_type(new_img_name))

        message = ModalView(size_hint=(None, None), size=(400, 400))
        messageLabel = Label(text="Message Encoded to:\n" + img, text_size=(message.width - 50, None))
        message.add_widget(messageLabel)
        message.open()
        print('done')

    # Decode the data in the image
    def decode(self):
        # img = input("Enter image name(with extension) :")
        img = self.ids.pathLabel.text
        # Must let PIL know that its a JPEG file, currently using JPG
        # Just need to use the same if statement as before
        image = Image.open(img, 'r')

        data = ''
        imgdata = iter(image.getdata())

        while (True):
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            # string of binary data
            binstr = ''

            for i in pixels[:8]:
                if (i % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if (pixels[-1] % 2 != 0):
                dmessage = ModalView(size_hint=(None, None), size=(400, 400))
                message_label = Label(text="Message:\n\n" + data, text_size=(dmessage.width - 50, None))
                dmessage.add_widget(message_label)
                dmessage.open()
                return data


class MainScreen(Screen):
    # Main Function
    def main(self):
        a = int(input(":: Welcome to Steganography ::\n"
                      "1. Encode\n"
                      "2. Decode\n"))
        if (a == 1):
            self.encode()

        elif (a == 2):
            print("Decoded word: " + self.decode())
        else:
            raise Exception("Enter correct input")


class FileScreen(Screen):

    def _fbrowser_canceled(self, instance):
        print('cancelled, Close self.')

    def _fbrowser_success(self, instance):
        print(instance.selection[0])
        # App.get_running_app().root.ids.pathLabel.text = instance.selection[0]
        self.path = instance.selection[0]


class StegoApp(App):

    def build(self):
        Window.size = (500, 350)
        self.screenmanager = Manager()
        return self.screenmanager


# Calling main function
if __name__ == '__main__':
    AppInstance = StegoApp()
    AppInstance.run()
