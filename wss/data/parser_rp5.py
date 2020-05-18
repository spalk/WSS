from abc import ABC
from html.parser import HTMLParser
import datetime
import re

import logging
logger = logging.getLogger('root')


class ParserRP5(HTMLParser, ABC):
    def __init__(self):
        HTMLParser.__init__(self)

        self.table_open = False
        self.tr_counter = 0
        self.date_marker = False
        self.hours_marker = False
        self.temper_marker = False
        self.temper_marker_final = False
        self.pressure_marker = False

        self.dates = []
        self.hours = []
        self.tempers = []
        self.pressures = []

        self.cnt_raw_data = 0
        self.cnt_clean_data = 0

        self.data = []

        logger.debug('Start RP5 parser processor')

    def handle_starttag(self, tag, attrs):
        # <table id="forecastTable" class="forecastTable" style="display: table;">
        if tag == 'table':
            for name, value in attrs:
                if name == 'id' and value == 'forecastTable':
                    self.table_open = True
                    break

        if self.table_open:
            if tag == 'tr':
                self.tr_counter += 1
                # ignore tr with class: <tr class="underlineRow"></tr>
                for name, value in attrs:
                    if name == 'class' and value == 'underlineRow':
                        self.tr_counter -= 1

            # Days
            # <span class="monthDay">April 29</span>
            if self.tr_counter == 1 and tag == 'span':
                for name, value in attrs:
                    if name == 'class' and value == 'monthDay':
                        self.date_marker = True
                        break

            # Hours
            # <td colspan="2" class="n underlineRow">03</td>
            if self.tr_counter == 2 and tag == 'td':
                for name, value in attrs:
                    if name == 'class' and 'underlineRow' in value.split(' '):
                        self.hours_marker = True
                        break

            # Temperature
            # <div class="t_0"><b>+<span class="otstup"></span>8</b></div>
            if self.tr_counter == 5 and tag == 'div':
                for name, value in attrs:
                    if name == 'class' and value == 't_0':
                        self.temper_marker = True
                        break

            if self.tr_counter == 5 and self.temper_marker and tag == 'b':
                self.temper_marker_final = True

            # Pressure
            # <div class="p_0">740</div>
            if self.tr_counter == 7 and tag == 'div':
                for name, value in attrs:
                    if name == 'class' and value == 'p_0':
                        self.pressure_marker = True
                        break

    def handle_endtag(self, tag):
        if self.table_open:
            if tag == 'table':
                self.table_open = False

        if self.date_marker:
            if tag == 'span':
                self.date_marker = False

        if self.hours_marker:
            if tag == 'span':
                self.hours_marker = False

        if self.temper_marker:
            if tag == 'div':
                self.temper_marker = False

        if self.temper_marker_final:
            if tag == 'b':
                self.temper_marker_final = False

        if self.pressure_marker:
            if tag == 'div':
                self.pressure_marker = False

    def handle_data(self, data):
        if self.date_marker:
            self.dates.append(data)
            self.cnt_raw_data += 1

        if self.hours_marker and self.tr_counter == 2:
            self.hours.append(data)
            self.cnt_raw_data += 1

        if self.temper_marker_final:
            self.tempers.append(data)
            self.cnt_raw_data += 1

        if self.pressure_marker:
            self.pressures.append(data)
            self.cnt_raw_data += 1

    def set_data_types(self):
        """Clearing data and converting from strings to datetime and int"""

        logger.debug('Raw data parsed: ' + str(self.cnt_raw_data))

        days_dt = []
        hours_int = []
        tempers_int = []
        pressures_int = []

        # days
        for day in self.dates:
            # "September 18, 2017, 22:19:55" -> "%B %d, %Y, %H:%M:%S"
            day_dt = datetime.datetime.strptime(day, '%B %d')
            current_year = self.get_year(day_dt.month)
            day_dt_final = day_dt.replace(year=current_year)
            days_dt.append(day_dt_final)
        logger.debug('>> len days_dt %s' % len(days_dt))

        # hours
        hour_num = re.compile(r'\d+')
        for hour in self.hours:
            if hour_num.match(hour):
                hours_int.append(int(hour))
        logger.debug('>> len hours_int %s' % len(hours_int))

        # temperature
        temper_sign = re.compile(r'[+,-]')
        for t in self.tempers:
            if temper_sign.match(t):
                sign = t
            else:
                temp = int(t)
                if sign == '-':
                    temp = temp * (-1)
                tempers_int.append(temp)
        logger.debug('>> len temper_int %s' % len(tempers_int))

        # pressure
        for p in self.pressures:
            pressures_int.append(int(p))
        logger.debug('>> len pressures_int %s' % len(pressures_int))

        # packing data
        data_len = len(hours_int) - 1
        data_len_list = range(data_len)
        date_index = 0

        for i in data_len_list:
            dt = days_dt[date_index].replace(hour=hours_int[i])
            data = {'datetime': dt, 'parameter': 't', 'value': tempers_int[i]}
            self.data.append(data)
            self.cnt_clean_data += 1
            data = {'datetime': dt, 'parameter': 'p', 'value': pressures_int[i]}
            self.data.append(data)
            self.cnt_clean_data += 1
            if not data_len_list.index(i) == data_len:
                if hours_int[i + 1] < hours_int[i]:
                    date_index += 1

        logger.debug('Clean data parsed: ' + str(self.cnt_clean_data))

    def get_data(self) -> list:
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
