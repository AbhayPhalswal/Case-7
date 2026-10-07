import sys; sys.path.insert(0, sys.argv[2])
from load import load
from math import sqrt, erf
D = load(sys.argv[1]); Y='second_purchase_within_60d'
def kn(R): return sum(x[Y] for x in R), len(R)
def p2(a,b):
    (k1,n1),(k2,n2)=a,b; p=(k1+k2)/(n1+n2); z=(k1/n1-k2/n2)/sqrt(p*(1-p)*(1/n1+1/n2)); return 2*(1-0.5*(1+erf(abs(z)/sqrt(2))))
iss=lambda x: x['packaging_issue']!='None'
gap=lambda x: x['recommended_reorder_days']-x['estimated_consumption_days']
cc=lambda x: x['subscription_offer']=='Choose cadence'
print("non-CC & issue & mismatched±10:", kn([x for x in D if (not cc(x)) and iss(x) and abs(gap(x))>10]))
for pop_name, pop in [("ALL", D), ("non-CC (n=131)", [x for x in D if not cc(x)]), ("CC (n=49)", [x for x in D if cc(x)]), ("T1", [x for x in D if not cc(x) and not iss(x) and x['first_order_returned']==0 and x['estimated_consumption_days']<=60])]:
    print("\n", pop_name)
    for t in (5,7,10,15):
        A=kn([x for x in pop if abs(gap(x))<=t]); M=kn([x for x in pop if abs(gap(x))>t])
        E=kn([x for x in pop if gap(x)<-t]); L=kn([x for x in pop if gap(x)>t])
        f=lambda q: f"{q[0]}/{q[1]}={100*q[0]/q[1]:.1f}%" if q[1] else "-"
        print(f"  ±{t:>2}: aligned {f(A):<14} mismatched {f(M):<14} gap {100*(A[0]/A[1]-M[0]/M[1]):5.1f} p={p2(A,M):.3f} | early {f(E):<14} late {f(L)}")
# absolute gap as continuous: logistic in non-CC
import numpy as np
P=[x for x in D if not cc(x)]
X=np.array([[1, abs(gap(x))/10, float(iss(x)), x['first_order_satisfaction_score_10']] for x in P]); y=np.array([x[Y] for x in P],float)
b=np.zeros(4)
for _ in range(50):
    p=1/(1+np.exp(-X@b)); H=X.T@(X*(p*(1-p))[:,None]); b+=np.linalg.solve(H,X.T@(y-p))
se=np.sqrt(np.diag(np.linalg.inv(H)))
print("\nnon-CC logistic: |gap|/10, issue, satisfaction ->", [(round(c,2), round(c/s,2)) for c,s in zip(b,se)])
# interaction in full model: timing aligned(±7) x CC
