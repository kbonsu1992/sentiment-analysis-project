import argparse
import csv
import json
import os

from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_review_sentiment(review_text: str) -> dict:
    """Return sentiment for one review as JSON-like dict."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a sentiment analysis assistant. "
                    "Classify the sentiment as Positive, Neutral, or Negative."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Analyze this product review and return a JSON object with keys: "
                    "sentiment, confidence (0 to 1), and reason (max 20 words).\n\n"
                    f"Review: {review_text}"
                ),
            },
        ],
    )
    return json.loads(response.choices[0].message.content)


def analyze_reviews_csv(
    input_csv_path: str, output_csv_path: str, review_column: str = "review"
) -> None:
    """Read reviews from CSV, analyze sentiment, and write to new CSV."""
    with open(input_csv_path, mode="r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header row.")
        if review_column not in reader.fieldnames:
            raise ValueError(
                f"Missing column '{review_column}'. Available columns: {reader.fieldnames}"
            )

        output_columns = reader.fieldnames + ["sentiment", "confidence", "reason"]

        with open(output_csv_path, mode="w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=output_columns)
            writer.writeheader()

            for row_number, row in enumerate(reader, start=1):
                review_text = (row.get(review_column) or "").strip()
                if not review_text:
                    row["sentiment"] = "N/A"
                    row["confidence"] = "0"
                    row["reason"] = "Empty review text."
                else:
                    result = analyze_review_sentiment(review_text)
                    row["sentiment"] = result.get("sentiment", "Unknown")
                    row["confidence"] = result.get("confidence", 0)
                    row["reason"] = result.get("reason", "No reason provided.")

                writer.writerow(row)
                print(f"Processed row {row_number}")


if __name__ == "__main__":
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

    if not os.path.exists(args.input):
        raise FileNotFoundError(
            f"Input file '{args.input}' not found. Create it with a '{args.review_column}' column."
        )

    analyze_reviews_csv(args.input, args.output, args.review_column)
    print(f"Done. Results written to: {args.output}")