import sys; sys.path.insert(0, sys.argv[2])
from load import load
from math import sqrt, erf
D = load(sys.argv[1]); Y='second_purchase_within_60d'
def r(R): k=sum(x[Y] for x in R); return f"{k}/{len(R)} = {100*k/len(R):.1f}%"
iss=lambda x: x['packaging_issue']!='None'
gap=lambda x: x['recommended_reorder_days']-x['estimated_consumption_days']
cc=lambda x: x['subscription_offer']=='Choose cadence'
W=lambda x: abs(gap(x))<=10
print("±10 matched:", r([x for x in D if W(x)]), " mismatched:", r([x for x in D if not W(x)]))
print("early (rec < est-10):", r([x for x in D if gap(x)<-10]), " late (rec > est+10):", r([x for x in D if gap(x)>10]))
print("non-CC matched:", r([x for x in D if not cc(x) and W(x)]), " non-CC mismatched:", r([x for x in D if not cc(x) and not W(x)]))
near=lambda e: min((30,45,60), key=lambda c: abs(c-e))
print("nearest-of-30/45/60 within 10d:", sum(abs(near(x['estimated_consumption_days'])-x['estimated_consumption_days'])<=10 for x in D), "/180")
print("non-CC no issue:", r([x for x in D if not cc(x) and not iss(x)]), " non-CC issue:", r([x for x in D if not cc(x) and iss(x)]))
print("issue & mismatched(±10):", r([x for x in D if iss(x) and not W(x)]))
print("CC & mismatched:", r([x for x in D if cc(x) and not W(x)]), " CC mismatched share", sum(cc(x) and not W(x) for x in D),"/49;  others mismatched", sum((not cc(x)) and not W(x) for x in D),"/131")
print("CC & issue:", r([x for x in D if cc(x) and iss(x)]))
dl=lambda x: x['delivery_delay_days']
print("delay 0-2", r([x for x in D if dl(x)<=2]), "3-4", r([x for x in D if 3<=dl(x)<=4]), "5+", r([x for x in D if dl(x)>=5]))
print("disc 30-40", r([x for x in D if x['first_order_discount_pct']>=30]), " 0-20", r([x for x in D if x['first_order_discount_pct']<=20]))
print("sat>=8", r([x for x in D if x['first_order_satisfaction_score_10']>=8]), " <8", r([x for x in D if x['first_order_satisfaction_score_10']<8]))
print("cons>30 share", sum(x['estimated_consumption_days']>30 for x in D), "/180")
def p2(k1,n1,k2,n2):
    p=(k1+k2)/(n1+n2); z=(k1/n1-k2/n2)/sqrt(p*(1-p)*(1/n1+1/n2)); return round(z,2), round(2*(1-0.5*(1+erf(abs(z)/sqrt(2)))),4)
print("z,p choose vs not offered", p2(40,49,34,84), " issue", p2(19,52,76,128), " timing±10", p2(47,73,48,107), " timing±7 aligned vs mismatched", p2(31,52,64,128))
