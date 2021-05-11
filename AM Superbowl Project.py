# Import packages
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import CSV file into a Pandas DataFrame and parse the Date column
superbowl = pd.read_csv("superbowl.csv", parse_dates=['Date'])
print(superbowl.shape, superbowl.info())

# API Request
Tampa_conditions = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Tampa&units=metric&appid=f648e458e1a21dbb28ba43bf164dceed")
print(Tampa_conditions)
print(Tampa_conditions.text)
print(type(Tampa_conditions.json()))
Tampa_conditions = Tampa_conditions.json()
print(Tampa_conditions['wind'])
print(Tampa_conditions['main'])

# Create a DataFrame from a dictionary of lists
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
         'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
         'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
         'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
         'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina','South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
         'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
postal_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
                'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
                'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
state_capitals = ['Montgomery', 'Juneau', 'Phoenix', 'Little Rock', 'Sacramento', 'Denver', 'Hartford', 'Dover', 'Tallahassee',
                  'Atlanta', 'Honolulu', 'Boise', 'Springfield', 'Indianapolis', 'Des Moines', 'Topeka', 'Frankfort',
                  'Baton Rouge', 'Augusta', 'Annapolis', 'Boston', 'Lansing', 'Saint Paul', 'Jackson', 'Jefferson City',
                  'Helena', 'Lincoln', 'Carson City', 'Concord', 'Trenton', 'Santa Fe', 'Albany', 'Raleigh', 'Bismarck', 'Columbus',
                  'Oklahoma City', 'Salem', 'Harrisburg', 'Providence', 'Columbia', 'Pierre', 'Nashville', 'Austin', 'Salt Lake City',
                  'Montpelier', 'Richmond', 'Olympia', 'Charleston', 'Madison', 'Cheyenne']

US_States_dictionary = {"State": states, "Code": postal_codes, "Capital": state_capitals}
US_States = pd.DataFrame(US_States_dictionary)
print(US_States)

# Merge DataFrames
superbowl_US_States = pd.merge(superbowl, US_States, on='State', how ='left')
print(superbowl_US_States.info())
print(superbowl_US_States.head())

# Drop duplicates
superbowl_US_States = superbowl_US_States.drop_duplicates(subset="SB")
print(superbowl_US_States.shape)

# Drop unwanted columns
superbowl_US_States.drop(superbowl_US_States.iloc[:, np.r_[-6:-4, -2]], inplace=True, axis=1)
print(superbowl_US_States.info())

# Check for missing values
missing_values_count = superbowl_US_States.isnull().sum()
print(missing_values_count)

# Add a column derived from subtracting one column from another
superbowl_US_States['Winning_Margin'] = superbowl_US_States['Winner Pts'] - superbowl_US_States['Loser Pts']
print(superbowl_US_States.info())

# Add a column derived from adding one column to another
superbowl_US_States['Combined_Score'] = superbowl_US_States['Winner Pts'] + superbowl_US_States['Loser Pts']

# Add a column by using iterrows() method in combination with a for loop:
for index, row in superbowl_US_States.iterrows():
    superbowl_US_States.loc[index, 'Cap_Host'] = row['City'] == row['Capital']
print(superbowl_US_States.head())
print(superbowl_US_States.info())

# Set the Date column as the Index
superbowl_US_States = superbowl_US_States.set_index('Date')
print(superbowl_US_States.head())
print(superbowl_US_States.info())

# Find out how many times the Super Bowl has been hosted by a State Capital and plot it
Cap_Host_Count = superbowl_US_States['Cap_Host'].value_counts()
print(Cap_Host_Count)
Cap_Host_Count_Df = superbowl_US_States[superbowl_US_States['Cap_Host']==True]
print(Cap_Host_Count_Df[['SB', 'Winner', 'City']])
sns.countplot(x='City', data=Cap_Host_Count_Df).set_title('State Capital hosts the Super Bowl')
plt.show()

# Plot time series data to see the Winning Margin over Time
fig, ax = plt.subplots()
ax.plot(superbowl_US_States.index, superbowl_US_States['Winning_Margin'], marker = "v", color = "b")
ax.set_xlabel('Time')
ax.set_ylabel('Winning Margin (points)')
ax.set_title('The Super Bowl Winning Margin Over Time')
plt.show()

# Plot time series data to see the Combined Score over Time
fig, ax = plt.subplots()
ax.plot(superbowl_US_States.index, superbowl_US_States['Combined_Score'], marker = "o", color = "r")
ax.set_xlabel('Time')
ax.set_ylabel('Combined Score (points)')
ax.set_title('The Super Bowl Combined Score Over Time')
plt.show()

# Create a countplot to demonstrate who has won a lot of Super Bowls
sns.countplot(y='Winner', data=superbowl_US_States).set_title('Super Bowl Wins by Team')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Create a countplot to demonstrate who has lost the most Super Bowls
sns.countplot(y='Loser', data=superbowl_US_States).set_title('Super Bowl Losses by Team')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Create a bar chart to see the Mean Points of a Winning Team across all their Wins
mean_winning_pts_by_team = superbowl_US_States.groupby('Winner')['Winner Pts'].mean()
print(mean_winning_pts_by_team)
mean_winning_pts_by_team.plot(kind = 'bar', title = "Mean Winner Points by Team in the Super Bowl")
plt.tight_layout()
plt.show()

# Create a countplot to demonstrate which Cities have hosted the Super Bowl most often
sns.countplot(y="City", data=superbowl_US_States).set_title('the Super Bowl Host Cities')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Calculate the total appearances by a team in the Super Bowl by considering the Winner and Loser columns
superbowl_appearances = pd.Series(superbowl_US_States[['Winner', 'Loser']].values.flatten()).value_counts()
print(superbowl_appearances)

# Subset a pandas series of teams that have appeared in at least 5 Super Bowls and create a plot
five_or_more_superbowl_appearances  = superbowl_appearances[superbowl_appearances>=5]
print(five_or_more_superbowl_appearances)
ax = five_or_more_superbowl_appearances.plot.bar()
ax.set_title("5 or more Super Bowl appearances")
ax.set_xlabel('Teams')
ax.set_ylabel("Superbowl Appearances")
plt.tight_layout()
plt.show()

# Group by winner and get points statistics
superbowl_points_stats = superbowl_US_States.groupby('Winner')[['Winner Pts', 'Loser Pts']].agg([np.min, np.max, np.median])
print(superbowl_points_stats)

# Function to create reusable code
def plot_and_customize_timeseries(axes,x,y,color,marker,xlabel,ylabel,title):
    axes.plot(x,y, color=color, marker=marker)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel, color=color, marker=marker)
    axes.set_title(title)









































































