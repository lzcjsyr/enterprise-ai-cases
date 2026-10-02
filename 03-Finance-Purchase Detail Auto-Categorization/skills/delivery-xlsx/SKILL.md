---
name: delivery-xlsx
DESCR: Classify the commodity items for procurement, sales, inventory or cost and output the classified tables. This Skyll. Input may be... xls,.xlsm,.csv or.tsv. It cannot be assumed that file names, worksheet names, headlines or field positions are fixed, as long as the user refers to local schedule, commodity classifications, subject-setting, procurement analysis or Excel/CSV data collation.
Compatibility: Python environments need to be able to read local tables; priority is given to openpyxl reading/ writing.xlsx/.xlsm,xlrd reading.xls, standard library reading.csv/.tsv.
---

# Discretion into detail and automatic

# Target and border

A breakdown of possible structural changes is organized into a delivery:

1. Classified breakdown: retain original breakdown and add "curricular code" and "subject name".

The classification criterion is the fixed operating rule for this Skyll, as detailed in `references/classification rules.md '. The code, subject name or subject boundary cannot be modified because the input file changes name, sequence or new commodity. If input is clearly not part of the standard, it should be stated that it is not applicable and that no additional subject is added without permission. The aggregation and chart analysis are a follow-up process and are presented separately by the user at the next stage.

# The most important principles of work #

## # AI understands, the program is implemented

AI first reads sample files, understands table structure and business semantics, then hands over clear structure information to the universal reading and writing logic. Read and write logic is responsible only for: reading assigned worksheets and areas, writing back and output files by map, not speculating on business implications.

Do not create scripts for a file name, for a column letter or for a fixed headline. Any secondary program that can be used must receive the following information by parameters or structured configuration:

- Enter file path and file type
- Sheet name or data page
- The header line, the data start line
- Trade name column, monetary column, date column, word-sampling column
- New insertion position
- AI generated commodity classification maps

This will change the file to.xlsx ', change the sheet name, add a few lines of description before the header, or change the trade name to "good name/good name" without any rewriting of the script.

# It's not a hypothetical file name and column number

Each case must be confirmed:

- Input file actually used, not default search for a fixed file Synchronising folder
- Sheet where the valid data is, not the default first table
- Headline and data start line
- trade name fields, and optional fields such as amounts, dates, quantities, etc.
- Whether there are aggregate rows, empty rows, indicating rows, repeat headers or multiple data areas

Field names may vary.... The first rows of samples, data types and the adjacent column are judged. For example, the name "trade name" "good name" "good name" "good name" "material name" may point to a trade name field, but cannot be determined directly by a string match.

# Standard workflow

Step 1: Find and check input

List the candidate files in the user-assigned directory, confirm the extension, file size and change time... only processes the user-assigned or clearly related files, without covering the original files.

Select common reading method by format:

- `.xls ': read with `xlrd '
- `.xlsx ', `.xlsm ': Use `openpyxl '; if you want to keep a macro, specify the output limit
- `.csv ', `.tsv ': Read tools using standard libraries or tables of equal value and detect coding, separator and quotation marks

Read the sheet list, the row range and a small sample sample, and then decide the target data area. Do not write "line 2" column 5 into the fixed code for the sake of a suitable example.

Step 2: Create a structure description

Before formal classification, a provisional structure statement or memory map is developed, including at least:

```json
{
"input file": "Pilot path"
"Sheet": "Practical Data Page",
  "header_row": 0,
  "data_start_row": 1,
  "columns": {
    "item_name": 4,
    "amount": 8,
    "date": 1,
    "quantity": 6,
    "unit": 7
  },
  "insert_after": 8,
"notes": [" Skip title lines, empty lines and aggregate lines"]
}
```

The figures here are the result of the identification of the current document, not the dead rule. The delivery statement is intended to inform the user of what is actually identified; If two possible trade names columns exist, first Based on the sample, it is still impossible to judge and indicate if it is suspended.

##3 Step: Semantic classification by fixed standard

