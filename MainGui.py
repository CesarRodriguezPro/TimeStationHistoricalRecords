import pandas as pd
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


#  todo take the main program and ingrated with the kivy interface.

''' 
this program uses the information of timestation beta API to 
download information and find who's employees where working
in a specify moment in time
'''


################### settings ###########################

''' This are the basic settings like the key for the API 
or the code to download the information from the server '''

with open('Api_key.txt', 'r') as tcode:
    key_api = tcode.read()
CODE = 34

########################################################


class data_analizer:

    '''
    this part we take the information from timestation website and start analyze it
    '''

    def __init__(self, location, date1):

        self.date1 = date1
        self.location = location

        self.url = f"https://api.mytimestation.com/v0.1/reports/?api_key={key_api}" \
            f"&Report_StartDate={self.date1}&Report_EndDate={self.date1}&id={CODE}&exportformat=csv"
        self.data = pd.read_csv(self.url)
        self.time = self.time_format_checker()
        self.display_results()

    def display_results(self):

        '''
        Initial analysis and control flow of the class
        '''

        x = self.gettings_points(self.time)
        x.reset_index(inplace=True)
        return x

    def gettings_points(self, t):

        '''
        this created a dataframe with the data for the especial point in time when employees are actually working
        and return it
        '''

        group_name = self.data[self.data["Time"] <= t]
        duplicates_removed = group_name.drop_duplicates(subset="Name", keep='last')
        punch_in_df = duplicates_removed[duplicates_removed.Activity.str.contains('Punch In')]
        x = punch_in_df[punch_in_df.Department.str.contains(self.location)]
        return x

    def time_format_checker(self):

        '''
        sometimes the user just place single number for hours. making the program crash,
        so i made this test to add a zero before the time giving and anticipate possible problems.
        this program require military time (24h)
        '''

        if len(self.time_d) == len('2:00'):
            return f'0{self.time_d}'
        else:
            return self.time_d

    def export_result(self):

        '''simple program to export the resolts in to csv file.'''

        x = self.gettings_points(self.time)
        file_name = 'historicalFor{}.csv'.format(self.date1)
        x.to_csv(file_name)
        os.startfile(file_name)


class ScatterTextWidget(BoxLayout):
    pass


class HistoricalApp(App):
    def build(self):
        return ScatterTextWidget()


if __name__ == "__main__":

    HistoricalApp().run()
