import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from scipy import stats

# 1. Завантаження та Попередня Обробка Даних

# Завантажте набір даних для контрольної та тестової груп
control = pd.read_csv("Datasets/control_group.csv", sep=';')
test = pd.read_csv("Datasets/test_group.csv", sep=';')

# Огляд датасетів 
print(control.head(), '\n')
print(control.info(), '\n')
print(control.columns, '\n\n\n')

print(test.head(), '\n')
print(test.info(), '\n')
print(control.columns, '\n\n\n')

# Перетворення значень у колонці 'Date' на формат datetime
control['Date'] = pd.to_datetime(control['Date'], format='%d.%m.%Y')
test['Date'] = pd.to_datetime(test['Date'], format='%d.%m.%Y')

# Перевірка кількості пропущених значень до заповнення у control
print(f"Control missing values before filling: {control.isnull().sum().sum()}")

# Перевірка на пропущені значення та заповнення їх середніми значеннями
control = control.apply(lambda col: col.fillna(round(col.mean())) if np.issubdtype(col.dtype, np.number) else col)

# Перевірка кількості пропущених значень після заповнення у control
print(f"Control missing values after filling: {control.isnull().sum().sum()}")


# Перевірка кількості пропущених значень до заповнення у test
print(f"Test missing values before filling: {test.isnull().sum().sum()}")

# Перевірка на пропущені значення та заповнення їх середніми значеннями
test = test.apply(lambda col: col.fillna(round(col.mean())) if np.issubdtype(col.dtype, np.number) else col)

# Перевірка кількості пропущених значень після заповнення у test
print(f"Test missing values after filling: {test.isnull().sum().sum()}")

print(control.head(), '\n')
print(test.head(), '\n')

# 2. Статистичний Аналіз

# Розрахунок коефіцієнтів конверсії для обох кампаній
control['Conversion Rate (%)'] = (control['# of Purchase'] / control['# of Impressions']) * 100
test['Conversion Rate (%)'] = (test['# of Purchase'] / test['# of Impressions']) * 100

# Перевірка результату розрахунків
print(control[['Campaign Name', 'Date', 'Conversion Rate (%)']].head(), '\n')
print(test[['Campaign Name', 'Date', 'Conversion Rate (%)']].head(), '\n')

# Перевірка нормальності розподілу коефіцієнтів конверсії за допомогою тесту Шапіро-Вілка
stat, p_value_control = stats.shapiro(control['Conversion Rate (%)'])
stat, p_value_test = stats.shapiro(test['Conversion Rate (%)'])
print(f"p-value for control group normality: {p_value_control}")
print(f"p-value for test group normality: {p_value_test}")

# Логарифмічна трансформація для нормалізації розподілу
control['Log Conversion Rate (%)'] = np.log(control['Conversion Rate (%)'] + 1)
test['Log Conversion Rate (%)'] = np.log(test['Conversion Rate (%)'] + 1)

# Перевірка нормальності після трансформації
stat_control_log, p_value_control_log = stats.shapiro(control['Log Conversion Rate (%)'])
stat_test_log, p_value_test_log = stats.shapiro(test['Log Conversion Rate (%)'])
print(f"p-value for control group after log transformation: {p_value_control_log}")
print(f"p-value for test group after log transformation: {p_value_test_log}")

# Проведення t-тесту на логарифмованих значеннях
t_stat, p_value = stats.ttest_ind(control['Log Conversion Rate (%)'], test['Log Conversion Rate (%)'], equal_var=False)
print(f"t-statistics: {t_stat}, p-value: {p_value}")

# 3. Візуалізація Результатів

# Побудова стовпчастої діаграми середніх значень коефіцієнтів конверсії
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

# Побудова боксплотів для обох груп
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

# Побудова гістограм для обох груп
plt.figure(figsize=(12, 5))
plt.hist(control['Log Conversion Rate (%)'], bins=15, alpha=0.5, label='Control', color='#6095a3')
plt.hist(test['Log Conversion Rate (%)'], bins=15, alpha=0.5, label='Test', color='#f4a261')
plt.title('Гістограми коефіцієнтів конверсії для контрольної та тестової групи')
plt.xlabel('Conversion Rate (%)')
plt.ylabel('Частота')
plt.legend()
plt.show()