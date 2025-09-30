#!/usr/bin/env python3
"""
JSON to Excel Converter
A flexible utility script to convert JSON files to Excel format with advanced formatting options.
"""

import json
import pandas as pd
import argparse
import os
import sys
from pathlib import Path
from typing import Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class JSONToExcelConverter:
    """A class to handle JSON to Excel conversion with various formatting options."""

    def __init__(self, input_file: str, output_file: str | None = None):
        """
        Initialize the converter.

        Args:
            input_file: Path to the input JSON file
            output_file: Path to the output Excel file (optional, will auto-generate if not provided)
        """
        self.input_file = input_file
        self.output_file = output_file or self._generate_output_filename()

    def _generate_output_filename(self) -> str:
        """Generate output filename based on input filename."""
        input_path = Path(self.input_file)
        return str(input_path.with_suffix(".xlsx"))

    def load_json_data(self) -> Any:
        """Load and parse JSON data from file."""
        try:
            with open(self.input_file, encoding="utf-8") as file:
                data = json.load(file)
                logger.info(f"Successfully loaded JSON data from {self.input_file}")
                return data
        except FileNotFoundError:
            logger.error(f"File not found: {self.input_file}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading JSON file: {e}")
            raise

    def normalize_data(self, data: Any) -> pd.DataFrame:
        """
        Convert JSON data to a normalized pandas DataFrame.

        Args:
            data: The JSON data (list, dict, or other structure)

        Returns:
            pd.DataFrame: Normalized dataframe
        """
        if isinstance(data, list):
            # Handle list of dictionaries (like your job analysis data)
            df = pd.json_normalize(data)

            # Handle array fields by converting them to string representations
            for column in df.columns:
                if df[column].dtype == "object":
                    # Check if any cell contains a list
                    sample_value = (
                        df[column].dropna().iloc[0]
                        if not df[column].dropna().empty
                        else None
                    )
                    if isinstance(sample_value, list):
                        # Join list items with semicolons for readability
                        df[column] = df[column].apply(
                            lambda x: "; ".join(x) if isinstance(x, list) and x else ""
                        )

        elif isinstance(data, dict):
            # Handle single dictionary or nested structure
            df = pd.json_normalize(data)
        else:
            # Handle other data types by creating a simple dataframe
            df = pd.DataFrame([{"value": data}])

        logger.info(f"Normalized data into DataFrame with shape: {df.shape}")
        return df

    def create_multiple_sheets(
        self, data: list[dict], excel_writer: pd.ExcelWriter
    ) -> None:
        """
        Create multiple sheets when dealing with complex nested data.

        Args:
            data: List of dictionaries containing the JSON data
            excel_writer: Excel writer object
        """
        # Main sheet with overview data
        main_df = self.normalize_data(data)
        main_df.to_excel(excel_writer, sheet_name="Overview", index=False)

        # Check if we have skills data to create a separate sheet
        if "skills_replaced" in main_df.columns:
            skills_data = []
            for i, record in enumerate(data):
                if "skills_replaced" in record and record["skills_replaced"]:
                    job_title = record.get("job_title", f"Job_{i}")
                    for skill in record["skills_replaced"]:
                        skills_data.append(
                            {
                                "job_title": job_title,
                                "skill": skill,
                                "likely_replaced": record.get(
                                    "likely_replaced_by_ai", False
                                ),
                            }
                        )

            if skills_data:
                skills_df = pd.DataFrame(skills_data)
                skills_df.to_excel(
                    excel_writer, sheet_name="Skills_Details", index=False
                )
                logger.info(
                    f"Created Skills_Details sheet with {len(skills_data)} entries"
                )

    def apply_formatting(
        self, excel_writer: pd.ExcelWriter, df: pd.DataFrame, sheet_name: str = "Sheet1"
    ) -> None:
        """
        Apply formatting to the Excel sheet.

        Args:
            excel_writer: Excel writer object
            df: DataFrame containing the data
            sheet_name: Name of the sheet to format
        """
        try:
            # Get the workbook and worksheet objects
            workbook = excel_writer.book
            worksheet = excel_writer.sheets[sheet_name]

            # Define formats
            header_format = workbook.add_format(
                {
                    "bold": True,
                    "bg_color": "#4F81BD",
                    "font_color": "white",
                    "border": 1,
                    "text_wrap": True,
                    "valign": "vcenter",
                }
            )

            cell_format = workbook.add_format(
                {"border": 1, "text_wrap": True, "valign": "top"}
            )

            boolean_format = workbook.add_format(
                {"border": 1, "align": "center", "valign": "vcenter"}
            )

            # Apply header formatting
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # Apply cell formatting
            for row in range(1, len(df) + 1):
                for col in range(len(df.columns)):
                    cell_value = df.iloc[row - 1, col]
                    if isinstance(cell_value, bool):
                        worksheet.write(row, col, cell_value, boolean_format)
                    else:
                        worksheet.write(row, col, cell_value, cell_format)

            # Auto-adjust column widths
            for i, column in enumerate(df.columns):
                max_length = max(df[column].astype(str).apply(len).max(), len(column))
                # Cap the width to prevent extremely wide columns
                adjusted_width = min(max_length + 2, 50)
                worksheet.set_column(i, i, adjusted_width)

            # Freeze the header row
            worksheet.freeze_panes(1, 0)

            logger.info(f"Applied formatting to sheet: {sheet_name}")

        except Exception as e:
            logger.warning(f"Could not apply advanced formatting: {e}")

    def convert(
        self, apply_formatting: bool = True, create_multiple_sheets: bool = True
    ) -> str:
        """
        Convert JSON to Excel file.

        Args:
            apply_formatting: Whether to apply formatting to the Excel file
            create_multiple_sheets: Whether to create multiple sheets for complex data

        Returns:
            str: Path to the created Excel file
        """
        try:
            # Load JSON data
            data = self.load_json_data()

            # Create Excel writer
            with pd.ExcelWriter(self.output_file, engine="xlsxwriter") as writer:
                if create_multiple_sheets and isinstance(data, list) and len(data) > 0:
                    # Create multiple sheets for complex data
                    self.create_multiple_sheets(data, writer)

                    if apply_formatting:
                        # Apply formatting to all sheets
                        for sheet_name in writer.sheets:
                            if sheet_name == "Overview":
                                df = self.normalize_data(data)
                            elif sheet_name == "Skills_Details":
                                # Get the skills dataframe for formatting
                                skills_data = []
                                for i, record in enumerate(data):
                                    if (
                                        "skills_replaced" in record
                                        and record["skills_replaced"]
                                    ):
                                        job_title = record.get("job_title", f"Job_{i}")
                                        for skill in record["skills_replaced"]:
                                            skills_data.append(
                                                {
                                                    "job_title": job_title,
                                                    "skill": skill,
                                                    "likely_replaced": record.get(
                                                        "likely_replaced_by_ai", False
                                                    ),
                                                }
                                            )
                                df = pd.DataFrame(skills_data)
                            else:
                                continue

                            self.apply_formatting(writer, df, sheet_name)
                else:
                    # Single sheet conversion
                    df = self.normalize_data(data)
                    df.to_excel(writer, sheet_name="Data", index=False)

                    if apply_formatting:
                        self.apply_formatting(writer, df, "Data")

            logger.info(f"Successfully converted JSON to Excel: {self.output_file}")
            return self.output_file

        except Exception as e:
            logger.error(f"Error during conversion: {e}")
            raise


