from bs4 import BeautifulSoup
from html.parser import HTMLParser
from time import localtime
from simpleaudio import WaveObject
from requests import get
from json import dumps, load

api = BeautifulSoup()

class Config:
    def __init__(self):
        self.links = dict()
        self.interval = 1800

    def add_product(self):
        while True:
            new_product_url = input("Enter URL to product (enter 'x' when finished):    ")
            if (new_product == 'x'):
                break
            name = get_product_name(new_product_url)
            self.links[name] = new_product_url
        update_config(self.__dict__)

    def load_config(self):
        try
            config_object = open('config.json', 'r')
        except FileNotFoundError:
            print ("No config file found. Creating new config...")
            config_object = open('config.json', 'x')
            config_object.write(dumps(self.__dict__, indent=2))
            config_object.close()
        except Exception:
            print ("Error with loading configuration")
        finally:
            json_object = load(config_object)
            self.links = json_object("links")
            self.interval = json_object("interval")


def play_sound(sound_file):
    try:
        audio_object = WaveObject.from_wave_file(f"./sounds/{sound_file}")
        play = audio_object.play()
        play.wait_done()
        play.stop()
    except FileNotFoundError:
        print(f"{sound_file} file not found.")
    except Exception:
        print("Error with playing notification audio.")
    finally:
        return

def html_request(url):
    try:
        new_request = get(url)
    except Exception:
        print ("Error making HTTP request")
        return False
    else:
        return BeautifulSoup(new_request.text, "html.parser")

def site_is_valid(website_input):
    if (len(website_input) == 0 or not "www." in website_input):
        print ("Invalid website given.")
        return False
    try:
        status_code = get(website_input).status_code
        if (status_code >= 200 and status_code <= 299):
                return True
            elif (status_code == 404):
                print("Invalid Server entered.")
                return False
            else:
                print("Connection error")
                return False
        except Exception:
            return False

#Halts program for configured time before making another request
def wait():
    global continue_condition
    for timer in range(config.interval):
        if continue_condition:
            sleep(1)
        else:
            break

def get_product_name(url):
    html_object = html_request(url)
    if not (html_object):
        return
    html_object = BeautifulSoup(html_object.text, "html.parser")
    product_name = html_object.find_all("h1", class_="productName_2KoPa")
    return product_name.string


def best_buy_checker(url):
    html_object = html_request(url)
    html_object = html_object.find("span", class_="shippingAvailability_2X3xt shippingAvailabilityTitle_2sixU")
    if (html_object.string == "Available to ship"):



def memory_express_checker():
    pass
def canada_computers_checker():
    pass
def newegg_checker():
    pass


def checker_director(user_input):
    if ("bestbuy" in user_input):
        best_buy_checker()
    elif ("memoryexpress" in user_input):
        memory_express_checker()
    elif ("canadacomputers" in user_input):
        canada_computers_checker()
    elif ("newegg" in user_input):
        newegg_checker()
    else:
        print ("Unrecognized site or input.")
        return

def main():
    command_dict = {"instock": print_in_stock,
                    "new": config.add_product,
                    "del": config.delete_product,
                    "help": print_manual,
                    "fresh": config_reset}

    while True:
        print ("-------------------------")
        user_input = input()
        print ("-------------------------")
        if (user_input in command_dict.keys()):
            command_dict[user_input]()
        elif (user_input == "exit"):
            stop()
            print("Program exiting.")
            break
        elif (user_input == ""):
            print ("")
        else:
            print ("Unknown command.")


if __name__ == '__main__':
    global in_stock_list
    in_stock_list = []