After reading `references/classification rules.md ', semantics of trade names:

1. To retain the original trade name and then to standardize it lightly, for example by removing the first-end spaces, changing lines, repeating spaces and visible format noises.
2. Classification of the only trade names after standardization, and mapping of the results back to all line items, avoiding the same commodity receiving different subjects in different lines.
3. Depending on the essential uses and categories of the commodity, reliance is not limited to a keyword; branding, origin, specification, packaging and processing are usually acquis.
4. Each trade name detail must be given a code and name in one of the seven subjects in existence.
5. The most immediate subject is still selected for undetermined commodities, with separate records of "person-reviewed" commodities, subject and basis of judgement... not to be written into new subjects.

If a " sorted" classification or other reference result with a clear subject code/subject name is available in the directory, it should be used as a sample for the current business:

- For the same trade names, if standardized in the same or light quantities, priority is given to the classification in the reference results, ensuring consistency in the same business calibre...
- Reference results can only help to resolve specific boundaries of existing commodities, not be used to add, change name, merge or divide seven fixed subjects.
- The semantics of the standard classification rule are used for new commodities that are not present in the reference results.
- If reference results appear to conflict with fixed rules, do not quietly change one of them; retain fixed lines and include conflict in the review list...

This step is particularly important: the classification script cannot replace AI's commodity understanding with rough keywords or self-suspecting inspirational rules, nor can it ignore the misallocation of goods between different subjects because the total amount is right.

It is proposed that the following classification maps be retained internally to facilitate reconciliation:

```json
{
Standardised trade name: {1 %1 %2 %2 %2 %2 %2 %2 %2 %1 %2 %2 %1 %1 %2 %2 %1 %1 %2 %1 %1 %1 %2 %1 %1 %2 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 %1 % %1 %1 %1 %1 %1 %1 %1 %1 %1 % %1 %
    "code": "1403.01.01",
"subject": "cooked food",
    "confidence": "high",
    "review": false,
"Reason: "Commodity is essentially meat."
  }
}
```

Step 4: Write back the details after validation

Check before writing back, not just check if the file is saved successfully:

- Whether all line items with trade names are given the subject code and the subject name
- Original line details, date, trade name and amount consistent with input
- Whether the amount column identified is sumable; whether the amount is text, empty or abnormally negative
- Whether the sum of the amounts for the individual categories after classification is equal to the original amount of the breakdown, and the difference must be explained
- If the catalogue contains reference classification results, the number of subject categories currently classified, whether the sum summary and the key commodity mapping are consistent with the reference calibre; if discrepancies occur, the commodity mapping is reviewed and delivered
- Total rows, empty rows and description lines that are misapplied as commodity details
- Whether there is a duplicate header, a duplicate trade name or an unrecognized unusual record

On output:

- Do not overwrite original files; give priority to generating new.rsx ' in the same directory
- Save original data order and main cell values
- Add "Focal Code" column, "Study Name", and insert position selected according to the current table structure, not fixed to a column number
- Leave non-data lines blank or as they are, without sub-values being added to the headings and totals Okay.
- Keep the date of the original table, numbers and basic formats as far as possible; if `.xls ' is converted to `.xlsx ' makes part of the format unreserved, state in the note

Output file name is generated by the input file name, e.g.:

- Schedule: `{Input filename} Classed.xx '

Do not write "April" or other example names in a fixed script. If the target file already exists, create a new file without overwhelming the original result, or explain it to the user first.

# Pre-delivery check

Check at least:

1. The breakdown of the list is real and the file name is dynamically generated by the input file.
2. Lines with trade names are given subject codes and subject names.
3. Randomly sample the commodities, classification codes and names of different subjects.
4. The review list contains all the uncertainties; no additional subjects have been introduced secretly to make coverage appear complete.
5. No original files were overwritten, no path, column numbers or illustrative amounts were coded into the common process.

# Run Environment Tips

`.xls ' was first processed to confirm that `xlrd ' was installed; `.xlsx ' was treated to `.xlsm ', `.xlsm ' to confirm that `openpyxl ' is available... relying on installation can only solve problems of access to file formats and cannot replace AI's judgement of the semantics of table structure and classification.

Known pits:

- The `logfile ' parameter of `xlrd.open workbook ' binds the then `sys.stdout ' in the definition of function, and therefore temporarily redirects `sys.stdout ' cannot be stopped OLE2  Inconsistency ', a whistle-blower will blend into stdout to fail JSON ' s analysis.
- Scripts give 'sugglestions ' just a hint. The column with the "name" may be "unit name" "client name" and not a trade name; it must be confirmed in combination with sample lines and not directly accepted.
- `.xls ', after `openpyxl ' output is `.xx ', the number of floating points in the whole number (e.g. `5.0 ' ) will be fixed by `5 ' reading back... values per se, which should be compared by value, not by string, otherwise the content will be miscalculated as inconsistent.
