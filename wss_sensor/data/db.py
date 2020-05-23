from wss.data.db import DB


class DB(DB):
    def save_sensor_value(self, value):
        return True
