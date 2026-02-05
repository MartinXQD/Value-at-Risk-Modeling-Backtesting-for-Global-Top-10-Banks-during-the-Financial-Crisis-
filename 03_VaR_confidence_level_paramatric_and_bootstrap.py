
# parametric method for historical VaR confidence interval

z = -2.326
CI_lo = np.full(len(his_return_data), np.nan)
CI_hi = np.full(len(his_return_data), np.nan)


for i in range(10, len(his_return_data)):
    hist = his_return_data["Return"].iloc[:i].to_numpy()
    sig = hist.std(ddof=1)
    VaR_center = his_return_data["Historical_VaR"].iloc[i]
    CI_lo[i] = VaR_center - 1.96 * sig
    CI_hi[i] = VaR_center + 1.96 * sig

his_return_data["HistVaR_param_CI_low"] = CI_lo
his_return_data["HistVaR_param_CI_high"] = CI_hi

print (his_return_data.head())
print (his_return_data.tail())
print(his_return_data.shape)

# bootstrap method for exponential and historical VaR confidence interval

def boot_ci_hist(hist_returns, c=0.99, B=300, seed=123):
    r = np.asarray(hist_returns)
    n = len(r)
    rng = np.random.default_rng(seed)
    vals = np.empty(B)
    for b in range(B):
        sample = rng.choice(r, size=n, replace=True)
        vals[b] = -np.quantile(sample, 1-c)
    return np.quantile(vals, 0.025), np.quantile(vals, 0.975)

def boot_ci_exp(hist_returns, lam=0.995, c=0.99, B=300, seed=123):
    r = np.asarray(hist_returns)
    n = len(r)
    rng = np.random.default_rng(seed)
    w = exp_weight(n, lam)
    vals = np.empty(B)
    for b in range(B):
        sample = rng.choice(r, size=n, replace=True)
        vals[b] = find_c(sample, w, c)
    return np.quantile(vals, 0.025), np.quantile(vals, 0.975)


B = 300
lo_h = np.full(len(his_return_data), np.nan)
hi_h = np.full(len(his_return_data), np.nan)
lo_e = np.full(len(his_return_data), np.nan)
hi_e = np.full(len(his_return_data), np.nan)

for i in range(20, len(his_return_data)):
    hist = his_return_data["Return"].iloc[:i].to_numpy()
    lo_h[i], hi_h[i] = boot_ci_hist(hist, c=0.99, B=B, seed=123)
    lo_e[i], hi_e[i] = boot_ci_exp(hist, lam=0.995, c=0.99, B=B, seed=123)

his_return_data["HistVaR_boot_low"] = lo_h
his_return_data["HistVaR_boot_high"] = hi_h
his_return_data["ExpVaR_boot_low"] = lo_e
his_return_data["ExpVaR_boot_high"] = hi_e


print (his_return_data.tail())
print(his_return_data.shape)
