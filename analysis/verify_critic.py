import sys; sys.path.insert(0, sys.argv[2])
from load import load
from collections import Counter
from math import sqrt
D = load(sys.argv[1]); Y='second_purchase_within_60d'
iss=lambda x: x['packaging_issue']!='None'
cc=lambda x: x['subscription_offer']=='Choose cadence'
T1=[x for x in D if not cc(x) and not iss(x) and x['first_order_returned']==0 and x['estimated_consumption_days']<=60]
near=lambda e: min((30,45,60), key=lambda c: abs(c-e))
c53=[x for x in T1 if 53<=x['estimated_consumption_days']<=60]
print("#1 T1 with consumption 53-60:", len(c53), "bought:", sum(x[Y] for x in c53), " default cadence:", Counter(near(x['estimated_consumption_days']) for x in c53))
print("   T1 default cadence distribution:", Counter(near(x['estimated_consumption_days']) for x in T1))
print("   T1 cons 46-52:", len([x for x in T1 if 46<=x['estimated_consumption_days']<=52]))
cells=Counter((x['acquisition_channel'], iss(x)) for x in D if cc(x)); print("#2 CC counts by channel x issue:", dict(cells))
print("#3 issue&CC", sum(x[Y] for x in D if iss(x) and cc(x)), "/", sum(1 for x in D if iss(x) and cc(x)), " issue&notCC", sum(x[Y] for x in D if iss(x) and not cc(x)), "/", sum(1 for x in D if iss(x) and not cc(x)))
s=2000/(76/180); print("#4 screened", round(s,1), "issue cases", round(s*52/180,1), "INR", round(s*52/180*65), " 29% of 2000 =", 0.289*2000, "  CI half-width at 1000/arm p=.55:", round(100*1.96*sqrt(2*.55*.45/1000),2))
print("#5 T1 marketplace", sum(x['acquisition_channel']=='Marketplace' for x in T1), "/", len(T1))
