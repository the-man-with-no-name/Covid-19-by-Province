__author__ = 'Ryan DeMuse'
__date__ = '5-14-2020'
__email__ = 'ryan.demuse@du.edu'

"""
TODO:

        make into video: ffmpeg -f image2 -framerate 5 -pattern_type sequence -start_number 0 -r 5 -i %d.png -s 720x480 -pix_fmt yuv420p covid_canada_daily.mp4

"""

import pandas
import geopandas
import matplotlib.pyplot as plt

# allows .head() to display #row_display rows
rows_display = 11

# Create lists of date ranges
jan_dates = ['1/{}/20'.format(i) for i in range(22,32)]
feb_dates = ['2/{}/20'.format(i) for i in range(1,30)]
mar_dates = ['3/{}/20'.format(i) for i in range(1,32)]
apr_dates = ['4/{}/20'.format(i) for i in range(1,31)]
may_dates = ['5/{}/20'.format(i) for i in range(1,13)]

all_dates = jan_dates + feb_dates + mar_dates + apr_dates + may_dates

# Get the number of unique new daily cases from total
def new_daily_cases(dates,cases):
    dc = pandas.DataFrame() #columns=total_cases.columns
    for i in range(len(dates)-1,-1,-1):
        if i > 0:
            dc[dates[i]]=cases[dates[i]]-cases[dates[i-1]]
        else:
            dc[dates[i]]=cases[dates[i]]
    dc['PRENAME'] = cases['PRENAME']
    return dc.iloc[:,::-1]

# Geo Data file for plotting the map of Canada
map_geo_file = "gpr_000b11a_e/gpr_000b11a_e.shp"
map_data_file = geopandas.read_file(map_geo_file)

# Import Canada Covid Numbers
covid_csv_file = "canada_numbers.csv"
covid_data_file = pandas.read_csv(covid_csv_file)

# Rename Data file column of Provinces to match Geo File
covid_data_file.rename({'Province/State': 'PRENAME'},axis=1,inplace=True)

covid_data_file_provinces_all = covid_data_file[['PRENAME'] + all_dates]

new_cases_all_dates = new_daily_cases(all_dates,covid_data_file)

# Merge the Geo Data file and the Cases file
space_and_data = map_data_file.merge(new_cases_all_dates,on='PRENAME')

def plot_all_dates(dates,data):
    i = 0
    val_min, val_max = data[all_dates].values.min(), data[all_dates].values.max() # min and max values resp.
    for date in dates:
        variable_to_plot = date
        vmin, vmax = val_min, val_max
        fig, ax = plt.subplots(1, figsize=(8, 4))
        ax.axis('off')
        ax.set_title('Daily Covid-19 Cases by Province: {}'.format(variable_to_plot), fontdict={'fontsize': '15', 'fontweight' : '2'})
        ax.annotate('Source: Statistics Canada, 2020',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=10, color='#555555')
        sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm.set_array([])
        fig.colorbar(sm, orientation="vertical", fraction=0.015, pad=0.2, aspect = 20)
        data.plot(column=variable_to_plot,cmap='Blues',linewidth=0.8,ax=ax,edgecolor='0.8',vmin=vmin,vmax=vmax)
        plt.savefig('images/{}.png'.format(i),dpi=300)
        plt.close('all')
        i += 1

plot_all_dates(all_dates,space_and_data)