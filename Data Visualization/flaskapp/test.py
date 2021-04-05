# import pandas as pd

# df = pd.read_csv('timeseries.csv')
# df['newdate'] = None
# df['newdate']=df.date.str.split(' ').str[0].tolist()
# df['newdate'] = df['newdate'].astype('datetime64[ns]')
# df['date'] = df['date'].astype('datetime64[ns]')
# df['newdate'] = df['newdate'].astype(str)
# df["newdate"] = pd.to_datetime(df["newdate"])

# after_start_date = df["newdate"] >= start_date
# before_end_date = df["newdate"] <= end_date
# between_two_dates = after_start_date & before_end_date
# filtered_dates = df.loc[between_two_dates]

# filtered_dates['date'] = filtered_dates['date'].apply(str)
# date_list = filtered_dates['date'].values.tolist()

# count_labels = filtered_dates['cnt'].values.tolist()

l = [1,2,3,4,5,6,7,8,9,0]
top=7
print(l)
l = l[:top]
print(l)