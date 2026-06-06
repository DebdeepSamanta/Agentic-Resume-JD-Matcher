import fitz  # PyMuPDF


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract clean plain text from a PDF supplied as raw bytes.

    Args:
        file_bytes: Raw bytes of the PDF file.

    Returns:
        A single string of all text found across all pages,
        with excessive blank lines removed.

    Raises:
        ValueError: If the PDF is empty or could not be read.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    if doc.page_count == 0:
        raise ValueError("PDF has no pages.")

    pages_text: list[str] = []
    for page in doc:
        pages_text.append(page.get_text("text"))

    doc.close()

    raw = "\n".join(pages_text)

    # Collapse blank lines and strip leading/trailing whitespace per line
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    result = "\n".join(lines)

    if len(result) < 20:
        raise ValueError("Extracted text is too short — PDF may be image-only or corrupted.")

    return result
