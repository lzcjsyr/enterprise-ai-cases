# Business AI landing case: from Excel to business knowledge Library
# -- Enlist enterprise data question and answer system complete link

> Applicable course: 06 Recruit data > Enterprise AI Land
> Case type: real business needs AI landing process
> Difficulty: ★★★☆☆ (regarding data cleansing, connector call, knowledge base operation)

---

# One, business background

The personnel recruited were **7 Excel documents** (2,517 records) recording the names of the enterprises with different caller vehicles (camps/buildings):
Central accelerator, cluster (Gl-I-Fang/Nunbrook Valley), Cloud Creek Valley, Rufon Building, American Industrial Park, South Screen Science Park, Fubrook Industrial Zone.

** Painful**: Data scattered in Excel, looking for "some integrated circuits in a certain area" requires multiple files to be manually opened, eye-to-eye matching, time-consuming and laborious.
**Request**: transform these data into a ** questionable knowledge base** - Ask questions whenever, AI answers.

** Business AI landing nature**: Turn "Leave data in the form" into "Leadable knowledge." Data is not in the system. It's worth zero.

---

# Two, Step 1 sets out clear needs (first of the most critical steps)

> Teaching point: **AI is not everything, the more needs are clear, the better.** This step is to tell AI "What fields I want, why."

The following requests are addressed to AI:

```
I have a list of seven businesses with a commercial vehicle, Excel, not a uniform field.
Objective: To merge into a single Excel, upload it to the corporate knowledge base, support normal questions and answers --
Like, "What businesses in a certain area?" "The list of businesses in a certain industry."

Please give a data cleansing program and ask:
1. Harmonization of field structures (to inform me of the eventual standard fields required)
2. Identification of all discrepancies and problems with dirty data in the 7 existing documents
3. To give the rules for each issue
```

** List of final standard fields (21)** - This is designed for "Questions and Answers":

| Class | Field | Why do you need |
|------|------|-----------|
|E |Empic, Unified Social Credit Code | unique identification, heavy, and check for |
Legal Representative, Lian Xi Ren Ji Shu Ji Hai Ma, obscurant, e-mail, e-mail, e-mail, and call for follow-up
Business and industry, registered business, date of establishment, date of registration, date of registration, date of registration, date of registration, date of registration, date of registration, date of establishment, date of establishment, date of establishment, date of establishment, date of registration, date of registration, date of registration, date of registration, date of registration, date of registration, date of registration, date of registration, date of entry, date of entry, date of entry, date of entry, date of entry, date of entry of the date of entry of the date of entry into the national registry, date of registration, date of entry of the date of entry of the date of entry into force of the date of entry into force of the date of entry into force of the date of entry into force of the Republic of the Republic of Macedonia, date of entry into force of the Republic of Macedonia, date of entry into force of the Republic of the Republic of Macedonia, date of registration of the Republic of Macedonia, date of registration of the Republic of Macedonia, date of entry of the Republic of Macedonia, date of entry of the Republic of the Republic of Macedonia, date of the Republic of the Republic of the Republic of the Republic of Macedonia of the Republic of Macedonia of the
Number of social security workers, national labels, national labels, sub-categories
** By region/carrier **
Other Recent Relocation Time, Business Profile, Validation Notes, Data Sources, Trace and Quality

** Questioning = field design capability.

---

# Three, Step 2|AI data cleansing program

##3.1 Mapping the background: a question count of 7 files

• Type of problem = specific situation = impact =
|---------|---------|------|
| 1 field is not uniform | 11-15 columns vary; | "registered funds" | "vs" registered business" | "industry subcategory" | cannot be directly merged
| 2 missing key fields | 34% missing United Credit Code; 21% missing founding time | cannot uniquely mark/validate |
|, registered tabal has 3 graphs of \300.0 million/50 million won.| Unable to calculate/ sort
| 4 Mixed Format | Number of Social Securitys written in "1 (2024)" (number + year) | Unable to aggregate |
5 repeat data 5 replicas 591 (full overlap) in two files
|6 Structureal anomalies | Fukuo Industrial Area, 2nd row, field is completely different | Special processing |
** 7 lacked dimensions | None of the files have "owned vehicle" and "in-area" fields ** cannot be asked by region/carrier** **

