import sys; sys.path.insert(0, sys.argv[2])
from load import load
from math import sqrt, ceil
from collections import Counter, defaultdict
D = load(sys.argv[1]); Y='second_purchase_within_60d'
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return (round(100*(c-h),1),round(100*(c+h),1))
def r(R): k=sum(x[Y] for x in R); n=len(R); return f"{k}/{n} = {100*k/n:.1f}% CI{wilson(k,n)}" if n else "0"
gap=lambda x: x['recommended_reorder_days']-x['estimated_consumption_days']
tim=lambda x: 'early' if gap(x)<-7 else ('aligned' if abs(gap(x))<=7 else 'late')
iss=lambda x: x['packaging_issue']!='None'
print("timing x consumption bucket")
for b,(lo,hi) in {'<=30':(0,30),'31-45':(31,45),'46-60':(46,60),'>60':(61,999)}.items():
    R=[x for x in D if lo<=x['estimated_consumption_days']<=hi]
    print(" ",b, Counter(tim(x) for x in R), r(R))
print("satisfaction mean by issue:", {k: round(sum(x['first_order_satisfaction_score_10'] for x in D if iss(x)==k)/sum(1 for x in D if iss(x)==k),2) for k in (True,False)})
print("surface cleaner offers:", Counter(x['subscription_offer'] for x in D if x['product_family']=='Surface cleaner'), "issues", sum(iss(x) for x in D if x['product_family']=='Surface cleaner'))
print("est consumption range", min(x['estimated_consumption_days'] for x in D), max(x['estimated_consumption_days'] for x in D))
print("rec==nearest? count gap distribution:", Counter('early' if gap(x)<-7 else 'aligned' if abs(gap(x))<=7 else 'late' for x in D))
# candidate targets
T = {
 'T1 notCC & no issue & not returned & cons<=60': lambda x: x['subscription_offer']!='Choose cadence' and not iss(x) and x['first_order_returned']==0 and x['estimated_consumption_days']<=60,
 'T2 notCC & no issue & not returned': lambda x: x['subscription_offer']!='Choose cadence' and not iss(x) and x['first_order_returned']==0,
 'T3 notCC (all)': lambda x: x['subscription_offer']!='Choose cadence',
 'T4 Not offered only, clean, cons<=60': lambda x: x['subscription_offer']=='Not offered' and not iss(x) and x['first_order_returned']==0 and x['estimated_consumption_days']<=60,
 'T5 marketplace notCC clean': lambda x: x['acquisition_channel']=='Marketplace' and x['subscription_offer']!='Choose cadence' and not iss(x) and x['first_order_returned']==0,
 'CC with same filters as T1': lambda x: x['subscription_offer']=='Choose cadence' and not iss(x) and x['first_order_returned']==0 and x['estimated_consumption_days']<=60,
 'Issue (any) ': iss,
 'Issue & notCC': lambda x: iss(x) and x['subscription_offer']!='Choose cadence',
 'Returned': lambda x: x['first_order_returned']==1,
 'Returned & issue': lambda x: x['first_order_returned']==1 and iss(x),
 'cons>60': lambda x: x['estimated_consumption_days']>60,
 'cons>60 & notCC': lambda x: x['estimated_consumption_days']>60 and x['subscription_offer']!='Choose cadence',
 'cons>60 & CC': lambda x: x['estimated_consumption_days']>60 and x['subscription_offer']=='Choose cadence',
}
for k,f in T.items():
    R=[x for x in D if f(x)]
    print(f"{k:<46} {r(R)}  offer={dict(Counter(x['subscription_offer'] for x in R))} ch={dict(Counter(x['acquisition_channel'] for x in R))}")
T1=[x for x in D if T['T1 notCC & no issue & not returned & cons<=60'](x)]
print("T1 timing:", {t: r([x for x in T1 if tim(x)==t]) for t in ('early','aligned','late')})
print("T1 offer:", {o: r([x for x in T1 if x['subscription_offer']==o]) for o in ('Not offered','Fixed 30-day')})
print("T1 product:", Counter(x['product_family'] for x in T1))
print("T1 discount:", Counter(x['first_order_discount_pct'] for x in T1))
print("T1 rec != est:", sum(x['recommended_reorder_days']!=x['estimated_consumption_days'] for x in T1))
# exclusion waterfall from 180
s=D; print("\nwaterfall: 180")
for lab,f in [('choose cadence already',lambda x:x['subscription_offer']=='Choose cadence'),('packaging issue',iss),('returned',lambda x:x['first_order_returned']==1),('cons>60',lambda x:x['estimated_consumption_days']>60)]:
    rem=[x for x in s if f(x)]; s=[x for x in s if not f(x)]; print(f"  minus {lab}: -{len(rem)} -> {len(s)}")
# Not offered + issue + returned, used by AI later
print("Not offered: issue", sum(iss(x) for x in D if x['subscription_offer']=='Not offered'), "returned", sum(x['first_order_returned'] for x in D if x['subscription_offer']=='Not offered'), "both", sum(iss(x) and x['first_order_returned'] for x in D if x['subscription_offer']=='Not offered'))
mk=[x for x in D if x['acquisition_channel']=='Marketplace' and x['subscription_offer']=='Not offered']
print("Marketplace & Not offered:", len(mk), "issue", sum(iss(x) for x in mk), "returned", sum(x['first_order_returned'] for x in mk), r(mk), "clean", r([x for x in mk if not iss(x) and x['first_order_returned']==0]))
