import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from scipy import stats

# 1. Downloading and Pre-processing Data

# Download the dataset for the control and test groups
control = pd.read_csv("Datasets/control_group.csv", sep=';')
test = pd.read_csv("Datasets/test_group.csv", sep=';')

# Dataset overview
print(control.head(), '\n')
print(control.info(), '\n')
print(control.columns, '\n\n\n')

print(test.head(), '\n')
print(test.info(), '\n')
print(control.columns, '\n\n\n')

# Convert values in the 'Date' column to datetime format
control['Date'] = pd.to_datetime(control['Date'], format='%d.%m.%Y')
test['Date'] = pd.to_datetime(test['Date'], format='%d.%m.%Y')

# Checking the number of missing values to be filled in control
print(f"Control missing values before filling: {control.isnull().sum().sum()}")

# Check for missing values and fill them in with average values
control = control.apply(lambda col: col.fillna(round(col.mean())) if np.issubdtype(col.dtype, np.number) else col)

# Checking the number of missing values after filling in control
print(f"Control missing values after filling: {control.isnull().sum().sum()}")


# Checking the number of missing values to fill in the test
print(f"Test missing values before filling: {test.isnull().sum().sum()}")

# Check for missing values and fill them in with average values
test = test.apply(lambda col: col.fillna(round(col.mean())) if np.issubdtype(col.dtype, np.number) else col)

# Checking the number of missing values after filling in the test
print(f"Test missing values after filling: {test.isnull().sum().sum()}")

print(control.head(), '\n')
print(test.head(), '\n')

# 2. Statistical Analysis

# Calculation of conversion rates for both campaigns
control['Conversion Rate (%)'] = (control['# of Purchase'] / control['# of Impressions']) * 100
test['Conversion Rate (%)'] = (test['# of Purchase'] / test['# of Impressions']) * 100

# Checking the calculation result
print(control[['Campaign Name', 'Date', 'Conversion Rate (%)']].head(), '\n')
print(test[['Campaign Name', 'Date', 'Conversion Rate (%)']].head(), '\n')

# Checking the normality of the distribution of conversion rates using the Shapiro-Wilk test
stat, p_value_control = stats.shapiro(control['Conversion Rate (%)'])
stat, p_value_test = stats.shapiro(test['Conversion Rate (%)'])
print(f"p-value for control group normality: {p_value_control}")
print(f"p-value for test group normality: {p_value_test}")

# Logarithmic transformation to normalise the distribution
control['Log Conversion Rate (%)'] = np.log(control['Conversion Rate (%)'] + 1)
test['Log Conversion Rate (%)'] = np.log(test['Conversion Rate (%)'] + 1)

# Checking the normality after transformation
stat_control_log, p_value_control_log = stats.shapiro(control['Log Conversion Rate (%)'])
stat_test_log, p_value_test_log = stats.shapiro(test['Log Conversion Rate (%)'])
print(f"p-value for control group after log transformation: {p_value_control_log}")
print(f"p-value for test group after log transformation: {p_value_test_log}")

# Carrying out a t-test on logarithmic values
t_stat, p_value = stats.ttest_ind(control['Log Conversion Rate (%)'], test['Log Conversion Rate (%)'], equal_var=False)
print(f"t-statistics: {t_stat}, p-value: {p_value}")

# 3. Visualisation of results

# Building a bar chart of average conversion rates
group_means = {
    'Group': ['Control', 'Test'],
    'Conversion Rate (%)': [
        control['Log Conversion Rate (%)'].mean(),
        test['Log Conversion Rate (%)'].mean()
    ]
}
group_means_df = pd.DataFrame(group_means)

plt.figure(figsize=(8, 5))
sns.barplot(x='Group', y='Conversion Rate (%)', data=group_means_df, palette=['#6095a3', '#f4a261'])
plt.title('Середні значення коефіцієнтів конверсії')
plt.ylabel('Conversion Rate (%)')
plt.xlabel('Group')
plt.show()

# Building boxspots for both groups
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.boxplot(data=control['Log Conversion Rate (%)'], ax=axes[0], color='#6095a3')
axes[0].set_title('Control Group')
axes[0].set_ylabel('Conversion Rate (%)')

sns.boxplot(data=test['Log Conversion Rate (%)'], ax=axes[1], color='#f4a261')
axes[1].set_title('Test Group')
axes[1].set_ylabel('Conversion Rate (%)')

fig.suptitle('Порівняння розподілу коефіцієнтів конверсії')
plt.tight_layout()
plt.show()

# Create histograms for both groups
plt.figure(figsize=(12, 5))
plt.hist(control['Log Conversion Rate (%)'], bins=15, alpha=0.5, label='Control', color='#6095a3')
plt.hist(test['Log Conversion Rate (%)'], bins=15, alpha=0.5, label='Test', color='#f4a261')
plt.title('Гістограми коефіцієнтів конверсії для контрольної та тестової групи')
plt.xlabel('Conversion Rate (%)')
plt.ylabel('Частота')
plt.legend()
plt.show()
