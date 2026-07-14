from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_pages(pages, filename):
    """
    Split each page into chunks while keeping
    the page number and source filename.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    documents = []

    for page in pages:

        chunks = splitter.split_text(page["text"])

        for chunk in chunks:

            documents.append(
                {
                    "text": chunk,
                    "page": page["page"],
                    "source": filename
                }
            )

    return documents