##3.2 Cleaning Scheme (AI give, manual confirmation)

1. **Uniform Schema**: 7 files map to 21 standard fields
2. ** Format standardization**: UTM value, UTM YYY-MM-DD, NNS number extraction, removal of \t '
3. ** Supplementary dimensions**: new "Beacon carriers" (by source document) and "House areas" (from address: Kano district/Gahnosu district/Gin Bay district/Doomen district/hyolin region)
4. ** Heavy**: Heavy by Qi Ye Ming Cheng, first appearance of the reservation
5. **External verification**: access to check and verify business information, complete missing fields

Elementary: Cleanup programs need to be ** diagnosed and then developed**.AI values are not "directly combined" but first to discover problems you can't see.

---

# Four, Step 3 | connection check: Verify + Supplement

> Teaching point:** AI handles data from "you gave" and tries to check for authoritative data from "business register."** The data quality is assured by the intersection of the two.

##4.1 Validation logic (two types of operation)

♪ Operation, scene, methodology, methodology ♪
|------|------|------|
** ** Two-factor validation** | There is a credit code | Checking business register, comparison of name/code/registered capital/found time **
** ** Completion** | Missing credit code/ registered capital/ corporate  ** press Qi Ye Ming Cheng Query, backfilling missing fields |

##4.2 Sample validation results (8 households, 6 carriers covered)

The company's carrier, the carrier, the carrier, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the carrier, the carrier, the carrier, the carrier, the carrier, the carrier, the carrier, the carrier, the carrier, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the agent, the person, the agent, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the person, the
|------|---------|--------------|---------|
** One hand-held digital technology ** cloud valley | two elements verify | code/legal / registered capital ** all agreed**, paid in full 1.49 million |
** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
** ** ** ** ** 🔍 🔍 🔍 credit code; ** place of registration (high-sengland) does not match address (Chanzhou region)** **
| Seymour semiconductor technology | Cheng | | | | ✅ ✅ ✅ ✅ ✅ / credit supplement code / reconciliation of establishment time = | / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / ed ed / ed
| Meta-Innovative Technology | Colony-Ii-Fang, Completion | Compensating Credit Code, verified consistency |
♪ The Chinese hotel management ♪
** Central China's PAUL, South Screen Technology Park, South China,  ** ** original table is not available, complete 52 million ** + time of establishment  **
**  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **  **

#4.3 High point of instruction

- ** Data contradicts**: Wigand education registration is in the High New Territories, the address is in the Shanzhou -- this means that business "register" and "real office" may be different, both of which are reserved for business.
- ** Missing or value**: attempt to complete completely unconnected data sources, completed by external authoritative data**
-** Methodologies can be expanded**: 8 demonstration methodologies in this sample; 1,900+ full volume of batchable check interfaces, with coverage from 66% to 95% +

---

# Five, Step 4 gills to produce a single Excel

## # 5.1 Cleaning-up comparison

♪ The way you're gonna be ♪
|------|--------|--------|
Total number of records 3,517 (including repetition) ** 1,922**
| Duplicate 595 (Yonbrook Valley 591 + Cross Carrier 4) | 0
| Unified Social Credit Code Covers 66% | 66% + Sample Completion |
**  ** 83.5% cannot be answered  ** (Chanzhou = 1,429 / High New Zealand = 115 / Doomong = 25 / Transon = 24 / Bay of King = 11) |
| Portal dimensions | No | 8 carriers fully covered |

##5.2 Delivery file

```
Enterprise knowledge base for commercial firms  summary 1922.xlsx
├── Sheet1  Enterprise summary (1,922 rows x 21 columns, standardized data)
├── Sheet2  Overview of data (statistical indicators)
└── Sheet3  Carrier x-area distribution (cross-view, directly supporting question and answer)
```

# # 5.3 Retrieve the details (teaching)

- The Cloud Creek Valley is fully re-unified in two documents** 591 ** ** Keep the "Close-Rown Creek Valley" and delete the duplicate source
- Cross-carrier repeats only 4 homes (Star 2, Southscreen 1, Fowbrook 1)
- Total number of businesses that have lost weight = 2,517 − 595 = **1,922**

