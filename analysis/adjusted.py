import sys; sys.path.insert(0, sys.argv[2])
from load import load
import numpy as np
from collections import defaultdict
D = load(sys.argv[1]); Y='second_purchase_within_60d'
def feats(r):
    g=r['recommended_reorder_days']-r['estimated_consumption_days']
    return {
     'choose_cadence': r['subscription_offer']=='Choose cadence',
     'fixed_30': r['subscription_offer']=='Fixed 30-day',
     'pack_issue': r['packaging_issue']!='None',
     'returned': r['first_order_returned']==1,
     'disc_pct/10': r['first_order_discount_pct']/10,
     'delay_days': r['delivery_delay_days'],
     'satisfaction': r['first_order_satisfaction_score_10'],
     'cons>60': r['estimated_consumption_days']>60,
     'timing_aligned': abs(g)<=7,
     'marketplace': r['acquisition_channel']=='Marketplace',
     'social': r['acquisition_channel']=='Social commerce',
     'surface_cleaner': r['product_family']=='Surface cleaner',
    }
names=list(feats(D[0]).keys())
X=np.array([[1.0]+[float(v) for v in feats(r).values()] for r in D]); y=np.array([r[Y] for r in D],float)
b=np.zeros(X.shape[1])
for _ in range(50):
    p=1/(1+np.exp(-X@b)); W=p*(1-p); H=X.T@(X*W[:,None]); b+=np.linalg.solve(H, X.T@(y-p))
se=np.sqrt(np.diag(np.linalg.inv(H)))
print(f"{'term':<18}{'coef':>7}{'OR':>7}{'z':>7}")
for n_,bb,s in zip(['const']+names,b,se): print(f"{n_:<18}{bb:7.2f}{np.exp(bb):7.2f}{bb/s:7.2f}")
p=1/(1+np.exp(-X@b)); ll=np.sum(y*np.log(p)+(1-y)*np.log(1-p)); p0=y.mean(); ll0=len(y)*(p0*np.log(p0)+(1-p0)*np.log(1-p0))
print("McFadden R2", round(1-ll/ll0,3))
# Mantel-Haenszel risk difference: choose cadence vs not, stratified by channel x issue
def mh(strat, treat):
    g=defaultdict(list)
    for r in D: g[strat(r)].append(r)
    num=den=0
    for k,R in g.items():
        T=[r for r in R if treat(r)]; C=[r for r in R if not treat(r)]
        if not T or not C: continue
        n=len(R); w=len(T)*len(C)/n
        num+=w*(sum(r[Y] for r in T)/len(T)-sum(r[Y] for r in C)/len(C)); den+=w
    return 100*num/den
cc=lambda r: r['subscription_offer']=='Choose cadence'
print("crude RD choose vs other:", round(100*(40/49-55/131),1), " (other 55/131)")
print("MH RD | channel x issue:", round(mh(lambda r:(r['acquisition_channel'],r['packaging_issue']!='None'),cc),1))
print("MH RD | channel x issue x cons>60:", round(mh(lambda r:(r['acquisition_channel'],r['packaging_issue']!='None',r['estimated_consumption_days']>60),cc),1))
print("MH RD | discount:", round(mh(lambda r:r['first_order_discount_pct'],cc),1))
pi=lambda r: r['packaging_issue']!='None'
print("issue crude RD:", round(100*(19/52-76/128),1), " MH | offer x channel:", round(mh(lambda r:(r['subscription_offer'],r['acquisition_channel']),pi),1))
