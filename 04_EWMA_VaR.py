lam = 0.96
z = 2.326
r = his_return_data["Return"].to_numpy()
n = len(r)

sigma2 = np.full(n, np.nan)
VaR_ewma = np.full(n, np.nan)
sigma2[20] = np.var(r[:20], ddof=1)

for t in range(21, n):
    sigma2[t] = lam * sigma2[t-1] + (1-lam) * r[t-1]**2
    VaR_ewma[t] = z * np.sqrt(sigma2[t])

his_return_data["EWMA_sigma"] = np.sqrt(sigma2)
his_return_data["EWMA_VaR"] = VaR_ewma

print (his_return_data[["EWMA_sigma","EWMA_VaR"]])
