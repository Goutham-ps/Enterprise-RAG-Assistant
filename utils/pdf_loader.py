import sys

print("=" * 60)
print("Python Executable:", sys.executable)

try:
    import pypdf
    print("✅ pypdf module:", pypdf.__file__)
    from pypdf import PdfReader
    print("✅ PdfReader imported successfully")
except Exception as e:
    print("❌ Import Error:", e)
    raise

def load_pdf(file):

    reader = PdfReader(file)

    pages = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if text:

            pages.append(
                {
                    "text": text,
                    "page": page_number + 1
                }
            )

    return pages