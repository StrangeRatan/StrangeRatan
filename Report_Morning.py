import os
from datetime import datetime
from openpyxl import Workbook

def count_images_in_folder(folder_path):
    files = [file for file in os.listdir(folder_path) if file.lower().endswith('.jpg')]
    return len(files)

def main():
    folder1_path = "Stricker image/output_open"
    folder2_path = "Stricker image/output_close"

    total_images_folder1 = count_images_in_folder(folder1_path)
    total_images_folder2 = count_images_in_folder(folder2_path)

    # Set the desired date and time
    specified_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    formatted_date_time = specified_time.strftime("%d-%b-%Y_%I-%M-%S%p")

    # Create the output string
    output = f"Date/Time\tMorning {formatted_date_time}\n" \
             f"Number of store aduit\t{total_images_folder1 + total_images_folder2}\n" \
             f"Store Open at 7:00 AM\t{total_images_folder1}\n" \
             f"Store Close at 7:00 AM\t{total_images_folder2}\n" \
             f"\tOpen store PPT Attach"

    # Create folder named 'Result'
    output_folder = "Result"
    os.makedirs(output_folder, exist_ok=True)

    # Create a new workbook
    workbook = Workbook()
    sheet = workbook.active

    # Split the output into rows and cells and write to Excel
    rows = output.split('\n')
    for row_idx, row in enumerate(rows, start=1):
        cells = row.split('\t')
        for col_idx, cell_value in enumerate(cells, start=1):
            sheet.cell(row=row_idx, column=col_idx).value = cell_value

    # Save the workbook to an Excel file in the 'Result' folder
    output_filename = os.path.join(output_folder, f'output_{formatted_date_time}.xlsx')
    workbook.save(filename=output_filename)
    print(f"Output saved to {output_filename}")

if __name__ == "__main__":
    main()
