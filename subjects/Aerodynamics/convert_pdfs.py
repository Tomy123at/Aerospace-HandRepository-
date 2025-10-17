import os
import PyPDF2
import sys

def convert_pdf_to_text(pdf_path, txt_path):
    try:
        # Check if file exists and is readable
        if not os.path.exists(pdf_path):
            print(f"Error: File does not exist: {pdf_path}")
            return False
            
        # Check file size
        file_size = os.path.getsize(pdf_path)
        if file_size == 0:
            print(f"Error: File is empty: {pdf_path}")
            return False
            
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                print(f"Error: PDF is encrypted: {pdf_path}")
                return False
                
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Check if we got any text
            if not text.strip():
                print(f"Warning: No text extracted from: {pdf_path}")
            
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
            print(f"Successfully converted {pdf_path} to {txt_path}")
            return True
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")
        return False

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a directory for text files if it doesn't exist
    txt_dir = os.path.join(current_dir, 'text_files')
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(current_dir) if f.lower().endswith('.pdf')]
    print(f"Found {len(pdf_files)} PDF files")
    
    # Convert all PDF files in the current directory
    successful = 0
    failed = 0
    
    for filename in pdf_files:
        pdf_path = os.path.join(current_dir, filename)
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(txt_dir, txt_filename)
        
        if convert_pdf_to_text(pdf_path, txt_path):
            successful += 1
        else:
            failed += 1
    
    print(f"\nConversion Summary:")
    print(f"Total PDFs found: {len(pdf_files)}")
    print(f"Successfully converted: {successful}")
    print(f"Failed to convert: {failed}")
    
    # List files that weren't converted
    if failed > 0:
        print("\nFiles that weren't converted:")
        for filename in pdf_files:
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(txt_dir, txt_filename)
            if not os.path.exists(txt_path):
                print(f"- {filename}")

if __name__ == "__main__":
    main() 