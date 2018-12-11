import pandas as pd
import os

''' this program uses the imformation of timestation beta API to download information and find whos employees where working
in a specify moment in time'''


################### settings ###########################
''' This are the basic settings like the key for the API or the code to download the information from the server '''

with open('Api_key.txt', 'r') as tcode:
    key_api = tcode.read()
CODE = 34
########################################################


class data_analizer:
    '''this part we take the information from timestation website and start analyze it'''

    def __init__(self, location):

        self.location = location
        self.date1 = input('introduce Date YYYY-MM-DD -- > ')
        self.time_d = input('Time (24H - 12:00, 15:00) -- > ')
        
        print('\nPLease Wait....')
        self.url = f"https://api.mytimestation.com/v0.1/reports/?api_key={key_api}" \
              f"&Report_StartDate={self.date1}&Report_EndDate={self.date1}&id={CODE}&exportformat=csv"

        self.data = pd.read_csv(self.url)
        self.time = self.time_format_checker()
        self.display_results()

    def display_results(self):
        '''Inicial analisis and control flow of the class'''

        x = self.gettings_points(self.time)
        total_of_workers = x.shape[0]
        x.reset_index(inplace=True)
        if x.empty:
            pass
        else:
            print(x[['Date', 'Name', 'Department', 'Device', 'Time']].to_string(index=False))
        print('\n\n the total of employees is {} at {}'.format(total_of_workers, self.time))

    def gettings_points(self, t):
        '''this created a dataframe with the data for the expecify point in time when employees are actually working 
            and return it'''

        group_name = self.data[self.data["Time"] <= t]
        duplicates_removed = group_name.drop_duplicates(subset="Name", keep='last')
        punch_in_df = duplicates_removed[duplicates_removed.Activity.str.contains('Punch In')]
        x = punch_in_df[punch_in_df.Department.str.contains(self.location)]
        return x

    def time_format_checker(self):

        ''' sometimes the user just place single number for hours. making the program crash,
        so i made this test to add a cero before the time giving and anticipate posible problems.
        this program require military time (24h) '''

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

    def quick_report(self):

        '''this created a report in detail for the hours especify in the botton'''

        list_times = '6:00 10:00 12:15 14:00 15:45'.split()
        for n, t in enumerate(list_times):
            x = self.gettings_points(t)
            file_name = '{}-{}-{}.csv'.format(self.date1, t.replace(':', '.'), n)
            x.to_csv(file_name)
            os.startfile(file_name)


def start_up():
    ''' this function will control the flow of the whole Program.'''

    def continue_answer():

        ''' this part will make sure that the question for "location" is ask only once.
            normally user search many times in the same location.
        '''
        ibk_data = data_analizer(location)

        print('\n--for new search press "enter"')
        print('--to change location type "location"')
        print('--to export to excel type "export"')
        print('--to make a quick report type "quick"')
        answer = input('-- >')

        if not answer:
            os.system('cls')
            continue_answer()

        elif answer.lower() == "location":
            os.system('cls')
            start_up()

        elif answer.lower() == 'export':
            ibk_data.export_result()

        elif answer.lower() == 'quick':
            ibk_data.quick_report()
        else:
            print('to at this moment there are no more choices ')

    location = input('Location (leave Blank for all jobsites or just number of jobsite like "199" or "262") \n ---> ')
    continue_answer()


if __name__ == '__main__':

    print(' Welcome Historical Time Station Search ')
    print('____________________________________________________________________________________________________ \n\n\n')
    start_up()





