import pandas as pd

#Specify our working directory and the name of the csv we want to import then read that into a Pandas dataframe
os.chdir('//chnas01/urc/URC-Private/Research/Modeling Team/Users/Sean/Misc/Python')
input_file = 'Test_Python_Set.csv'

#Read in the data
state_data = pd.read_csv(input_file)
print('Data read!')
print('\n')

pip install -U git+https://github.com/aplavin/pandasql.git
