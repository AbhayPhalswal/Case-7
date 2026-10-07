from math import sqrt, ceil
from statistics import NormalDist
Z=NormalDist().inv_cdf
def n_arm(p1,p2,alpha=0.05,power=0.80):
    za=Z(1-alpha/2); zb=Z(power); pb=(p1+p2)/2
    return ((za*sqrt(2*pb*(1-pb))+zb*sqrt(p1*(1-p1)+p2*(1-p2)))**2)/(p2-p1)**2
p1=0.526
for d in (0.05,0.07,0.08,0.10,0.12,0.15):
    print(f"MDE {d*100:.0f} pts: n/arm={n_arm(p1,p1+d):7.1f} -> {ceil(n_arm(p1,p1+d))}   (alpha .025 for 2 comparisons: {ceil(n_arm(p1,p1+d,alpha=0.025))})")
# with historical n=38 per arm, what MDE?
for n in (38,400,500,800):
    # solve MDE by bisection
    lo,hi=0.001,0.47
    for _ in range(60):
        m=(lo+hi)/2
        if n_arm(p1,p1+m)>n: lo=m
        else: hi=m
    print(f"n/arm={n}: MDE={100*hi:.1f} pts; 95% CI half-width of diff at p~0.58: {100*1.96*sqrt(2*0.58*0.42/n):.1f} pts")
print("observed stratified gap ~36-40; quarter of 40 =",40/4)
