def exp_weight(n, lambda1):
    exponents = np.arange(n,0,-1)
    w = (1 - lambda1) * lambda1 ** (exponents-1)
    return w / w.sum()

def find_c (returns, w, c): 
    returns = np.asarray (returns )
    w = np.asarray (w)
    sorted_idx  =  np.argsort (returns)
    r_sorted = returns[sorted_idx]
    w_sorted = w [ sorted_idx]
    cum_w = np.cumsum(w_sorted)
    return -r_sorted[np.searchsorted(cum_w, 1-c, side = "left")]

VaR_1 = np.full(len(his_return_data),np.nan)
for i in range (1, len(his_return_data["Return"])):
    his_return = his_return_data["Return"].iloc[:i]
    weight = exp_weight (i, 0.995)
    VaR_1[i] = find_c (his_return, weight, 0.99)

his_return_data["Exponential_VaR"] = VaR_1

print (his_return_data.head())
print (his_return_data.tail())
print(his_return_data.shape)

VaR_2 = np.full(len(his_return_data),np.nan)
for i in range (1, len(his_return_data["Return"])):
    his_return = his_return_data["Return"].iloc[:i]
    VaR_2 [i] = -np.quantile (his_return, 0.01)

his_return_data["Historical_VaR"] = VaR_2

print (his_return_data.head())
print (his_return_data.tail())
print(his_return_data.shape)


VaR_2015_17 = his_return_data[[ "Return","Exponential_VaR", "Historical_VaR"]].loc["2015-01-01":"2017-12-19"].copy()
print (VaR_2015_17.head())
print (VaR_2015_17.tail())
print(VaR_2015_17.shape)


VaR_2015_17["Exceptions_ex"] = (VaR_2015_17["Return"] < (-VaR_2015_17["Exponential_VaR"])).astype(int)
VaR_2015_17["Exceptions_his"] = (VaR_2015_17["Return"] < (-VaR_2015_17["Historical_VaR"])).astype(int)
x1 = VaR_2015_17["Exceptions_ex"].sum()
x2 = VaR_2015_17["Exceptions_his"].sum()
print (f"There are {x2} trading days that loss more than VaR under Historical methods\n")
print (f"There are {x1} trading days that loss more than VaR under Exponential methods \n")
