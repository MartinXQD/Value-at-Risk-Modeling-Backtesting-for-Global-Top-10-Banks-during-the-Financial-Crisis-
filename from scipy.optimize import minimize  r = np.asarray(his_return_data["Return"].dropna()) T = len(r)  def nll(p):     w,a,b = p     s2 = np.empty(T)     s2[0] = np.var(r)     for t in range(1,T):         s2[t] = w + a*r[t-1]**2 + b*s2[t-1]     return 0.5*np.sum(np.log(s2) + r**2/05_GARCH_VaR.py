from scipy.optimize import minimize

r = np.asarray(his_return_data["Return"].dropna())
T = len(r)

def nll(p):
    w,a,b = p
    s2 = np.empty(T)
    s2[0] = np.var(r)
    for t in range(1,T):
        s2[t] = w + a*r[t-1]**2 + b*s2[t-1]
    return 0.5*np.sum(np.log(s2) + r**2/s2)

res = minimize(nll, x0=[1e-6,0.05,0.9], method="Nelder-Mead")
w,a,b = res.x
sigma = np.sqrt(np.maximum(1e-12, np.array([np.var(r)] + [0]*(len(r)-1))))
s2 = np.empty_like(r)
s2[0]=np.var(r)

for t in range(1,len(r)): 
    s2[t]=w+a*r[t-1]**2+b*s2[t-1]
    
sigma = np.sqrt(s2)

z = 2.326
VaR_garch = z * sigma
print("params:", w,a,b, "converged:", res.success)
his_return_data.loc[his_return_data["Return"].notna(), "GARCH_VaR"] = VaR_garch
print (his_return_data["GARCH_VaR"])
