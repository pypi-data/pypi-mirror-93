from json import loads
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError

class sRemoAPI():
    access_token = ""
    device_identifier = ""

    param = {
        "tkn": "",
        "sig": "",
    }

    adjustment = {
        "temperature": 0,
        "humidity": 0,
        "brightness": 0,
    }

    appliances_type = {
        "tv": "t",
        "light": "l",
        "dvd":"d",
        "switch": "s",
        "aircon": "a",
    }

    def __init__(self, access_token, device_identifier):
        self.access_token = access_token
        self.device_identifier = device_identifier
        self.param["tkn"] = access_token

    def get_appliances_type(self):
        return self.appliances_type

    def get_adjustment(self):
        return self.adjustment

    def set_adjustment(self, temperature, humidity, brightness):
        self.adjustment["temperature"] = temperature
        self.adjustment["humidity"] = humidity
        self.adjustment["brightness"] = brightness

    def get_sensor_data(self):
        paramStr = urlencode(self.param)
        bese_url = "https://uapi1.sremo.net/user_api/" + self.device_identifier + "/webthl?"
        url = bese_url + paramStr

        data = []
        try:
            with urlopen(url) as response:
                request  = response.read()
                data = loads(request)
        except HTTPError as e:
            print(e)

        sensor_data = {
            "temperature": data["t"] + self.adjustment["temperature"],
            "humidity": data["h"] + self.adjustment["humidity"],
            "brightness": data["l"] + self.adjustment["brightness"]
        }

        return sensor_data
    
    def get_time(self):
        paramStr = urlencode(self.param)
        bese_url = "https://uapi1.sremo.net/user_api/" + self.device_identifier + "/webtim?"
        url = bese_url + paramStr

        data = []
        try:
            with urlopen(url) as response:
                request  = response.read()
                data = loads(request)
        except HTTPError as e:
            print(e)
        time = data["t"]

        return time

    def get_limit(self):
        paramStr = urlencode(self.param)
        bese_url = "https://uapi1.sremo.net/user_api/" + self.device_identifier + "/weblim?"
        url = bese_url + paramStr

        limit = 0
        try:
            with urlopen(url) as response:
                request  = response.read()
                limit = loads(request)
        except HTTPError as e:
            print(e)

        return limit
    
    def send_signal_141(self, signal):
        self.param["sig"] = signal
        paramStr = urlencode(self.param)
        bese_url = "https://uapi1.sremo.net/user_api/" + self.device_identifier + "/webhook?"
        url = bese_url + paramStr

        try:
            with urlopen(url) as response:
                request  = response.read()
        except HTTPError as e:
            print(e)

    def send_signal(self, appliance_number, appliance_type, signal):
        self.param["sig"] = appliance_number + "-" + self.appliances_type[appliance_type] + "-" + signal
        paramStr = urlencode(self.param)
        base_url = "https://uapi1.sremo.net/user_api/" + self.device_identifier + "/webhook?"
        url =  base_url + paramStr

        try:
            with urlopen(url) as response:
                request  = response.read()
        except HTTPError as e:
            print(e)


