import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("Case2.xlsx", 0)  

rows = df.iloc[:, 0].fillna('').astype(str)
egypt_start = rows[rows.str.contains('EGYPT', case=False)].index[0]
ksa_start = rows[rows.str.contains('KSA', case=False)].index[0]

egypt_df = df.iloc[egypt_start:ksa_start].copy()
ksa_df = df.iloc[ksa_start:].copy()

dates = ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

egypt_processed = []
ksa_processed = []

disease1_rows = egypt_df.iloc[0:6]  
disease2_rows = egypt_df.iloc[6:12]  
consumption_rows = egypt_df.iloc[12:19] 

# print(disease1_rows)
# print(disease2_rows)
# print(consumption_rows)

for month_idx, month in enumerate(dates):
    month_data = {
        'Country': 'EGYPT',
        'Month': month,    
        'Year': 2024 if month_idx > 0 else 2023
    }
    
    metrics1 = ['Current Cases', 'New', 'In process', 'Drop out', 'Prospected']
    for i, metric in enumerate(metrics1):
        col_idx = month_idx + 3
        if col_idx < len(disease1_rows.columns):
            month_data[f'Disease1 {metric}'] = disease1_rows.iloc[i+1, col_idx]
    
    metrics2 = ['Current Cases', 'New', 'In process', 'Drop out', 'Prospected']
    for i, metric in enumerate(metrics2):
        col_idx = month_idx + 3
        if col_idx < len(disease2_rows.columns):
            month_data[f'Disease2 {metric}'] = disease2_rows.iloc[i+1, col_idx]
    
    consumption_metrics = ['Stock', 'coverage', 'Consumption ACT Unit', 
                           'PY ACT Consumption', 'Consumption growth vs PY', 'Imported goods' ]
    for i, metric in enumerate(consumption_metrics):
        col_idx = month_idx + 3
        if col_idx < len(consumption_rows.columns):
            month_data[f'drugA {metric}'] = consumption_rows.iloc[i+1, col_idx]
    
    egypt_processed.append(month_data)

egypt_data = pd.DataFrame(egypt_processed)
# print(egypt_data)
egypt_data.to_excel("egypt_data.xlsx")


disease1_rows = ksa_df.iloc[0:6]  
disease2_rows = ksa_df.iloc[6:12]  
consumption_rows = ksa_df.iloc[12:19]

# print(disease1_rows)
# print(disease2_rows)
# print(consumption_rows)


for month_idx, month in enumerate(dates):
    month_data = {
        'Country': 'KSA',
        'Month': month,
        'Year': 2024 if month_idx > 0 else 2023
    }
    
    metrics1 = ['Current Cases', 'New', 'In process', 'Drop out', 'Prospected']
    for i, metric in enumerate(metrics1):
        col_idx = month_idx + 3
        if col_idx < len(disease1_rows.columns):
            month_data[f'Disease1 {metric}'] = disease1_rows.iloc[i+1, col_idx]
    
    metrics2 = ['Current Cases', 'New', 'In process', 'Drop out', 'Prospected']
    for i, metric in enumerate(metrics2):
        col_idx = month_idx + 3
        if col_idx < len(disease2_rows.columns):
            month_data[f'Disease2 {metric}'] = disease2_rows.iloc[i+1, col_idx]
    
    consumption_metrics = ['Stock', 'coverage', 'Consumption ACT Unit', 
                           'PY ACT Consumption', 'Consumption growth vs PY', 'Imported goods']
    for i, metric in enumerate(consumption_metrics):
        col_idx = month_idx + 3
        if col_idx < len(consumption_rows.columns):
            month_data[f'drugA {metric}'] = consumption_rows.iloc[i+1, col_idx]
    
    ksa_processed.append(month_data)

ksa_data = pd.DataFrame(ksa_processed)
# print(ksa_data)
ksa_data.to_excel("ksa_data.xlsx")


egypt_disease1_total = egypt_data.filter(like='Disease1').sum(axis=1)
ksa_disease1_total = ksa_data.filter(like='Disease1').sum(axis=1)

egypt_disease2_total = egypt_data.filter(like='Disease2').sum(axis=1)
ksa_disease2_total = ksa_data.filter(like='Disease2').sum(axis=1)

egypt_drug_consumption = egypt_data.filter(like='drugA Consumption ACT Unit').sum(axis=1)
ksa_drug_consumption = ksa_data.filter(like='drugA Consumption ACT Unit').sum(axis=1)


plt.figure(figsize=(14, 6))

# Plot Disease1 and Disease2 
plt.subplot(1, 2, 1)
plt.plot(egypt_data['Month'] + ' ' + egypt_data['Year'].astype(str), egypt_disease1_total, label='Egypt Disease1 Cases')
plt.plot(ksa_data['Month'] + ' ' + ksa_data['Year'].astype(str), ksa_disease1_total, label='KSA Disease1 Cases')
plt.plot(egypt_data['Month'] + ' ' + egypt_data['Year'].astype(str), egypt_disease2_total, label='Egypt Disease2 Cases', linestyle='--')
plt.plot(ksa_data['Month'] + ' ' + ksa_data['Year'].astype(str), ksa_disease2_total, label='KSA Disease2 Cases', linestyle='--')
plt.title('Disease Cases Over Time')
plt.xlabel('Month')
plt.ylabel('Total Cases')
plt.xticks(rotation=45)
plt.legend()

# Plot Drug Consumption
plt.subplot(1, 2, 2)
plt.plot(egypt_data['Month'] + ' ' + egypt_data['Year'].astype(str), egypt_drug_consumption, label='Egypt Drug Consumption')
plt.plot(ksa_data['Month'] + ' ' + ksa_data['Year'].astype(str), ksa_drug_consumption, label='KSA Drug Consumption')
plt.title('Drug Consumption Over Time')
plt.xlabel('Month')
plt.ylabel('Total Consumption')
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.show()