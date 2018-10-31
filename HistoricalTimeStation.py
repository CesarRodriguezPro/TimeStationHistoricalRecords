import pandas as pd
import os
import matplotlib.pyplot as plt

# settings
key_api = 'spbdxdqepugjhgeh4kbrn6t2sz7jfytm'
code = 34


class data_analizer:

    ''' '''

    def __init__(self, location):

        self.location = location

        self.date1 = input('introduce Date YYYY-MM-DD -- > ')
        self.time_d = input('Time (24H - 12:00, 15:00) -- > ')
        print('\nPLease Wait....')

        self.url = f"https://api.mytimestation.com/v0.1/reports/?api_key={key_api}" \
              f"&Report_StartDate={self.date1}&Report_EndDate={self.date1}&id={code}&exportformat=csv"

        self.data = pd.read_csv(self.url)

        #  ['Date', 'Employee ID', 'Name', 'Department', 'Device', 'Time',
        # 'Activity', 'Punch Method', 'Latitude', 'Longitude', 'IP Address','Notes']
        
        self.time = self.time_format_checker()

        self.display_results()

    def gettings_points(self, t):

        group_name = self.data[self.data["Time"] <= t]
        duplicates_removed = group_name.drop_duplicates(subset="Name", keep='last')
        punch_in_df = duplicates_removed[duplicates_removed.Activity.str.contains('Punch In')]
        x = punch_in_df[punch_in_df.Department.str.contains(self.location)]
        return x

    def display_results(self):

        x = self.gettings_points(self.time)
        total_of_workers = x.shape[0]
        x.reset_index(inplace=True)

        if x.empty:
            pass
        else:
            print(x[['Date', 'Name', 'Department', 'Device', 'Time']].to_string(index=False))

        print('\n\n the total of employees is {} at {}'.format(total_of_workers, self.time))

    def time_format_checker(self):

        if len(self.time_d) == len('2:00'):
            return f'0{self.time_d}'
        else:
            return self.time_d

    def export_result(self):
        x = self.gettings_points(self.time)
        file_name = 'historicalFor{}.csv'.format(self.date1)
        x.to_csv(file_name)
        os.startfile(file_name)

    def quick_report(self):

        list_times = '6:00 10:00 12:15 14:00 15:45'.split()

        for n, t in enumerate(list_times):
            x = self.gettings_points(t)
            file_name = '{}-{}-{}.csv'.format(self.date1, t.replace(':', '.'), n)
            x.to_csv(file_name)
            os.startfile(file_name)


def start_up():

    def continue_answer():

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





