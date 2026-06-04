

class City:
    def __init__(self, city_id, name):
        self.city_id = city_id
        self.name = name


class WeatherRecord:
    def __init__(self, city_id, description_en, description_de, temp, temp_min, temp_max, date):
        self.city_id = city_id
        self.description_en = description_en
        self.description_de = description_de
        self.temp = temp
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.date = date
        