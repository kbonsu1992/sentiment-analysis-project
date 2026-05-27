import argparse
import csv
import json
import os

from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_review_sentiment(review_text: str) -> dict:
    """Analyze one review and return a dict with sentiment, confidence, and reason."""
    # Keep temperature low so classifications are more consistent run-to-run.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        # Enforce structured output so we can parse reliably with json.loads.
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    # System prompt defines the model's role and allowed labels.
                    "You are a sentiment analysis assistant. "
                    "Classify the sentiment as Positive, Neutral, or Negative."
                ),
            },
            {
                "role": "user",
                "content": (
                    # User prompt specifies exact keys and value constraints.
                    "Analyze this product review and return a JSON object with keys: "
                    "sentiment, confidence (0 to 1), and reason (max 20 words).\n\n"
                    f"Review: {review_text}"
                ),
            },
        ],
    )
    # Parse the assistant JSON string into a Python dict.
    return json.loads(response.choices[0].message.content)


def analyze_reviews_csv(
    input_csv_path: str, output_csv_path: str, review_column: str = "review"
) -> None:
    """Read input CSV rows, enrich each row with sentiment fields, and write output CSV."""
    # Open the source CSV and read rows as dictionaries keyed by column names.
    with open(input_csv_path, mode="r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        # Ensure the file has a header row; DictReader depends on it.
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header row.")
        # Ensure the configured review column exists before processing rows.
        if review_column not in reader.fieldnames:
            raise ValueError(
                f"Missing column '{review_column}'. Available columns: {reader.fieldnames}"
            )

        # Keep all original columns and append new analysis columns.
        output_columns = reader.fieldnames + ["sentiment", "confidence", "reason"]

        # Create the destination CSV and write the header once.
        with open(output_csv_path, mode="w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=output_columns)
            writer.writeheader()

            # Process each row independently so a full dataset can be enriched.
            for row_number, row in enumerate(reader, start=1):
                # Normalize missing/whitespace-only text to an empty string.
                review_text = (row.get(review_column) or "").strip()
                if not review_text:
                    # Graceful fallback for missing/blank review rows.
                    row["sentiment"] = "N/A"
                    row["confidence"] = "0"
                    row["reason"] = "Empty review text."
                else:
                    # Send the review to the model and map returned values into the row.
                    result = analyze_review_sentiment(review_text)
                    # Use safe defaults in case a key is missing in model output.
                    row["sentiment"] = result.get("sentiment", "Unknown")
                    row["confidence"] = result.get("confidence", 0)
                    row["reason"] = result.get("reason", "No reason provided.")

                # Write the enriched row immediately and print progress.
                writer.writerow(row)
                print(f"Processed row {row_number}")


if __name__ == "__main__":
    # Define command-line options so the script can run with defaults or custom paths.
    parser = argparse.ArgumentParser(
        description="Run sentiment analysis on reviews from a CSV file."
    )
    parser.add_argument(
        "--input",
        default="reviews.csv",
        help="Path to input CSV file (default: reviews.csv)",
    )
    parser.add_argument(
        "--output",
        default="sentiment_results.csv",
        help="Path to output CSV file (default: sentiment_results.csv)",
    )
    parser.add_argument(
        "--review-column",
        default="review",
        help="CSV column containing review text (default: review)",
    )
    args = parser.parse_args()

    # Fail fast with a clear message if the input file is missing.
    if not os.path.exists(args.input):
        raise FileNotFoundError(
            f"Input file '{args.input}' not found. Create it with a '{args.review_column}' column."
        )

    # Start processing and report where results were saved.
    analyze_reviews_csv(args.input, args.output, args.review_column)
    print(f"Done. Results written to: {args.output}")