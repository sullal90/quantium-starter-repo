import csv
import os
import glob
from collections import defaultdict
from typing import Iterable


def process_and_aggregate_sales(input_files: Iterable[str], output_file: str, filter_product: str = "pink morsel") -> None:
    """Read input CSVs, keep only rows where product matches filter_product,
    compute sales = price * quantity, and aggregate total sales by (date, region).

    The result is written to output_file with header: date,region,sales
    where sales is formatted as a float with 2 decimal places.
    """

    agg = defaultdict(float)  # (date, region) -> total sales
    seen_input_header = False

    for fname in input_files:
        with open(fname, newline='') as in_f:
            reader = csv.DictReader(in_f)
            # skip empty files
            if reader.fieldnames is None:
                continue
            # Basic validation - ensure required columns exist
            required = {"product", "price", "quantity", "date", "region"}
            if not required.issubset(set(map(str.lower, reader.fieldnames))):
                # try normalising header names to lowercase mapping
                # but if still missing, skip file
                raise RuntimeError(f"Input file {fname} is missing required columns; found: {reader.fieldnames}")

            for row in reader:
                # Defensive normalisation: lower-case product field and strip
                product = row.get("product") or row.get("Product") or ""
                if product is None:
                    continue
                if product.strip().lower() != filter_product.lower():
                    continue

                # Parse price like "$3.00" -> 3.00
                price_raw = row.get("price") or row.get("Price") or "0"
                # remove common currency symbols and commas
                price_str = "".join(ch for ch in price_raw if (ch.isdigit() or ch == '.' or ch == '-'))
                try:
                    price = float(price_str) if price_str not in ("", "-") else 0.0
                except ValueError:
                    price = 0.0

                # Parse quantity
                qty_raw = row.get("quantity") or row.get("Quantity") or "0"
                try:
                    quantity = int(qty_raw)
                except (ValueError, TypeError):
                    # fallback: try float -> int
                    try:
                        quantity = int(float(qty_raw))
                    except Exception:
                        quantity = 0

                date = row.get("date") or row.get("Date") or ""
                region = row.get("region") or row.get("Region") or ""

                sales = price * quantity
                agg[(date, region)] += sales

    # Write aggregated results
    with open(output_file, mode='w', newline='') as out_f:
        writer = csv.writer(out_f)
        # User requested column order: Sales, Date, Region
        writer.writerow(["Sales", "Date", "Region"])
        for (date, region), total in sorted(agg.items()):
            # write Sales first, then Date, then Region
            writer.writerow([f"{total:.2f}", date, region])


if __name__ == "__main__":
    data_dir = "data"
    filtered_file_path = os.path.join(data_dir, "filtered_data.csv")
    # Find all .csv files in data_dir (non-recursive), sort for deterministic order
    all_csvs = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    # Exclude the output file if it exists in the same folder
    input_files = [p for p in all_csvs if os.path.abspath(p) != os.path.abspath(filtered_file_path)]
    process_and_aggregate_sales(input_files, filtered_file_path, filter_product="pink morsel")
