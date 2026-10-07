# Emits the calculation register (markdown) used in the assurance report: every material statistic with filter, k, n, rate, CI.
import sys; sys.path.insert(0, sys.argv[2])
from load import load
from math import sqrt
D = load(sys.argv[1]); Y='second_purchase_within_60d'
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return f"{100*(c-h):.1f}–{100*(c+h):.1f}"
iss=lambda x: x['packaging_issue']!='None'
gap=lambda x: x['recommended_reorder_days']-x['estimated_consumption_days']
T1=lambda x: x['subscription_offer']!='Choose cadence' and not iss(x) and x['first_order_returned']==0 and x['estimated_consumption_days']<=60
rows=[
 ("All customers", lambda x: True),
 ("Offer = Choose cadence", lambda x: x['subscription_offer']=='Choose cadence'),
 ("Offer = Fixed 30-day", lambda x: x['subscription_offer']=='Fixed 30-day'),
 ("Offer = Not offered", lambda x: x['subscription_offer']=='Not offered'),
 ("Offer ≠ Choose cadence", lambda x: x['subscription_offer']!='Choose cadence'),
 ("Any recorded packaging issue", iss),
 ("packaging_issue = None", lambda x: not iss(x)),
 ("Damaged outer pack", lambda x: x['packaging_issue']=='Damaged outer pack'),
 ("Minor leak", lambda x: x['packaging_issue']=='Minor leak'),
 ("Wrong pack size", lambda x: x['packaging_issue']=='Wrong pack size'),
 ("Reorder rec. within ±7 d of consumption", lambda x: abs(gap(x))<=7),
 ("Reorder rec. >7 d early", lambda x: gap(x)<-7),
 ("Reorder rec. >7 d late", lambda x: gap(x)>7),
 ("Mismatched >7 d (early or late)", lambda x: abs(gap(x))>7),
 ("Consumption ≤30 d", lambda x: x['estimated_consumption_days']<=30),
 ("Consumption ≤30 d & late", lambda x: x['estimated_consumption_days']<=30 and gap(x)>7),
 ("Consumption >60 d", lambda x: x['estimated_consumption_days']>60),
 ("Discount 0%", lambda x: x['first_order_discount_pct']==0),
 ("Discount 10%", lambda x: x['first_order_discount_pct']==10),
 ("Discount 20%", lambda x: x['first_order_discount_pct']==20),
 ("Discount 30%", lambda x: x['first_order_discount_pct']==30),
 ("Discount 40%", lambda x: x['first_order_discount_pct']==40),
 ("Marketplace", lambda x: x['acquisition_channel']=='Marketplace'),
 ("Social commerce", lambda x: x['acquisition_channel']=='Social commerce'),
 ("Website", lambda x: x['acquisition_channel']=='Website'),
 ("Returned first order", lambda x: x['first_order_returned']==1),
 ("PRIMARY TARGET T1", T1),
 ("T1 & Not offered", lambda x: T1(x) and x['subscription_offer']=='Not offered'),
 ("T1 & Fixed 30-day", lambda x: T1(x) and x['subscription_offer']=='Fixed 30-day'),
 ("T1 & Marketplace", lambda x: T1(x) and x['acquisition_channel']=='Marketplace'),
 ("Choose cadence with T1's other filters", lambda x: x['subscription_offer']=='Choose cadence' and not iss(x) and x['first_order_returned']==0 and x['estimated_consumption_days']<=60),
 ("Issue & offer ≠ Choose cadence", lambda x: iss(x) and x['subscription_offer']!='Choose cadence'),
 ("Issue & Choose cadence", lambda x: iss(x) and x['subscription_offer']=='Choose cadence'),
]
print("| Filter | k (bought again) | n | Rate | 95% Wilson CI |\n|---|---:|---:|---:|---|")
for lab,f in rows:
    R=[x for x in D if f(x)]; k=sum(x[Y] for x in R); n=len(R)
    print(f"| {lab} | {k} | {n} | {100*k/n:.1f}% | {wilson(k,n)}{' (n<20)' if n<20 else ''} |")
