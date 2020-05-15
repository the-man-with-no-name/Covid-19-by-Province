# Covid-19-by-Province

This repository provides a file to create a video from several choropleth images using ```pandas```, ```geopandas```, and ```matplotlib```.

The dataset of daily Covid-19 numbers and ```.shp``` file are from [```Statistics Canada```](https://www.statcan.gc.ca/eng/start).

An ```.shp``` file gives the shapes of different geographic objects (in this case, Provinces) that are used to plot them by ```geopandas```.

The file ```daily_covid_canada.py``` creates a choropleth of each days new cases by running ```python daily_covid_canada.py```.

To make these images into a video, I recommend using ```ffmpeg```, a useful command line tool for media.

Change directory to the appropriate folder where the images are located and run:

```ffmpeg -f image2 -framerate 5 -pattern_type sequence -start_number 0 -r 5 -i %d.png -s 720x480 -pix_fmt yuv420p covid_canada_daily.mp4```
