from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
import json

Config.set('graphics', 'width', 1080)
Config.set('graphics', 'height', 780)

outputtext = ''
last_detected_time = 0

# JSON data
json_data = '''
[
    {"barcode_id":"123456789012","name":"Tool Box","price":10.99,"description":"Organised Heavy-Duty Portable Essential Toolbox with Top Lid and Removable Tray Compartment for Easy & Convenient Storage, 1 Year Warranty, YELLOW & BLACK (Made in Israel)","product_img":"assets/product/product-1.jpg"},
    {"barcode_id":"9088813","name":"Noise Cancelling Headphones","price":20.99,"description":"ProCase Noise Reduction Ear Muffs, NRR 28dB Shooters Hearing Protection Headphones Headset, Professional Noise Cancelling Ear Defenders for Construction Work Shooting Range Hunting","product_img":"assets/product/product-2.jpg"},
    {"barcode_id":"9023817","name":"Cutter","price":30.99,"description":"STANLEY STHT10276-812 18mm Steel Snap-Off Knife (red)","product_img":"assets/product/product-3.jpg"},
    {"barcode_id":"8906008422276","name":"LED Bulb","price":40.99,"description":"Widest range of lighting product : LED, CFL, Halogens and HID lamps & luminaires","product_img":"assets/product/product-4.jpg"},
    {"barcode_id":"8901765119025","name":"Dumbbells","price":50.99,"description":"Dumbbells Set for Home Gym | 5kg Dumbbells Set of 2 | Fitness Gym Dumbbell set for Home Workout | Anti Skid rubber Dumbbell set | Weights for Workout","product_img":"assets/product/product-5.jpg"},
    {"barcode_id":"8901057510028","name":"Boxing Gloves","price":60.99,"description":"UNBEATABLE Lite Contest Pu Boxing Gloves for Men & Women with Moulded Foam Padding, Sweat Wicking Lining, Elasticated Hook & Loop Wrap Around Closure System (Red, 12oz)","product_img":"assets/product/product-6.jpg"}
]
'''
products = json.loads(json_data)

# Function to get product details from the JSON data
def get_product_details(barcode_id):
    for product in products:
        if product["barcode_id"] == barcode_id:
            return product["name"], product["price"], product["product_img"], product["description"]
    return None

class MainScreen(BoxLayout):
    def __init__(self, second_screen, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'  # horizontal placing of widgets
        self.second_screen = second_screen

        self.slideshow_images = [
            'assets/slideshow-1.jpg',
            'assets/slideshow-2.jpg',
            'assets/slideshow-3.jpg',
            # Add more paths as needed
        ]

        self.gif_images = [
            'assets/file_pages-to-jpg-0001.png',
            'assets/file_pages-to-jpg-0002.png',
            'assets/file_pages-to-jpg-0003.png',
            # Add more paths as needed
        ]

        self.current_image_index = 0
        self.current_image_gif = 0

        self.barcode = ""

        Window.bind(on_key_down=self.on_key_down)
        
        Clock.schedule_interval(self.check_barcode_timeout, 1)  # check barcode timeout every second
        Clock.schedule_interval(self.update_slideshow, 5)
        Clock.schedule_interval(self.update_gif, .5)  # update gif every 0.5 seconds

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:  # Enter key
            self.process_barcode(self.barcode)
            self.barcode = ""
        else:
            self.barcode += text
        print(self.barcode)

    def process_barcode(self, barcode_id):
        global outputtext, last_detected_time
        outputtext = barcode_id
        self.update_second_screen(barcode_id)
        if main_app.sm.current != 'second':
            self.change_screen()
        last_detected_time = Clock.get_boottime()

    def update_second_screen(self, barcode_id):
        product = get_product_details(barcode_id)
        if product:
            product_name, price, product_img, descrip = product
            self.second_screen.ids.product_image.source = f'{product_img}'  # Update product image
            self.second_screen.ids.lab1.text = f"Barcode ID: {barcode_id}"
            self.second_screen.ids.lab2.text = f"Product Name: {product_name}"
            self.second_screen.ids.lab3.text = f"Price: {price}"
            self.second_screen.ids.lab4.text = f"Description: {descrip}"
        else:
            self.second_screen.ids.product_image.source = 'assets/DIY-Infiniti-Mall-Malad.jpg'  # Update default image
            self.second_screen.ids.lab1.text = f"Barcode ID: {barcode_id}"
            self.second_screen.ids.lab2.text = "Product Name: Not found"
            self.second_screen.ids.lab4.text = f"Description: Not found"

    def change_screen(self, *args):
        main_app.sm.current = 'second'  # once barcode is detected, switch to second screen

    def check_barcode_timeout(self, dt):
        global last_detected_time, outputtext
        if Clock.get_boottime() - last_detected_time > 10:
            if main_app.sm.current == 'second':
                outputtext = ''
                main_app.sm.current = 'main'
            last_detected_time = Clock.get_boottime()

    def update_slideshow(self, dt):
        self.current_image_index = (self.current_image_index + 1) % len(self.slideshow_images)
        self.ids.slideshow.source = self.slideshow_images[self.current_image_index]

    def update_gif(self, dt):
        self.current_image_gif = (self.current_image_gif + 1) % len(self.gif_images)
        self.ids.gif.source = self.gif_images[self.current_image_gif]

class SecondScreen(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()  # screenmanager is used to manage screens
        self.second_screen = SecondScreen()
        
        scrn = Screen(name='main')
        mainsc = MainScreen(self.second_screen)
        scrn.add_widget(mainsc)
        self.sm.add_widget(scrn)

        scrn = Screen(name='second')
        scrn.add_widget(self.second_screen)
        self.sm.add_widget(scrn)

        return self.sm

if __name__ == '__main__':
    main_app = MyApp()
    main_app.run()