> Stepping Record: The first edition of the first edition is only 21.5% coverage in the area -- because the Python trap of `nan or address ' (nan is real, resulting in no address field being checked). Post-repair jumps to 83.5%.** Technical detail determines data quality.**

---

Six, Step 5 uploads knowledge Library

Three steps for upload (application certificate HTTP PUT confirmation):

♪ Step, step, step, move, result, result ♪
|------|------|------|
|Set 1 Request Upload |Specify the target knowledge base "Industry Recruitment Information", file name, 748,374 bytes |Senture to get presigned URL |
|2 Upload Content |curl-X PUT-data-binary@file  @HTTP 200  @
**3 Confirm completion of session id | file entry creation, state unprocessed  **finished** |

** Knowledge base location**: `Industry Quest ' Knowledge base (along with existing `Integrator   Merger of Enterprises',' Smart Table)

** Document link**: `https://lexiangla.com/pages/{entry id}?company from={company code}

> Teaching point:** "Page up " *" * *.Enjoy needs to be analyzed, Excel, and then back up the question and answer, waiting to become finished.

---

# Seven, Step 6 # Normalization Question and Answer Validation

Upon completion of the processing of the knowledge base, the following questions are directly asked (simulation of the daily recruitment of business personnel):

| Example of question | Wen Da Question logic | Data support |
|---------|---------|---------|
"What are the integrated circuits related businesses in the Shanzhou?"
"What businesses are the cloud valley carriers? "
| "Golden New Zone over 10 million businesses?" = Region = High New Zone + filtered capital > 1000  >
"How many businesses are there?"
"Is this business still in business?"

**Question and answer capacity validation results** (Living search):

♪ Check the lines, check the results, check the results, check the results ♪
|--------|------|
**Processed  **Processing  **
| Title search, | upload, | 10 minutes effective |
| Content-level search (searching business name/industry/carrying) ⏳ 1,922 Line AI alms with larger altimeters, and a step-by-step index sync (old document is in the right place and can return to the "business state/ address/industry/scope" summary) |

The real lesson**: "Playing up "Questions and Answers at once." The first-level analysis of Excel (generated by each firm's file abstract) takes time, the older the document becomes. When officially used: uploading first-class, finished, measured, 2-3 questions confirmed, valid, then open to the team.

---

# Eight, over: What does this case teach you?

## # 8.1 Enterprise AI Minimum closed loop to land

```
Business needs - Clear fields - AI Cleaning Program - External data validation - Single data source - Knowledge base - Normalize questions Answer
   ↑                                                                        ↓
Questions and answers revealed data gaps and a new round of cleansing. ─
```

# # 8.2 Five Key Success Elements

1. ** Translation required**: translation of "Be a knowledge base" into "21 standard fields + which questions to support"
2. ** Cleaning is a prerequisite**: dirty data directly into the knowledge base = the error answer automatically spreads
3. ** Cross-check external data sources**: check blind areas that are not visible to AI or manual
4.** Single data source**: multiple files combined in one, questions and answers are not "version conflicts"
5. ** Validation of closed loops**: several questions must be measured after uploading, confirming that the knowledge base really " understands" data

# # 8.3 Extensionable direction

- ** Full verification**: 1,900+ enterprises to conduct bulk checking, with reference to 95% credit code/area coverage
-** Periodically updated**: data on the solicitation are updated monthly, time-sensitive through automated processes + re-upload
-** Authority and Sharing**: Visibility of knowledge base by sector (Rendering Group/ Park Operating Group)
-** Question and answer upgrade**: from "Research Question and Answer" to "analytical Q and Answer" (e.g., "What carrier has the highest enterprise density of integrated circuits")

---

# Attach: full operating record

♪ The world is so full of shit ♪
|------|--------|------|
` Step 2 Purge Merger ` step1_Purge merge. py` pip wash script/ pip
Step 3 Check to fill in the ` step2_Backfill. py` clean script/ pip
| Step 4 Intermediate result | Intermediate watch after cleaning. csv`(Line 1,922) | Output/ |
|Step 4 Final Delivery |Enterprise Knowledge Bank of Remanders sum 1922.xx`Export/ |
|Step 5 Knowledge Bank | Industrial Recruitment Information (Lexiangla.com |
