from pypdf import PdfReader


def extract_resume_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


if __name__ == "__main__":

    pdf_path = "resume.pdf"

    resume_text = extract_resume_text(
        pdf_path
    )

    print("\nExtracted Resume Text:\n")
    print(resume_text)