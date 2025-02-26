import os
import sys
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import tabula

def convert_pdf_to_excel(pdf_path, output_path=None):
    """
    Convert a PDF file to Excel format
    
    Parameters:
    pdf_path (str): Path to the PDF file
    output_path (str, optional): Path to save the Excel file. If not provided, 
                                uses the PDF filename with .xlsx extension
    
    Returns:
    str: Path to the created Excel file
    """
    print(f"Processing: {pdf_path}")
    
    if not output_path:
        # Generate output filename by replacing .pdf with .xlsx
        output_path = os.path.splitext(pdf_path)[0] + ".xlsx"
    
    try:
        # Try using tabula-py first (good for native PDFs with text)
        print("Attempting to extract tables with tabula-py...")
        dfs = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
        
        if dfs and len(dfs) > 0:
            print(f"Extracted {len(dfs)} tables")
            
            # Create a Excel writer object
            with pd.ExcelWriter(output_path) as writer:
                # Write each dataframe to a different worksheet
                for i, df in enumerate(dfs):
                    sheet_name = f"Table_{i+1}"
                    print(f"Writing table {i+1} to sheet {sheet_name}")
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"Successfully created Excel file: {output_path}")
            return output_path
            
        else:
            print("No tables detected with tabula-py. Attempting OCR...")
            
            # If tabula didn't work, try OCR approach
            print("Converting PDF to images...")
            images = convert_from_path(pdf_path)
            
            all_text = []
            for i, image in enumerate(images):
                print(f"Processing page {i+1}/{len(images)}")
                text = pytesseract.image_to_string(image)
                all_text.append(text)
            
            # Create a simple DataFrame with the extracted text
            df = pd.DataFrame({"Page": range(1, len(all_text) + 1), "Text": all_text})
            
            # Write to Excel
            df.to_excel(output_path, index=False)
            print(f"Created Excel file with OCR text: {output_path}")
            return output_path
            
    except Exception as e:
        print(f"Error converting PDF to Excel: {str(e)}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_excel.py <pdf_file> [output_excel_file]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found")
        sys.exit(1)
    
    convert_pdf_to_excel(pdf_path, output_path)

if __name__ == "__main__":
    main()