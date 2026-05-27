# Sentiment Analysis on Reviews (OpenAI)

This project uses the OpenAI API to analyze product review sentiment from a CSV file.

The script classifies each review as:
- Positive
- Neutral
- Negative

It also returns:
- Confidence score (0 to 1)
- Short reason (up to 20 words)

## Project Structure

- `prompt_ex.py` - reads reviews from CSV, calls OpenAI, writes sentiment results CSV.
- `reviews.csv` - starter input dataset with sample review rows.
- `sentiment_results.csv` - output file generated after running the script.
- `README.md` - quick-start setup and usage guide.
- `CODE_EXPLANATION.md` - complete technical explanation of the codebase.

## Detailed Documentation

For a full breakdown of architecture, function-by-function logic, data flow, and customization options, see:
- `CODE_EXPLANATION.md`

## Requirements

- Python 3.8+
- OpenAI Python SDK

Install dependency:

```bash
pip install openai
```

## Setup API Key

Set your OpenAI API key as an environment variable.

### PowerShell (Windows)

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

### Command Prompt (Windows)

```cmd
set OPENAI_API_KEY=your_api_key_here
```

## CSV Format

Create an input CSV file (default name: `reviews.csv`) with a header row.
By default, the script expects a column named `review`.

Example `reviews.csv`:

```csv
id,review
1,The battery life is amazing and the camera quality is outstanding.
2,It works fine, but nothing really impressed me.
3,Terrible build quality. It stopped working in two days.
```

## Run the Script

### Default paths

This reads `reviews.csv` and writes `sentiment_results.csv`:

```bash
py prompt_ex.py
```

### Custom paths/column

```bash
py prompt_ex.py --input my_reviews.csv --output results.csv --review-column review_text
```

## How It Works

1. The script reads each row from the input CSV.
2. It sends the review text to `gpt-4o-mini`.
3. The model is instructed to return strict JSON:
   - `sentiment`
   - `confidence`
   - `reason`
4. The script writes a new CSV with original columns plus:
   - `sentiment`
   - `confidence`
   - `reason`
