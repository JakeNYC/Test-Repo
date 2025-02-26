import os
import re
from datetime import datetime
import glob

def extract_date(filename):
    # Extract month and day from filename format "Chase Month DD.pdf" with year
    match = re.search(r'Chase (\w+) (\d+)\.pdf', filename)
    if match:
        month_name, day = match.groups()
        # Convert month name to number
        try:
            month_num = datetime.strptime(month_name, '%B').month
            # Extract year from the filename
            year = 2020 if '20.pdf' in filename else 2021
            # Create a datetime object for sorting
            date_obj = datetime(year, month_num, int(day))
            return date_obj
        except ValueError:
            # Handle abbreviated month names
            month_map = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'March': 3, 'Apr': 4, 'April': 4,
                'May': 5, 'Jun': 6, 'June': 6, 'Jul': 7, 'July': 7, 'Aug': 8,
                'Sep': 9, 'Sept': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
            }
            if month_name in month_map:
                month_num = month_map[month_name]
                year = 2020 if '20.pdf' in filename else 2021
                date_obj = datetime(year, month_num, int(day))
                return date_obj
    return None

def rename_pdf_files(directory='.'):
    # Get all PDF files matching the pattern
    pdf_files = glob.glob(os.path.join(directory, "Chase *.pdf"))
    
    # Create a list of tuples (filename, date)
    files_with_dates = []
    for file in pdf_files:
        basename = os.path.basename(file)
        date = extract_date(basename)
        if date:
            files_with_dates.append((file, date))
        else:
            print(f"Warning: Could not parse date from {basename}")
    
    # Sort files by date
    files_with_dates.sort(key=lambda x: x[1])
    
    # Rename files with order prefix
    for index, (file_path, date) in enumerate(files_with_dates, 1):
        directory = os.path.dirname(file_path)
        old_name = os.path.basename(file_path)
        # Format the number with leading zero if needed
        prefix = f"{index:02d}"
        new_name = f"{prefix}.{old_name}"
        new_path = os.path.join(directory, new_name)
        
        print(f"Renaming: {old_name} -> {new_name} (Date: {date.strftime('%Y-%m-%d')})")
        os.rename(file_path, new_path)

if __name__ == "__main__":
    # Run the renaming function
    rename_pdf_files()
    print("File renaming complete!")