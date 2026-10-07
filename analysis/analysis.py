import sys; sys.path.insert(0, sys.argv[2])
from load import load
from math import sqrt
from collections import defaultdict
D = load(sys.argv[1]); Y='second_purchase_within_60d'
def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (100*(c-h),100*(c+h))
def rate(rows):
    k=sum(r[Y] for r in rows); n=len(rows); lo,hi=wilson(k,n)
    return f"{k:>3}/{n:<3} = {100*k/n if n else 0:5.1f}%  CI {lo:4.1f}-{hi:4.1f}{'  (n<20)' if n<20 else ''}"
def by(key, rows=D, title=None):
    print(f"\n-- {title or key}")
    g=defaultdict(list)
    for r in rows: g[key(r) if callable(key) else r[key]].append(r)
    for k in sorted(g, key=str): print(f"  {str(k):<28} {rate(g[k])}")
    return g
print("ALL", rate(D))
for k in ['subscription_offer','acquisition_channel','product_family','first_order_discount_pct','packaging_issue','recommended_reorder_days','household_size','first_order_returned','delivery_delay_days']:
    by(k)
by(lambda r: 'issue' if r['packaging_issue']!='None' else 'none', title='any packaging issue')
by(lambda r: '0-2' if r['delivery_delay_days']<=2 else ('3-4' if r['delivery_delay_days']<=4 else '5+'), title='delay bucket')
by(lambda r: '<6' if r['first_order_satisfaction_score_10']<6 else ('6-7.9' if r['first_order_satisfaction_score_10']<8 else '8+'), title='satisfaction bucket')
by(lambda r: '<=30' if r['estimated_consumption_days']<=30 else ('31-45' if r['estimated_consumption_days']<=45 else ('46-60' if r['estimated_consumption_days']<=60 else '>60')), title='consumption bucket')
gap=lambda r: r['recommended_reorder_days']-r['estimated_consumption_days']
by(lambda r: 'early >7d' if gap(r)< -7 else ('aligned +-7' if abs(gap(r))<=7 else 'late >7d'), title='reorder timing vs consumption (rec - est)')
by(lambda r: 'early >7d' if gap(r)< -7 else ('aligned +-7' if abs(gap(r))<=7 else 'late >7d'), rows=[r for r in D if r['estimated_consumption_days']<=60], title='timing, consumption<=60 only')
by(lambda r: (r['subscription_offer'], r['acquisition_channel']), title='offer x channel')
by(lambda r: (r['subscription_offer'], r['packaging_issue']!='None'), title='offer x any issue')
by(lambda r: (r['acquisition_channel'], r['packaging_issue']!='None'), title='channel x issue')
by(lambda r: (r['first_order_discount_pct'], r['subscription_offer']), title='discount x offer')
# mean profile by offer
print("\n-- profile by offer (means)")
for o in ['Choose cadence','Fixed 30-day','Not offered']:
    R=[r for r in D if r['subscription_offer']==o]; n=len(R)
    m=lambda k: sum(r[k] for r in R)/n
    print(f"  {o:<15} n={n} disc={m('first_order_discount_pct'):.1f} delay={m('delivery_delay_days'):.2f} sat={m('first_order_satisfaction_score_10'):.2f} cons={m('estimated_consumption_days'):.1f} issue={sum(r['packaging_issue']!='None' for r in R)}/{n} ret={sum(r['first_order_returned'] for r in R)} mkt={sum(r['acquisition_channel']=='Marketplace' for r in R)} web={sum(r['acquisition_channel']=='Website' for r in R)} soc={sum(r['acquisition_channel']=='Social commerce' for r in R)} cons>60={sum(r['estimated_consumption_days']>60 for r in R)}")
