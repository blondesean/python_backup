#Declare libraries we will need
import math
import pandas as pd
import numpy as np
import random 
import pylab
import matplotlib.pyplot as plt
import sys
import os

'''
#SEPERATE FIGURES 
#Specify our working directory and the name of the csv we want to import then read that into a Pandas dataframe
os.chdir('//chnas06/MKT-Data/INTERNET/INET Admin/Sean/Projects/Data Visualization')
input_file = 'Test_Python_Set.csv'

#Read in the data
state_data = pd.read_csv(input_file)
print('Data read!')
print('\n')

#Make the graphs
fig1 = plt.figure(figsize = (8,8)) #figure size
ind = np.arange(len(state_data['LRR'])) #Order by x-axis variable
width = 0.35 #the width of the bars

#Make each graph
p1 = plt.plot(ind, state_data['LRR']) 
plt.xticks(ind+width/2,(state_data['State']))

fig2 = plt.figure(figsize = (8,8)) #figure size
p2 = plt.bar(ind, state_data['Age'], width, color = "red")
plt.show()
print('Made graph 1 and 2!')
print('X off the viewer to continue')
print('\n')

#OVERLAPPING FIGURES
t = np.linspace(0,2*math.pi,400)
a = np.sin(t)
b = np.cos(t)
c = a + b

plt.plot(t,a,'r')
plt.plot(t,b,'b')
plt.plot(t,c,'g')
plt.show()

print('Made graph 3!')
print('X off the viewer to continue')
print('\n')

#MULTIPLE FIGURES IN ONE WINDOW
# Prepare the data
t = np.linspace(-math.pi, math.pi, 1024)
s = np.random.randn(2, 256)

# Do the plot
grid_size = (5, 2)
 
# Plot 1
plt.subplot2grid(grid_size, (0, 0), rowspan=2, colspan=2)
plt.plot(t, np.sinc(t), c= '#000000')
 
# Plot 2
plt.subplot2grid(grid_size, (2, 0), rowspan=3, colspan=1)
plt.scatter(s[0], s[1], c= '#000000')
 
# Plot 2
plt.subplot2grid(grid_size, (2, 1), rowspan=3, colspan=1)
plt.plot(np.sin(2 * t), np.cos(0.5 * t), c= '#000000')
 
# Automagically fits things together
plt.tight_layout()
 
# Done !
plt.show()
print('Made graph 4!')
print('X off the viewer to continue')
print('\n')
'''

#BAR CHARTS
#Get the Data
os.chdir('//chnas06/MKT-Data/INTERNET/INET Admin/Sean/Projects/Data Visualization')
input_file2 = 'Satisfaction_Test2.csv'
satis_data = pd.read_csv(input_file2)
print('Data read!')
print('\n')

'''
#Enable ipython to display matplotlib graphs
#Variable processing
data = pd.DataFrame(satis_data)
data2 = data.set_index(data['Insurer'])
my_plot = data2.plot(kind = 'bar', stacked = True,title="Satisfaction by Carrier", color = ['#00b33c','#809fff','#808080','#ff8533','#cc0000'])
my_plot.set_xlabel("Insurer")
my_plot.set_ylabel("Satisfaction")
my_plot.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)
#plt.savefig("test.png", bbox_inches='tight')
pylab.show()
'''

#PIE CHART
# Data to plot
labels = ["Probably Will    ","    Might/Might Not","   Probably Won't"]
sizes = [85,13,2]
colors = ['#66ff33', '#808080', '#ff4d4d']
explode = (0.2, 0, 0)  # explode 1st slice
 
# Plot
fig = plt.figure(figsize=(12,12))
plt.rcParams['font.size'] = 36.0
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.0f%%', shadow=True, pctdistance=1.1, startangle=90)
#patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
#plt.legend(patches, labels, loc="best")

plt.axis('equal')
plt.savefig("Pie_Chart_Renew.png", bbox_inches='tight')
#plt.show()


#Make and show the graph


''' '''
'''
my_plot = company_group.unstack().plot(kind='bar',stacked=True,title="Customer Satisfaction by Carrier",figsize=(9, 7))
my_plot.set_xlabel("Insurer")
my_plot.set_ylabel("Satisfaction")
my_plot.legend(["Extreme","Pleased","Neutral","Bitter", "DEFCON 5"], loc=9,ncol=4)

'''