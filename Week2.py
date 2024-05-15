import pandas as pd

# Load datasets
cab_data = pd.read_csv('C:/Users/a/Downloads/Cab_Data.csv')
customer_data = pd.read_csv('C:/Users/a/Downloads/Customer_ID.csv')
transaction_data = pd.read_csv('C:/Users/a/Downloads/Transaction_ID.csv')
city_data = pd.read_csv('C:/Users/a/Downloads/City.csv')

# Display the first few rows of each dataset
cab_data_head = cab_data.head()
customer_data_head = customer_data.head()
transaction_data_head = transaction_data.head()
city_data_head = city_data.head()

# Check for missing values and basic statistics
cab_data_info = cab_data.info()
customer_data_info = customer_data.info()
transaction_data_info = transaction_data.info()
city_data_info = city_data.info()

# Get basic statistics
cab_data_desc = cab_data.describe(include='all')
customer_data_desc = customer_data.describe(include='all')
transaction_data_desc = transaction_data.describe(include='all')
city_data_desc = city_data.describe(include='all')

(cab_data_head, customer_data_head, transaction_data_head, city_data_head,
 cab_data_info, customer_data_info, transaction_data_info, city_data_info,
 cab_data_desc, customer_data_desc, transaction_data_desc, city_data_desc)

# Convert relevant fields to appropriate data types in City.csv
city_data['Population'] = city_data['Population'].str.replace(',', '').astype(int)
city_data['Users'] = city_data['Users'].str.replace(',', '').astype(int)

# Merge datasets to create a master dataset
# Merge Cab_Data with Transaction_ID on 'Transaction ID'
cab_transaction_merged = pd.merge(cab_data, transaction_data, on='Transaction ID', how='left')

# Merge the result with Customer_ID on 'Customer ID'
cab_transaction_customer_merged = pd.merge(cab_transaction_merged, customer_data, on='Customer ID', how='left')

# Merge the result with City on 'City'
master_data = pd.merge(cab_transaction_customer_merged, city_data, on='City', how='left')

# Display the first few rows of the master dataset
master_data_head = master_data.head()
master_data_info = master_data.info()
master_data_desc = master_data.describe(include='all')

(master_data_head, master_data_info, master_data_desc)

import matplotlib.pyplot as plt

# Convert 'Date of Travel' to datetime format
master_data['Date of Travel'] = pd.to_datetime(master_data['Date of Travel'], origin='1899-12-30', unit='D')

# Extract year and month for analysis
master_data['Year'] = master_data['Date of Travel'].dt.year
master_data['Month'] = master_data['Date of Travel'].dt.month

# Seasonality in Cab Usage
# Group by year and month to get the number of trips
monthly_trips = master_data.groupby(['Year', 'Month']).size().reset_index(name='Number of Trips')

# Plot the number of trips over time
plt.figure(figsize=(12, 6))
plt.plot(monthly_trips['Year'].astype(str) + '-' + monthly_trips['Month'].astype(str), monthly_trips['Number of Trips'], marker='o')
plt.xticks(rotation=90)
plt.xlabel('Year-Month')
plt.ylabel('Number of Trips')
plt.title('Monthly Number of Cab Trips (2016-2018)')
plt.grid(True)
plt.show()
# The plot illustrates the monthly number of cab trips for each company (Pink Cab and Yellow Cab) from January 2016 to December 2018.

# Company Performance Comparison
# Group by year, month, and company to get the number of trips for each company
monthly_trips_company = master_data.groupby(['Year', 'Month', 'Company']).size().reset_index(name='Number of Trips')

# Plot the number of trips for each company over time
plt.figure(figsize=(12, 6))
for company in monthly_trips_company['Company'].unique():
    company_data = monthly_trips_company[monthly_trips_company['Company'] == company]
    plt.plot(company_data['Year'].astype(str) + '-' + company_data['Month'].astype(str), company_data['Number of Trips'], marker='o', label=company)

plt.xticks(rotation=90)
plt.xlabel('Year-Month')
plt.ylabel('Number of Trips')
plt.title('Monthly Number of Cab Trips by Company (2016-2018)')
plt.legend()
plt.grid(True)
plt.show()


# Customer Segmentation
# Plot the distribution of customers by gender
plt.figure(figsize=(8, 6))
gender_counts = master_data['Gender'].value_counts()
plt.bar(gender_counts.index, gender_counts.values, color=['blue', 'pink'])
plt.xlabel('Gender')
plt.ylabel('Number of Customers')
plt.title('Customer Distribution by Gender')
plt.show()

# Plot the distribution of customers by age
plt.figure(figsize=(12, 6))
plt.hist(master_data['Age'], bins=30, color='green', edgecolor='black')
plt.xlabel('Age')
plt.ylabel('Number of Customers')
plt.title('Customer Distribution by Age')
plt.show()

# Plot the distribution of customers by income
plt.figure(figsize=(12, 6))
plt.hist(master_data['Income (USD/Month)'], bins=30, color='orange', edgecolor='black')
plt.xlabel('Income (USD/Month)')
plt.ylabel('Number of Customers')
plt.title('Customer Distribution by Income')
plt.show()

# Revenue and Cost Analysis
# Calculate the margin for each trip
master_data['Margin'] = master_data['Price Charged'] - master_data['Cost of Trip']

# Group by year and month to get the total number of trips and average margin
monthly_margin = master_data.groupby(['Year', 'Month']).agg({'Transaction ID': 'count', 'Margin': 'mean'}).reset_index()
monthly_margin.columns = ['Year', 'Month', 'Number of Trips', 'Average Margin']

# Plot the relationship between the number of trips and the average margin
plt.figure(figsize=(12, 6))
plt.scatter(monthly_margin['Number of Trips'], monthly_margin['Average Margin'], color='purple', alpha=0.6)
plt.xlabel('Number of Trips')
plt.ylabel('Average Margin')
plt.title('Relationship between Number of Trips and Average Margin')
plt.grid(True)
plt.show()

# Geographical Analysis
# Group by city to get the number of trips and average margin for each city
city_analysis = master_data.groupby('City').agg({'Transaction ID': 'count', 'Margin': 'mean'}).reset_index()
city_analysis.columns = ['City', 'Number of Trips', 'Average Margin']

# Sort cities by the number of trips
city_analysis = city_analysis.sort_values(by='Number of Trips', ascending=False)

# Plot the number of trips and average margin for each city
fig, ax1 = plt.subplots(figsize=(14, 8))

color = 'tab:blue'
ax1.set_xlabel('City')
ax1.set_ylabel('Number of Trips', color=color)
ax1.bar(city_analysis['City'], city_analysis['Number of Trips'], color=color, alpha=0.6)
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticklabels(city_analysis['City'], rotation=90)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Average Margin', color=color)
ax2.plot(city_analysis['City'], city_analysis['Average Margin'], color=color, marker='o')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Number of Trips and Average Margin by City')
plt.show()

# 1.Yellow Cab consistently had the maximum number of users each month from January 2016 to December 2018.
# 2.The number of trips and the average margin have a negative correlation which shows that higher volume does not necessarilty result in higher margins.
# 3.# Gender: The majority of customers are male.
# Age: The age distribution of customers is fairly spread out, with a notable concentration in the 25-45 age range.
# Income: The income distribution shows a wide range, with most customers earning between $5,000 and $20,000 per month.