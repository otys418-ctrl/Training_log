"""
PDF Parser using PyMuPDF to extract text from PDF files
"""

import fitz  # PyMuPDF
from typing import Union


class PDFParser:
    """
    Handles extraction of text content from PDF files
    """
    
    def parse(self, pdf_content: Union[bytes, str]) -> str:
        """
        Extract text from a PDF file
        
        Args:
            pdf_content: PDF file content as bytes or file path as string
        
        Returns:
            Extracted text as a single string
        
        Raises:
            ValueError: If the PDF cannot be opened or is empty
        """
        try:
            # Open PDF from bytes or file path
            if isinstance(pdf_content, bytes):
                doc = fitz.open(stream=pdf_content, filetype="pdf")
            else:
                doc = fitz.open(pdf_content)
            
            # Extract text from all pages
            text_content = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                text_content.append(text)
            
            doc.close()
            
            # Join all pages with double newline
            full_text = "\n\n".join(text_content)
            
            if not full_text.strip():
                raise ValueError("PDF contains no extractable text. The PDF may be image-based.")
            
            return full_text
            
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    def validate_pdf(self, pdf_content: bytes) -> bool:
        """
        Validate that the content is a valid PDF
        
        Args:
            pdf_content: PDF file content as bytes
        
        Returns:
            True if valid PDF, False otherwise
        """
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            doc.close()
            return True
        except:
            return False
