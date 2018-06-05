import matplotlib
import matplotlib.dates
import matplotlib.pyplot as plt


list_of_datetimes=[]
list_of_datetimes.append('2018-05-02 00:00:00')
list_of_datetimes.append('2018-02-10')
list_of_datetimes.append('2018-10-28')

values = []
values.append(2)
values.append(5)
values.append(1)
# dates = matplotlib.dates.date2num(list_of_datetimes)
matplotlib.pyplot.plot_date(list_of_datetimes, values)
plt.show()