def main():
    """Main function to handle command-line execution."""
    parser = argparse.ArgumentParser(
        description="Convert JSON files to Excel format with advanced formatting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python json_to_excel_converter.py data.json
  python json_to_excel_converter.py data.json -o output.xlsx
  python json_to_excel_converter.py data.json --no-formatting
  python json_to_excel_converter.py data.json --single-sheet
        """,
    )

    parser.add_argument("input_file", help="Input JSON file path")
    parser.add_argument("-o", "--output", help="Output Excel file path (optional)")
    parser.add_argument(
        "--no-formatting",
        action="store_true",
        help="Skip applying formatting to the Excel file",
    )
    parser.add_argument(
        "--single-sheet",
        action="store_true",
        help="Create only a single sheet instead of multiple sheets",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Check if input file exists
    if not os.path.exists(args.input_file):
        logger.error(f"Input file does not exist: {args.input_file}")
        sys.exit(1)

    try:
        # Create converter instance
        converter = JSONToExcelConverter(args.input_file, args.output)

        # Convert the file
        output_path = converter.convert(
            apply_formatting=not args.no_formatting,
            create_multiple_sheets=not args.single_sheet,
        )

        print("\n✅ Conversion completed successfully!")
        print(f"📁 Output file: {output_path}")
        print(f"📊 File size: {os.path.getsize(output_path):,} bytes")

    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
