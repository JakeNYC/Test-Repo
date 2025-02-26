import os
import re
from PyPDF2 import PdfMerger, PdfReader
import glob

def merge_numbered_pdfs(directory='.', output_filename='merged_statements.pdf'):
    print("\n=== PDF MERGER LOG ===")
    
    # Get all PDF files matching the numbered pattern
    pattern = "*.pdf"  # Get all PDFs to make sure we don't miss any
    print(f"Searching for files matching pattern: {pattern}")
    all_pdf_files = glob.glob(os.path.join(directory, pattern))
    
    # Filter to only include Chase statements
    pdf_files = [f for f in all_pdf_files if "Chase" in os.path.basename(f)]
    
    if not pdf_files:
        print("ERROR: No Chase PDF files found. Please check the directory.")
        return
    
    print(f"Found {len(pdf_files)} Chase PDF files.")
    
    # Extract the number prefix and sort by numerical value
    numbered_files = []
    for pdf in pdf_files:
        filename = os.path.basename(pdf)
        match = re.search(r'^(\d+)\.', filename)
        if match:
            try:
                number = int(match.group(1))
                numbered_files.append((number, pdf))
            except ValueError:
                print(f"Warning: Could not parse number from {filename}")
        else:
            print(f"Warning: No number prefix found in {filename}")
    
    # Sort by the extracted number
    numbered_files.sort(key=lambda x: x[0])
    
    # List the files in the order they'll be merged
    print("\nFiles will be processed in this order:")
    for idx, (number, pdf) in enumerate(numbered_files, 1):
        print(f"{idx}. [{number:02d}] {os.path.basename(pdf)}")
    
    # Merge the PDFs
    print("\n=== BEGINNING MERGE PROCESS ===")
    merger = PdfMerger()
    successful_files = 0
    failed_files = []
    total_pages = 0
    
    for number, pdf in numbered_files:
        filename = os.path.basename(pdf)
        print(f"\nProcessing [{number:02d}] {filename}")
        
        try:
            # Verify the file is a valid PDF
            reader = PdfReader(pdf)
            num_pages = len(reader.pages)
            print(f"  Pages: {num_pages}")
            
            # Add to merger
            merger.append(pdf)
            successful_files += 1
            total_pages += num_pages
            
            print(f"  Success: Added to merger")
            
        except Exception as e:
            print(f"  ERROR: Failed to process {filename}")
            print(f"  Error details: {str(e)}")
            failed_files.append((filename, str(e)))
    
    # Write the merged PDF
    print("\n=== FINALIZING MERGED DOCUMENT ===")
    if successful_files > 0:
        try:
            output_path = os.path.join(directory, output_filename)
            print(f"Writing merged PDF to: {output_path}")
            merger.write(output_path)
            merger.close()
            
            # Verify the output file
            if os.path.exists(output_path):
                output_reader = PdfReader(output_path)
                final_pages = len(output_reader.pages)
                print(f"Success: Created merged PDF with {final_pages} pages")
            else:
                print("ERROR: Output file was not created")
            
        except Exception as e:
            print(f"ERROR writing merged file: {str(e)}")
    else:
        print("ERROR: No files were successfully processed, cannot create merged PDF.")
    
    # Summary
    print("\n=== SUMMARY ===")
    print(f"Total files processed: {successful_files} of {len(numbered_files)}")
    print(f"Total pages in merged document: {total_pages}")
    
    if failed_files:
        print("\nFiles that couldn't be processed:")
        for file, error in failed_files:
            print(f"- {file}: {error}")
    
    print("=== END OF LOG ===\n")

if __name__ == "__main__":
    # Run the merging function
    merge_numbered_pdfs()