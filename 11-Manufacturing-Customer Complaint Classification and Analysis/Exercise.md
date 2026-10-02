# Test 09: Client complaints intelligence classification and root causes analysis

# Background

A consumer electronic enterprise receives client complaints monthly from multiple sources, such as electric power platforms, hotlines and after-sale worksheets.... The quality team needs to classify complaints in a uniform manner, identify duplication of problems in the same product, prioritize and summarize possible root causes.... The text of the complaint is not consistent and may contain multiple statements of the same symptoms, including situations where automatic responses must be stopped, such as security incidents and personal exposures.

As a member of the Quality Clients and Management Digital Project, a complaint classification and analysis intelligence body is needed to receive the normal complaint title to be processed by the response and responsibility department, while manual border upgrades are implemented for high-risk complaints.

# Provide material

- `Data for complaints. csv ': 50 cross-channel complaints containing duplicate problem sheets, security incidents and personal information records...
- `Classification of complaints.txt ': definition of seven categories of complaints, first response to SLA, volume issues, security upgrades and dissensitisation rules...
- `History Complaints Case Book/ ': 7 disposal cases with case numbers, conditions applicable and conditions of cessation...

# Business tasks to be accomplished

1. All 50 complaints are classified by standard as product quality, logistics breakdown, functional failure, appearance defects, missing accessories, use of consulting or other, and export classification basis, SLA and processing priority.
2. Identification of duplicated submission of the same order, and of the same type, the mass problem signals of symptoms reaching 3 in 7 days. Original complaint ID and conclusive evidence linked to the output.
3. Summary of the statistical and root causes by category and product type....The root causes should distinguish between "existing cases supporting " and "predicts requiring verification" and should not be directly identified as causes of similar phenomena.
4. Generate standardized draft responses to routine complaints of historical cases, case basis and responsibility to be followed by the responsible department
5. Generate quality improvement lists for product managers, containing problem sheets, evidence, impact ranges, recommendations for validation actions and priorities.

# Unusual and border

- In the event of a security incident involving smoke, fire, electrical shock or injury to personnel, mark P0, immediately stop the automatic response and transfer to the quality manager.
- Mark P1 when you hit a mass problem signal and turn manual intervention, not only on individual client issues.
- Complaints contain a full telephone number, ID number or a detailed address, which is not repeated in the output.
- Duplicate complaints of the same order may be consolidated, but the original records may not be deleted or covered...
- Additional new complaints should be recounted and classified, problem groups and underlying assumptions retained.

# Delivery requirements

On site, routine complaints, repeat questions, bulk signals, security incidents and the differential handling of personal information... are to be achieved by the player's own design.
