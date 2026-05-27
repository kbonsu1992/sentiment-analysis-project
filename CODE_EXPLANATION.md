# Complete Code Explanation

This document explains the entire project and how each part works.

## Project Files

- `prompt_ex.py` - main Python application.
- `reviews.csv` - sample input data (reviews to analyze).
- `README.md` - setup and quick usage guide.
- `CODE_EXPLANATION.md` - this deeper technical explanation.

## Goal of the Project

The project performs sentiment analysis on customer/product reviews using the OpenAI API.

For each review, the script produces:
- `sentiment` (`Positive`, `Neutral`, or `Negative`)
- `confidence` (numeric score between 0 and 1)
- `reason` (short explanation)

## High-Level Execution Flow

1. Load API key from environment variable `OPENAI_API_KEY`.
2. Parse command-line arguments (`--input`, `--output`, `--review-column`).
3. Validate that the input CSV exists.
4. Read reviews from input CSV.
5. Send each review to the OpenAI model for classification.
6. Parse model JSON response into Python dictionary.
7. Write all original row data plus sentiment fields to a new CSV.
8. Print progress in terminal.

## `prompt_ex.py` Detailed Breakdown

## 1) Imports

- `argparse` - handles command-line options.
- `csv` - reads and writes CSV files.
- `json` - parses JSON returned by the model.
- `os` - checks file existence and reads environment variables.
- `OpenAI` from `openai` - API client.

## 2) OpenAI Client Initialization

The client is created with:
- `api_key=os.getenv("OPENAI_API_KEY")`

This means the script expects your key to be set in your shell environment before running.

## 3) Function: `analyze_review_sentiment(review_text: str) -> dict`

Purpose:
- Send one review to the OpenAI model and return structured sentiment output.

What it does:
- Calls `client.chat.completions.create(...)`.
- Uses model `gpt-4o-mini`.
- Sets `temperature=0` for consistency.
- Sets `response_format={"type": "json_object"}` to request strict JSON.
- Uses:
  - System message: defines the assistant role and allowed sentiment classes.
  - User message: asks for keys `sentiment`, `confidence`, and `reason`.
- Parses returned JSON text with `json.loads(...)`.
- Returns a Python `dict`.

Expected returned dictionary shape:

```python
{
    "sentiment": "Positive",
    "confidence": 0.94,
    "reason": "Strong positive language about quality and reliability."
}
```

## 4) Function: `analyze_reviews_csv(input_csv_path, output_csv_path, review_column="review")`

Purpose:
- Process an entire CSV file row-by-row and save enriched results.

Step-by-step behavior:
- Opens input file with UTF-8 encoding.
- Reads rows using `csv.DictReader` (so each row is a dict keyed by column name).
- Validates:
  - The CSV has a header row.
  - The selected review column exists.
- Builds output columns as:
  - All original columns
  - `sentiment`, `confidence`, `reason`
- Opens output CSV with `csv.DictWriter`.
- Iterates every input row:
  - Gets review text from the configured review column.
  - If review is empty:
    - Writes defaults (`N/A`, `0`, `Empty review text.`)
  - Else:
    - Calls `analyze_review_sentiment(...)`
    - Writes returned values into the row
- Writes each row to output file.
- Prints `Processed row X` progress.

## 5) Main Entry Block: `if __name__ == "__main__":`

Purpose:
- Make the file executable from command line with flexible options.

Arguments:
- `--input` (default `reviews.csv`)
- `--output` (default `sentiment_results.csv`)
- `--review-column` (default `review`)

Validations:
- Checks if input file exists.
- Raises a clear `FileNotFoundError` if not found.

Final action:
- Calls `analyze_reviews_csv(...)` with parsed arguments.
- Prints final output file path.

## Input and Output Contracts

## Input CSV Requirements

- Must have a header row.
- Must contain a text column for reviews (default column name: `review`).

Example:

```csv
id,review
1,The battery lasts all day.
2,It is okay but expensive.
3,Very poor quality.
```

## Output CSV Shape

Output includes all original columns plus:
- `sentiment`
- `confidence`
- `reason`

Example:

```csv
id,review,sentiment,confidence,reason
1,The battery lasts all day.,Positive,0.95,Clear praise of battery performance.
```

## Error Handling in the Script

- Missing input file -> raises `FileNotFoundError`.
- Missing CSV header -> raises `ValueError`.
- Missing review column -> raises `ValueError` with available columns.
- Empty review cell -> writes safe default values instead of failing.

## Why This Design Works Well

- Simple and readable structure.
- Strongly typed row handling using CSV dictionaries.
- Deterministic-ish output via `temperature=0`.
- Structured model response through JSON mode.
- Easy to automate in data pipelines (CSV in, CSV out).

## Common Customizations

- Change model: edit `model="gpt-4o-mini"` in `analyze_review_sentiment`.
- Add more output fields (e.g., emotion, topic): update prompt and writer columns.
- Batch large files: split CSV or add retry/rate-limit handling if needed.
- Integrate with Excel workflows: open output CSV directly in spreadsheet tools.
