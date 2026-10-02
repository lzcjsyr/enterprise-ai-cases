# Question 07: Vendor assessment and risk screening

# Background

A manufacturing enterprise needs to select a qualified supplier for the same type of material.... The procurement price is only part of the decision-making process. The enterprise needs to consider the delivery punctuality rate, quality pass rate, qualification effectiveness and business justice risk in a comprehensive manner.... The different information is scattered across multiple data, including the lack of historical performance data for new suppliers, expired certificates, abnormally low prices, significant quality accidents and high judicial risk.

You are a member of the Supply Chain Access Assessment project and need to build a comprehensive assessment intelligence body linking multiple source data to the same supplier, giving a reviewable rating, red line risk and access advice.

# Provide material

- `Supplier ' Quotation forms.csv ': 12 vendors ' tax-inclusive offers, dues and accounts.
- `Supplier history'. csv ': historical order volume, punctuality rate, quality pass rate, return rate and major accidents...
- `Supplier qualification list.csv ': Type of certificate, validity period and verification status...
- `Property business information.csv ': Founded criminal and judicial risk snapshots.
- `Supplier scoring rules.txt ': 5D scoring, classification thresholds and red line rules...

# Business tasks to be accomplished

1. A complete assessment of 12 suppliers by stabilizing the entire data with the `supplier id ' key.
2. The five dimensions of competitive offers, delivery, quality, qualifications and business risk, and total scores, are calculated strictly in accordance with the rules, showing the basis for the calculation...
3. Inspection of expired qualifications, major quality incidents, high performance of red line conditions... The supplier may not automatically recommend only the total points after hitting the red line, even if the total score is higher...
4. Disaggregating suppliers into "recommended", "considerable", "no recommendations" or "manual review", scoring home-to-house, key advantages, main risks, sources of evidence and access recommendations.
5. Generate a horizontal supplier assessment matrix and provide a checklist of best practices and manual clearance for vendors requiring additional surveys.

# Unusual and border

- No historical data should use the points of the new supplier specified in the rules and mark to be adjusted to the extent that it is not deduced from its performance...
- An offer that is clearly below the median price should be marked as an abnormally low review and should not be considered a direct finding of advantage.
- In the event of the absence or conflict of multiple tables, the specific tables, fields and conflict values should be indicated and the favourable data should not be subjectively selected...
- Supports the re-evaluation of the weights of the various dimensions by the procurement manager and the retention of the version of the weights, the total points and changes in rankings. The red line rules should not be covered by the weights adjustment...

# Delivery requirements

The field needs to demonstrate multi-table linkages, integrated scores, red line interception, unhistorical data processing and weight change comparisons.
