FreshNest's 60-day repurchase problem shows up in **85 of 180 customers (47%)**, who didn't buy again within 60 days; 95 did. Three things are linked to it, and all three can be fixed: reorder timing that doesn't match how fast customers use the product, packaging problems, and the kind of subscription offer shown. Discounts and delivery speed show no link.

## The three most important findings

**1. The reorder recommendation is wrongly timed for most customers, and those customers come back much less**
- The system only ever recommends 30, 45 or 60 days, but estimated consumption ranges from 12 to 83 days. For **107 of 180 customers (59%)**, the recommendation is more than 10 days away from their estimated consumption.
- **Repurchase rates:** 64% (47/73) when the timing is within 10 days, against 45% (48/107) when it isn't. Being off in either direction hurts: too early 40% (20/50), too late 49% (28/57).
- **Who it hits hardest:** customers who couldn't set their own cadence (fixed 30-day offer or no offer). They repurchased at 59% (36/61) when timing matched and 27% (19/70) when it didn't.
- **Easy fix:** if the system simply picked whichever of 30, 45 or 60 is closest to each customer's consumption, about 87% of customers (157/180) would be within 10 days. Today it's 41%.

**2. Packaging problems cut the repurchase rate by more than a third**
- 52 customers (29%) had a recorded packaging issue. They repurchased at **37% (19/52)**, against **59% (76/128)** for customers with no issue.
- **By type:** damaged outer pack 32% (7/22), minor leak 39% (7/18), wrong pack size 42% (5/12).
- **Without a choose-cadence offer:** 21% (8/38) with an issue against 51% (47/93) without. Customers with both an issue and a wrongly timed reorder repurchased at 15% (4/26).

**3. The "choose cadence" offer is the strongest positive signal; the fixed 30-day offer barely beats no offer**
- **Repurchase by offer:** choose cadence **82% (40/49)**, fixed 30-day **45% (21/47)**, no offer **40% (34/84)**.
- **It holds in every channel:** website 80% (16/20), marketplace 69% (11/16), social commerce 100% (13/13).
- **It seems to cushion the other two problems:** these customers repurchased at 78% (29/37) even when timing was wrong, and 79% (11/14) even with a packaging issue. They were also *more* likely to have wrong timing (76% against 53% for everyone else), so that isn't what's flattering their numbers.

**What doesn't explain it.** This matters because these are the obvious things to reach for.
- **Discount:** customers who got 30–40% off their first order repurchased at 51% (34/67), against 54% (61/113) for 0–20%. Bigger discounts don't lead to more repurchase. This supports the rule against a blanket 30% discount.
- **Delivery delay:** 0–2 days 57%, 3–4 days 47%, 5 or more days 54%. There's no consistent pattern.
- **Channel:** marketplace 47% (36/76), against website 56% and social commerce 58%. The gap is small and could be chance.
- **Satisfaction:** customers scoring 8 or higher repurchased at 66%, against 43% for lower scores. But 25 of the 74 highly satisfied customers still didn't come back, which fits a timing problem better than a product-quality problem.

## Main limitations of the data
1. **Small, synthetic and observational.** There are only 180 rows, and many subgroups have 12–50 customers, so their rates could be off by 10–15 percentage points. A simple statistical test says the three main gaps are unlikely to be chance (p < 0.01), but the discount, delay and channel gaps could be. None of this proves cause and effect.
2. **We don't know how offers were assigned.** If choose cadence went to more engaged customers, finding 3 overstates its effect. There is some imbalance: 19 of the 40 surface-cleaner customers got it, against 30 of the 140 others.
3. **"Offer shown" isn't "subscribed."** The data has no field for whether customers took up the offer. It also doesn't say whether a subscription delivery counts as a second purchase. If it does, part of the choose-cadence effect is automatic rather than earned.
4. **The 60-day window is too blunt.** 30 customers have estimated consumption above 60 days. 17 of them are among the 85 who didn't repurchase, so about 1 in 5 of those may simply not have run out yet.
5. **We don't know how consumption was estimated.** If the estimates are poor, some of the timing gap in finding 1 is measurement error.
6. **Packaging issues are "recorded," not verified.** They are probably under-reported, and we don't know whether any recovery was offered.
7. **There are no economics.** Order value, margin, incentive cost and volumes aren't in the data, so break-even can't be calculated from what you pasted.
8. **Other gaps.** It's unclear whether a second purchase made in a different channel is counted. The interviews only point in a direction; they don't show how common each problem is.

## What FreshNest should do
**Recommendation:** run a randomised pilot, not a full rollout.

| Arm | What customers get | Incentive cost |
|---|---|---|
| A: Control | The current experience | None |
| B: Right-time cadence | A choose-cadence subscription offer that allows pausing, skipping and changing cadence, as the constraints require. It replaces the fixed 30-day offer. The default cadence and reminders are set from estimated consumption, starting with whichever of 30, 45 or 60 is closest. | About INR 0 |
| C: B plus issue recovery | Arm B, plus a proactive replacement or credit when a packaging issue is verified | Up to INR 65 per verified case. At about 29% of customers having an issue, that's roughly INR 19 per treated customer. |

- **Who's included:** all new first-order customers in channels where FreshNest controls contact after the purchase. Include marketplace only if the platform allows the offer. Split results by channel, and test clearer "buy direct from FreshNest" wording on marketplace, since interviews say some marketplace customers don't recognise the offer.
- **Size and spend:** about 400 customers per arm can detect a 10-point lift from the roughly 53% baseline. To measure the recovery effect on customers who had an issue, you need about 600 per arm. Incentive spend would be roughly INR 7,500–11,000, all in Arm C. INR 11 lakh is therefore not the limit; most of it would go on building the cadence logic and issue verification. Confirm with Finance whether the INR 65 cap is an average across all treated customers or per customer who receives something.
- **Success and break-even:**
  - **Primary measure:** second purchase within 60 days, and also within estimated consumption plus 15 days.
  - **Guardrails:** contribution margin per customer, incentive spend per extra second order, and pause or cancel rates.
  - **Arm B** has almost no incentive cost, so it's the low-risk bet.
  - **Arm C** must beat B by at least (average incentive per treated customer ÷ contribution margin per second order). Finance's margin figure decides how generous recovery can be.

**Alternatives I'd reject:**

| Option | Evidence it helps | Margin and discount leakage | Operations | Sustainability |
|---|---|---|---|---|
| **Recommended pilot (above)** | Strongest: 82% against 40–45%, and 64% against 45% when timing matches | Low: no discount | Within the stated constraints | Fewer refills arriving before the last pack is used |
| Discount on the second order | None: deeper discounts show no lift | High leakage | Easy | Neutral |
| Push the fixed 30-day offer harder | Weak: 45% against 40% | Low | Breaks the pause/cadence rule | Over-ships for the 78% of customers whose consumption is over 30 days |

**Later-stage options, outside this pilot:** packaging redesign, and a reorder system that recommends exact days instead of only 30, 45 or 60.

**Fix the data now:** record offer uptake, when reminders are sent, verified packaging issues, and repurchases in any channel. Add a repurchase measure adjusted for each customer's consumption, so the next analysis can establish cause rather than just patterns.
