# AB-Test-Marketing-Effectiveness

## Project Overview
This project evaluates the effectiveness of two marketing campaigns using **A/B testing**. Through statistical analysis and hypothesis testing, we determine which campaign leads to higher conversion rates.

## Project Structure
- **Datasets/control_group.csv** – Data for the control group.
- **Datasets/test_group.csv** – Data for the test group.
- **ab_testing.py** – Contains functions for data preprocessing and analysis.
- **README.md** – Project documentation.

## Key Aspects Covered
- **Data Preprocessing**: Handling missing values, converting date formats, and preparing data for analysis.
- **Exploratory Data Analysis (EDA)**: Evaluating conversion rates, visualizing distributions, and comparing campaign performance.
- **Statistical Analysis**: Conducting hypothesis testing (t-test) to assess the significance of differences between the control and test groups.
- **Visualization**: Comparing distributions using histograms, boxplots, and bar charts.

## Findings
The A/B test analysis revealed significant insights:
- The conversion rate for the control group was **1.23%**, while for the test group, it reached **2.54%**.
- The test campaign demonstrated a **2.07x improvement** over the control campaign.
- A **t-test** confirmed statistical significance, yielding a **p-value of 0.001**, ensuring the observed improvement was not due to random chance.

## Visualizations
Below are key visualizations from the analysis:

### **Histogram of Conversion Rates**
![image](https://github.com/user-attachments/assets/cc501e5b-b7e5-4038-b3a0-4e888115b668)


### **Boxplots of Conversion Rates by Group**
![image](https://github.com/user-attachments/assets/2e47348c-2c1e-4558-8c88-bc5e1f523226)


### **Comparison of Average Conversion Rates**
![image](https://github.com/user-attachments/assets/7484c115-089d-463d-a2e0-0a592d242250)


## Recommendations
Based on the statistical results, the test campaign is **recommended as the primary marketing strategy**, as it significantly improves user engagement and conversion rates.

---
This project demonstrates how data-driven decision-making can optimize marketing effectiveness through rigorous A/B testing.

