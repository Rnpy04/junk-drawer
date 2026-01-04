from pypdf import PdfMerger

def merge_pdfs(output_path, *pdf_files):
    merger = PdfMerger()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(output_path)
    merger.close()


merge_pdfs(
    "merged.pdf",
    "a.pdf",
    "b.pdf",
    "c.pdf"
)
