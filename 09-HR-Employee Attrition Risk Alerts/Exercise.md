# Question 03: Early warning of staff separation risks

# Background

A firm HR regularly follows staff stability, but is currently largely dependent on the experience of the manager of the operation, who is not easily able to identify people who need care or communication in a timely manner. The enterprise provided performance for 72 employees, leave, late arrival, salary adjustments, change of management and professionalism data, and there were stable samples of the data, individual anomalies, compound anomalies and missing key fields.

You are a member of the HR Data Analysis Project, which needs to build an early warning intelligence body on the risks of separation, translate clear rules into a reviewable risk signal, help HR arrange manual communication... The result is not a factual determination that an employee will leave, nor can it be the sole basis for dismissal, salary reductions or other adverse decisions.

# Provide material

- `Adviser data.csv ': Basemarks for 72 employees, department and related indicators for one year...
- `Staff-out risk indicator.txt ': definition of indicators, scoring method, hierarchy rules and requirements for the treatment of missing values...

# Business tasks to be accomplished

1. Six risk indicators and total risk score for all 72 staff, each of which should show whether the hit or the corresponding raw data were available.
2. Strictly rule staff are classified as high risk, medium risk, low risk or manual review, and no subjective impression replaces the rule.
3. Output of detailed employee results, including at least: employee ID, department, indicators results, total score, risk level, evidence-based statement and recommended HR action.
4. Generate a summary of the sectoral dimensions showing the number of people at each risk level, the proportion and the persons to be reviewed manually, and generate a tiered follow-up plan.

# Unusual and border

- Performance, monthly leave or absence of any key field with a professional commitment, must be marked with manual review and must not be directly rated as a high risk.
- Provide enforceable monitoring indicators and review cycles for medium-risk staff; generate only communication and care recommendations for high-risk staff
- Avoid "necessarily" in output, "low loyalty" and other labels that cannot be confirmed by data.
- Support recalculations after adjusting risk thresholds or replacing data and demonstrate the record of changes in risk levels...

# Delivery requirements

On-site demonstrations of individual indicator calculations, batch rankings, missing data disposal, departmental aggregations and HR follow-up recommendations... The way to achieve this is designed by the players themselves.
