import pandas as pd
import numpy as np 

his_return_data = pd.read_csv("path for historical returns")
his_return_data["Date"] = pd.to_datetime(his_return_data["Date"], format = "%m/%d/%Y")
his_return_data = his_return_data.set_index("Date")
print (his_return_data.head())
print (his_return_data.tail())
print(his_return_data.shape)
