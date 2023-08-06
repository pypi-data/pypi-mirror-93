"""
Date conversion, English date to Bengali date, date string to numeric date

Author: Faruk Ahmad

Last Update: 29 Jan, 2021
"""

from datetime import datetime

class Date:
    def __init__(self):
        self.today = ""

    def get_date(self):
        try:
            time_now = datetime.now()
            self.today = time_now.strftime("%Y-%m-%d  %H:%M:%S")
        except Exception as e:
            print(f"Something went wrong. + {e}")
            return self.today
        else:
            return self.today
