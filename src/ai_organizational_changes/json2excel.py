"""Convert JSON files to Excel format.

This module provides functionality to convert JSON files with nested structures
to Excel spreadsheets with a flattened tabular format.
"""

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


def flatten_json_results(json_data: dict[str, Any]) -> pd.DataFrame:
    """Flatten nested JSON structure into a DataFrame.

    Args:
        json_data: Dictionary containing JSON data with 'model', 'has_probs',
                   and 'results' keys.

    Returns:
        DataFrame with flattened data where each result entry is a row.
    """
    rows = []

    model = json_data.get("model")
    has_probs = json_data.get("has_probs")
    results = json_data.get("results", [])

    # Flatten the nested results array
    for result_group in results:
        for result in result_group:
            row = {
                "model": model,
                "has_probs": has_probs,
                "prompt": result.get("prompt"),
                "malicious": result.get("malicious"),
                "prob": result.get("prob"),
                "content": result.get("content"),
            }
            rows.append(row)

    return pd.DataFrame(rows)


def convert_json_to_excel(
    json_path: Path,
    output_path: Path | None = None,
) -> Path:
    """Convert a single JSON file to Excel format.

    Args:
        json_path: Path to the input JSON file.
        output_path: Optional path for output Excel file. If None, generates
                     name based on input file.

    Returns:
        Path to the created Excel file.
    """
    # Read JSON file
    with open(json_path, encoding="utf-8") as f:
        json_data = json.load(f)

    # Flatten data
    df = flatten_json_results(json_data)

    # Determine output path
    if output_path is None:
        output_path = json_path.with_suffix(".xlsx")

    # Write to Excel
    df.to_excel(output_path, index=False, engine="openpyxl")

    return output_path


def convert_directory_to_excel(
    directory: Path,
    output_dir: Path | None = None,
    pattern: str = "*.json",
) -> list[Path]:
    """Convert all JSON files in a directory to Excel format.

    Args:
        directory: Path to directory containing JSON files.
        output_dir: Optional output directory. If None, uses same directory as input.
        pattern: Glob pattern for matching JSON files (default: "*.json").

    Returns:
        List of paths to created Excel files.
    """
    if output_dir is None:
        output_dir = directory

    output_dir.mkdir(parents=True, exist_ok=True)

    output_files = []

    for json_file in directory.glob(pattern):
        if json_file.is_file():
            output_path = output_dir / json_file.with_suffix(".xlsx").name
            created_file = convert_json_to_excel(json_file, output_path)
            output_files.append(created_file)
            print(f"Converted: {json_file.name} -> {created_file.name}")

    return output_files


def main():
    """Command-line interface for JSON to Excel conversion."""
    parser = argparse.ArgumentParser(description="Convert JSON files to Excel format")
    parser.add_argument(
        "input",
        type=Path,
        help="Path to JSON file or directory containing JSON files",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output path (file or directory)",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        default="*.json",
        help="Glob pattern for matching files (default: *.json)",
    )

    args = parser.parse_args()

    input_path = args.input

    if not input_path.exists():
        print(f"Error: {input_path} does not exist")
        return

    if input_path.is_file():
        # Convert single file
        output_file = convert_json_to_excel(input_path, args.output)
        print(f"Successfully converted to: {output_file}")
    elif input_path.is_dir():
        # Convert directory
        output_files = convert_directory_to_excel(
            input_path,
            args.output,
            args.pattern,
        )
        print(f"\nSuccessfully converted {len(output_files)} file(s)")
    else:
        print(f"Error: {input_path} is neither a file nor directory")


if __name__ == "__main__":
    main()
