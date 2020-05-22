from abc import ABC
from html.parser import HTMLParser
import datetime

import logging
logger = logging.getLogger('root')


class ParserYandex(HTMLParser, ABC):
    def __init__(self):
        HTMLParser.__init__(self)

        self.day_marker = False
        self.month_marker = False
        self.in_temper_td = False
        self.temper_marker = False
        self.temper_range = []
        self.pressure_marker = False

        self.days = []
        self.months = []
        self.tempers = []
        self.pressures = []

        self.data = []

        self.cnt_raw_data = 0
        self.cnt_clean_data = 0

        logger.debug('Start yandex parser processor')

    def handle_starttag(self, tag, attrs):
        # day
        # <strong class="forecast-details__day-number">3</strong>
        if tag == 'strong':
            for attr, value in attrs:
                if attr == 'class' and value == 'forecast-details__day-number':
                    self.day_marker = True

        # month
        # <span class="forecast-details__day-month">мая</span>
        if tag == 'span':
            for attr, value in attrs:
                if attr == 'class' and value == 'forecast-details__day-month':
                    self.month_marker = True

        # temp (2 stage parsing)
        # 1: <td class="weather-table__body-cell weather-table__body-cell_type_daypart
        #    weather-table__body-cell_wrapper">
        # 2: <span class="temp__value">+18</span>
        if tag == 'td':
            for attr, value in attrs:
                if attr == 'class' and 'weather-table__body-cell_wrapper' in value.split(' '):
                    self.in_temper_td = True
        if self.in_temper_td and tag == 'span':
            for attr, value in attrs:
                if attr == 'class' and value == 'temp__value':
                    self.temper_marker = True

        # pressure
        # <td class="weather-table__body-cell weather-table__body-cell_type_air-pressure">750</td>
        if tag == 'td':
            for attr, value in attrs:
                if attr == 'class' and 'weather-table__body-cell_type_air-pressure' in value.split(' '):
                    self.pressure_marker = True

    def handle_endtag(self, tag):
        if self.day_marker:
            if tag == 'strong':
                self.day_marker = False

        if self.month_marker:
            if tag == 'span':
                self.month_marker = False

        if self.temper_marker:
            if tag == 'span':
                self.temper_marker = False

        if self.in_temper_td:
            if tag == 'td':
                self.in_temper_td = False
                if len(self.temper_range) > 0:
                    self.tempers.append(self.temper_range)
                self.temper_range = []

        if self.pressure_marker:
            if tag == 'td':
                self.pressure_marker = False

    def handle_data(self, data):
        if self.day_marker:
            self.days.append(data)
            self.cnt_raw_data += 1

        if self.month_marker:
            self.months.append(data)
            self.cnt_raw_data += 1

        if self.temper_marker:
            self.temper_range.append(data)
            self.cnt_raw_data += 1

        if self.pressure_marker:
            self.pressures.append(data)
            self.cnt_raw_data += 1

    def set_data_types(self):
        """Clearing data and converting from strings to datetime and int"""
        logger.debug('Raw data parsed: ' + str(self.cnt_raw_data))

        days_dt = []

        # days (datetime)
        for i in range(len(self.days)):
            day_int = int(self.days[i])
            month_int = self.convert_month_to_int(self.months[i])
            year_int = self.get_year(month_int)
            days_dt.append(datetime.datetime(year=year_int, month=month_int, day=day_int))
        # print(days_dt)

        # packing data
        cnt_day = 0
        time_of_day_dic = {1: 9,  # morning
                           2: 15,  # afternoon
                           3: 21,  # evening
                           4: 3,  # night of next day
                           }
        time_of_day = 0
        for i in range(len(self.tempers)):
            time_of_day += 1
            hour = time_of_day_dic[time_of_day]
            dt = days_dt[cnt_day].replace(hour=hour)
            if time_of_day == 4:
                dt = dt + datetime.timedelta(days=1)

            for t in self.tempers[i]:
                data = {'datetime': dt, 'parameter': 't', 'value': int(t)}
                self.data.append(data)
                self.cnt_clean_data += 1

            data = {'datetime': dt, 'parameter': 'p', 'value': int(self.pressures[i])}
            self.data.append(data)
            self.cnt_clean_data += 1

            if time_of_day == 4:
                time_of_day = 0
                cnt_day += 1

        logger.debug('Clean data parsed: ' + str(self.cnt_clean_data))

    def get_data(self):
        return self.data

    @staticmethod
    def get_year(month: int) -> int:
        """Get year (int) from month (int)"""
        now = datetime.datetime.now()
        current_month = now.month
        if month != current_month and month == 1:
            return now.year + 1
        else:
            return now.year

    @staticmethod
    def convert_month_to_int(month: str) -> int:
        months_dic = {'января': 1,
                      'февраля': 2,
                      'марта': 3,
                      'апреля': 4,
                      'мая': 5,
                      'июня': 6,
                      'июля': 7,
                      'августа': 8,
                      'сентября': 9,
                      'октября': 10,
                      'ноября': 11,
                      'декабря': 12}
        return months_dic[month]

