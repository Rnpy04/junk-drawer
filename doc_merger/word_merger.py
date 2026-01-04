from docx import Document
from docxcompose.composer import Composer

def merge_word_files(output_path, *input_files):
    first_doc = Document(input_files[0])
    composer = Composer(first_doc)

    for file in input_files[1:]:
        doc = Document(file)
        composer.append(doc)

    composer.save(output_path)


merge_word_files(
    "merged.docx",
    "file1.docx",
    "file2.docx",
    "file3.docx"
)
