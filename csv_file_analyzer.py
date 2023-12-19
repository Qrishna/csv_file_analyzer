import csv
import json
import argparse
import time
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Process CSV file information.')
    parser.add_argument('-c', '--primary_context_column', type=int, default=1, help='Primary context column')
    parser.add_argument('-m', '--matching_context_column', help='Matching context column. Format: COLUMN=VALUE')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--filename', help='CSV file name')
    group.add_argument('-d', '--directory', help='Directory to process all files')
    return parser.parse_args()


def process_file(file_path, primary_context_column, matching_context_column=None):
    print(f"Processing file: {file_path}, Column: {primary_context_column}, Matching column context: {matching_context_column}")

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter='\t')
        header_row = next(csv_reader)

        total_lines = sum(1 for _ in csv_reader) + 1
        total_header_columns = len(header_row)

        file.seek(0)
        next(csv_reader)  # Skip header for further processing

        data = [row[primary_context_column - 1] if len(row) >= primary_context_column else '' for row in csv_reader]

        # Calculate matching context value if provided
        matching_context_column_key = None
        count_matching_context_value = None
        matching_context_value = None
        if matching_context_column:

            try:
                matching_column, matching_context_value = map(int, matching_context_column.split('='))
                matching_context_column_key = header_row[matching_column - 1]

                file.seek(0)
                next(csv_reader)  # Skip header
                count_matching_context_value = sum(1 for row in csv_reader if
                                                   len(row) >= matching_column and row[matching_column - 1] == str(
                                                       matching_context_value))

                file.seek(0)
                next(csv_reader)  # Skip header
                count_non_matching_context_value = sum(1 for row in csv_reader if
                                                       len(row) >= matching_column and row[matching_column - 1] != str(
                                                           matching_context_value))

            except ValueError:
                print("Invalid format for -m argument. Please use COLUMN=VALUE.")
        total_unique_lines_in_file = len(set(','.join(row) for row in csv.reader(open(file_path))))

        total_duplicate_lines_in_file = total_lines - total_unique_lines_in_file

        total_number_of_blank_lines_no_text = sum(1 for row in csv.reader(open(file_path)) if not any(row))

        total_number_of_rows_with_no_data_but_only_field_separators = sum(
            1 for row in csv.reader(open(file_path)) if not any(row) and any(cell.strip() == '' for cell in row))

        total_empty_for_column_in_context = sum(1 for value in data if value.isspace() or not value)

        total_unique_rows_for_context_columns = len(set(data))
        total_duplicate_rows_for_context_columns = total_lines - total_unique_rows_for_context_columns - 1

    return {
        "file_name": file_path,
        "primary_context_column": primary_context_column,
        "primary_context_column_header": header_row[primary_context_column - 1],
        "total_header_columns": total_header_columns,
        "total_lines": total_lines,
        "total_unique_lines_in_file": total_unique_lines_in_file,
        "total_duplicate_lines_in_file": total_duplicate_lines_in_file,
        "total_number_of_blank_lines_no_text": total_number_of_blank_lines_no_text,
        "total_number_of_rows_with_no_data_but_only_field_separators": total_number_of_rows_with_no_data_but_only_field_separators,
        "total_empty_for_column_in_context": total_empty_for_column_in_context,
        "total_unique_rows_for_context_column": total_unique_rows_for_context_columns,
        "total_duplicate_rows_for_context_column": total_duplicate_rows_for_context_columns,
        "matching_context_column_key": str(matching_context_column_key) + "=" + str(matching_context_value),
        "count_matching_context_value": count_matching_context_value,
        "count_non_matching_context_value": count_non_matching_context_value
    }


def main():
    start_time = time.time()
    args = parse_args()
    results = []
    fieldnames = [
        "file_name", "primary_context_column", "primary_context_column_header", "total_header_columns",
        "total_lines", "total_unique_lines_in_file", "total_duplicate_lines_in_file",
        "total_number_of_blank_lines_no_text", "total_number_of_rows_with_no_data_but_only_field_separators",
        "total_empty_for_column_in_context", "total_unique_rows_for_context_column",
        "total_duplicate_rows_for_context_column", "matching_context_column_key", "count_matching_context_value",
        "count_non_matching_context_value"
    ]
    os.makedirs("output", exist_ok=True)
    with open('output/complete_analysis.csv', 'w') as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(fieldnames)

        if args.directory:
            directory = args.directory

            for filename in sorted(os.listdir(directory)):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path) and file_path.endswith('.csv'):
                    file_result = process_file(file_path, args.primary_context_column, args.matching_context_column)

                    if file_result:
                        results.append(file_result)
                        output_writer.writerow([file_result[key] for key in fieldnames])

        elif args.filename:
            file_result = process_file(args.filename, args.primary_context_column, args.matching_context_column)
            if file_result:
                results.append(file_result)
                output_writer.writerow([file_result[key] for key in fieldnames])

        for result in results:
            print(json.dumps(result, indent=4))
        print(f"Total execution time: {time.time() - start_time} seconds")


if __name__ == "__main__":
    main()
