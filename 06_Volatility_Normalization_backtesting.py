import matplotlib.pyplot as plt

win = 21
normal_return_data = his_return_data.copy()
r = normal_return_data["Return"]

normal_return_data["sigma_month"] = r.rolling(win).std(ddof=1).shift(1)
normal_return_data["r_norm"] = normal_return_data["Return"] / normal_return_data["sigma_month"]

tmp = normal_return_data.dropna(subset=["r_norm"])


plt.figure()
plt.hist(tmp["Return"], bins=50, alpha=0.6, label="Original returns")
plt.hist(tmp["r_norm"], bins=50, alpha=0.6, label="Normalized returns")
plt.legend(); plt.title("Distribution: original vs normalized"); plt.show()

print(tmp[["Return","r_norm"]].describe())

c = 0.99

VaR_mixed = np.full(len(normal_return_data), np.nan)

for i in range(win+1, len(normal_return_data)):
    
    norm_hist = normal_return_data["r_norm"].iloc[:i].dropna().to_numpy()
    q = np.quantile(norm_hist, 1-c)
    VaR_mixed[i] = -q * normal_return_data["sigma_month"].iloc[i]

normal_return_data["VaR_mixed"] = VaR_mixed

normal_return_data["ex_mixed"] = (normal_return_data["Return"] < -normal_return_data["VaR_mixed"]).astype(int)
data_15_17 = normal_return_data.loc["2015-01-01":"2017-12-19"].copy()

x3 =  data_15_17["ex_mixed"].sum()
print(f"There are {x3} trading days that loss more than VaR under mixed methods \n")
