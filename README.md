# Sentiment Analysis on Reviews (OpenAI)

Analyze review text from a CSV file using OpenAI and write results to a new CSV.

For each review, the script returns:
- `sentiment` (`Positive`, `Neutral`, `Negative`)
- `confidence` (0 to 1)
- `reason` (short explanation)

## Files

- `prompt_ex.py` - main script
- `reviews.csv` - sample input
- `sentiment_results.csv` - generated output
- `README.md` - setup + code explanation

## Requirements

- Python 3.8+
- `openai` package

```bash
pip install openai
```

## Set API Key

PowerShell:
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

Command Prompt:
```cmd
set OPENAI_API_KEY=your_api_key_here
```

## Input CSV Format

The input file must have a header and a review text column (default: `review`).

```csv
id,review
1,The battery life is amazing.
2,It works fine, but nothing special.
3,Terrible build quality.
```

## Run

Default:
```bash
py prompt_ex.py
```

Custom paths/column:
```bash
py prompt_ex.py --input my_reviews.csv --output results.csv --review-column review_text
```

## Code Explanation

### Execution Flow

1. Read `OPENAI_API_KEY`.
2. Parse CLI args (`--input`, `--output`, `--review-column`).
3. Validate input file exists.
4. Read rows from CSV.
5. Send each review to `gpt-4o-mini`.
6. Parse JSON response and write output CSV.

### `prompt_ex.py`

- `analyze_review_sentiment(review_text)`:
  - Calls `client.chat.completions.create(...)`
  - Uses `temperature=0` and JSON response mode
  - Returns parsed dict with `sentiment`, `confidence`, `reason`
- `analyze_reviews_csv(input_csv_path, output_csv_path, review_column="review")`:
  - Reads rows with `csv.DictReader`
  - Validates header + review column
  - Writes original columns plus `sentiment`, `confidence`, `reason`
  - Handles empty reviews with safe defaults (`N/A`, `0`, `Empty review text.`)
- Main block:
  - Configures CLI arguments
  - Validates input path
  - Runs processing and prints output path

### Error Handling

- Missing file -> `FileNotFoundError`
- Missing header -> `ValueError`
- Missing review column -> `ValueError`
- Empty review cell -> handled without crashing

### Customization

- Change model in `analyze_review_sentiment` (`model="gpt-4o-mini"`)
- Add fields by updating the prompt and output columns
- Change input text column with `--review-column`
