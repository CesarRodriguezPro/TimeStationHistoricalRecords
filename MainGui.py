import pandas as pd
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty


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


class ScatterTextWidget(BoxLayout):
    ''' this part we take the information from timestation website and start analyze it '''

    item_to_display

    def initialize_request(self):
        ''' Initial analysis and control flow of the class '''
        
        location = self.ids.text_location.text
        date = self.ids.input_date.text
        time_raw = self.ids.input_time.text
        print(f'{location} - {date} - {time_raw}')

        url = f"https://api.mytimestation.com/v0.1/reports/?api_key={key_api}" \
            f"&Report_StartDate={date}&Report_EndDate={date}&id={CODE}&exportformat=csv"

        data = pd.read_csv(url)
        time = self.time_format_checker(time_d=time_raw)
        group_name = data[data["Time"] <= time]
        duplicates_removed = group_name.drop_duplicates(subset="Name", keep='last')
        punch_in_df = duplicates_removed[duplicates_removed.Activity.str.contains('Punch In')]
        x = punch_in_df[punch_in_df.Department.str.contains(location)]
        x.reset_index(inplace=True)
        self.ids.print_out.text = x.to_string()

    def time_format_checker(self, time_d):

        '''
        sometimes the user just place single number for hours. making the program crash,
        so i made this test to add a zero before the time giving and anticipate possible problems.
        this program require military time (24h)
        '''

        if len(time_d) == len('2:00'):
            return f'0{time_d}'
        else:
            return time_d

    def export_result(self):

        '''simple program to export the resolts in to csv file.'''

        x = self.gettings_points(self.time)
        file_name = 'historicalFor{}.csv'.format(self.date1)
        x.to_csv(file_name)
        os.startfile(file_name)


class HistoricalApp(App):
    def build(self):
        return ScatterTextWidget()


if __name__ == "__main__":

    HistoricalApp().run()

