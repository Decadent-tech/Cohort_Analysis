import pandas as pd 

df = pd.read_csv('cohorts.csv')
print(df.head())

print(df.isnull().sum())

print(df.dtypes)

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
print(df['Date'].head())
print(df['Date'].dtype)  # should be datetime64[ns]
print(df.describe())
print(df.head())

import plotly.graph_objects as go
import plotly.express as px
# Create the plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Date'].dt.strftime('%Y-%m-%d'),  # force clean string dates
    y=df['New users'],
    mode='lines+markers',
    name='New Users'
))

fig.add_trace(go.Scatter(
    x=df['Date'].dt.strftime('%Y-%m-%d'),
    y=df['Returning users'],
    mode='lines+markers',
    name='Returning Users'
))

fig.update_layout(
    title='Trend of New and Returning Users Over Time',
    xaxis_title='Date',
    yaxis_title='Number of Users',
    xaxis=dict(
        tickangle=45
    )
)

fig.write_image('Cohort_trends/user_trend.png')
#fig.show()
# Cohort Analysis for User trend per duration
#fig = px.line(data_frame=df, x='Date', y=['Duration Day 1', 'Duration Day 7'], markers=True, labels={'value': 'Duration'})

fig.add_trace(go.Scatter(
    x=df['Date'].dt.strftime('%Y-%m-%d'),  # force clean string dates
    y=df[['Duration Day 1', 'Duration Day 7']].mean(axis=1),  # calculate mean duration for Day 1 and Day 7
    mode='lines+markers',
    name='Trend of Duration (Day 1 and Day 7) Over Time'
))


fig.update_layout(title='Trend of Duration (Day 1 and Day 7) Over Time', xaxis_title='Date', yaxis_title='Duration', xaxis=dict(tickangle=-45))
fig.write_image('Cohort_trends/duration_trend.png')

import seaborn as sns
import matplotlib.pyplot as plt

# Correlation matrix
correlation_matrix = df.corr()

# Plotting the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Variables')
#plt.show()
plt.savefig('Cohort_trends/correlation_matrix.png')

# Grouping data by week
df['Week'] = df['Date'].dt.isocalendar().week

# Calculating weekly averages
weekly_averages = df.groupby('Week').agg({
    'New users': 'mean',
    'Returning users': 'mean',
    'Duration Day 1': 'mean',
    'Duration Day 7': 'mean'
}).reset_index()

print(weekly_averages.head())


# Weekly Average of New vs. Returning Users
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=weekly_averages['Week'],
    y=weekly_averages['New users'],
    mode='lines+markers',
    name='Weekly Average New Users'
))
fig.add_trace(go.Scatter(
    x=weekly_averages['Week'],
    y=weekly_averages['Returning users'],
    mode='lines+markers',
    name='Weekly Average Returning Users'
))
fig.update_layout(
    title='Weekly Average of New vs. Returning Users',
    xaxis_title='Week',
    yaxis_title='Number of Users',
    xaxis=dict(tickangle=45)
)
fig.write_image('Cohort_trends/weekly_user_trend.png')


#Weekly Average of Duration (Day 1 vs. Day 7)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=weekly_averages['Week'],
    y=weekly_averages['Duration Day 1'],
    mode='lines+markers',
    name='Weekly Average Duration Day 1'
))
fig.add_trace(go.Scatter(
    x=weekly_averages['Week'],
    y=weekly_averages['Duration Day 7'],
    mode='lines+markers',
    name='Weekly Average Duration Day 7'
))
fig.update_layout(
    title='Weekly Average of Duration (Day 1 vs. Day 7)',
    xaxis_title='Week',
    yaxis_title='Duration',
    xaxis=dict(tickangle=45)
)
fig.write_image('Cohort_trends/weekly_duration_trend.png')


# Creating a cohort matrix
cohort_matrix = weekly_averages.set_index('Week')

# Plotting the cohort matrix
plt.figure(figsize=(12, 8))

sns.heatmap(cohort_matrix, annot=True, cmap='coolwarm', fmt=".1f")
plt.title('Cohort Matrix of Weekly Averages')
plt.ylabel('Week of the Year')
plt.savefig('Cohort_trends/cohort_matrix_weekly_averages.png')

#  number of new users and returning users fluctuates from week to week. 
# Notably, there was a significant increase in both new and returning users in Week 47.
#  The average duration of user engagement on Day 1 and Day 7 varies across the weeks. 
# The durations do not follow a consistent pattern about the number of new or returning users, 
# suggesting that other factors might be influencing user engagement.