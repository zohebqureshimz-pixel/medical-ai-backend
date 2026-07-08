import os
import re
import fitz



def extract_pages(pdf_path):

    doc = fitz.open(pdf_path)

    document_name = os.path.basename(pdf_path)

    pages = []

    for page_num, page in enumerate(doc):

        pages.append(
            {
                "page": page_num + 1,
                "text": page.get_text()
            }
        )
    
    return pages , document_name

  

# clean

def clean_pdf(text):
    text = text.lower()
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# chunk
chunk_size = 300
overlap = 50

def chunk_pages (pages,  document_name,
    chunk_size=300):

    chunks = []
    
    
    for page in pages:
        
        words = page["text"].split()

        for i in range (0,len(words) , chunk_size - overlap):

            chunk = " ".join(
                words[i:i + chunk_size]
            )

            chunks.append(
                {
                    "document" : document_name,
                    "page": page["page"],
                    "chunk": chunk
                }
            )
            print(len(chunks))

    for chunk in chunks[:5]:
        print(chunk["document"])

    return chunks



def process_pdf(
    pdf_path
):

    pages, document_name = (
        extract_pages(pdf_path)
    )

    for page in pages:

        page["text"] = clean_pdf(
            page["text"]
        )

    chunks = chunk_pages(
        pages,
        document_name
    )

    return chunks