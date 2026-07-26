from pathlib import Path
from typing import Dict, List
import hashlib

import fitz
from docx import Document

from core.text_cleaner import clean_text, is_valid_text


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


class DocumentProcessor:
    """
    Extract text and metadata from supported academic documents.

    Supported formats:
        PDF
        DOCX
        TXT
    """

    def process_document(
        self,
        file_path: str | Path
    ) -> List[Dict]:

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        extension = file_path.suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        document_id = self._generate_document_id(
            file_path
        )

        if extension == ".pdf":
            return self._process_pdf(
                file_path,
                document_id
            )

        if extension == ".docx":
            return self._process_docx(
                file_path,
                document_id
            )

        if extension == ".txt":
            return self._process_txt(
                file_path,
                document_id
            )

        return []

    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    def _process_pdf(
        self,
        file_path: Path,
        document_id: str
    ) -> List[Dict]:

        pages = []

        document = fitz.open(file_path)

        try:

            total_pages = len(document)

            for page_index in range(total_pages):

                page = document.load_page(
                    page_index
                )

                raw_text = page.get_text(
                    "text"
                )

                text = clean_text(
                    raw_text
                )

                if not is_valid_text(text):
                    continue

                pages.append(
                    {
                        "document_id": document_id,
                        "filename": file_path.name,
                        "file_type": "pdf",

                        # Human-readable page number
                        "page": page_index + 1,

                        "total_pages": total_pages,
                        "text": text
                    }
                )

        finally:
            document.close()

        return pages

    # -----------------------------------------------------
    # DOCX
    # -----------------------------------------------------

    def _process_docx(
        self,
        file_path: Path,
        document_id: str
    ) -> List[Dict]:

        document = Document(
            file_path
        )

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        raw_text = "\n\n".join(
            paragraphs
        )

        text = clean_text(
            raw_text
        )

        if not is_valid_text(text):
            return []

        return [
            {
                "document_id": document_id,
                "filename": file_path.name,
                "file_type": "docx",

                # DOCX doesn't expose reliable physical
                # page boundaries through python-docx.
                "page": None,

                "total_pages": None,
                "text": text
            }
        ]

    # -----------------------------------------------------
    # TXT
    # -----------------------------------------------------

    def _process_txt(
        self,
        file_path: Path,
        document_id: str
    ) -> List[Dict]:

        raw_text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        text = clean_text(
            raw_text
        )

        if not is_valid_text(text):
            return []

        return [
            {
                "document_id": document_id,
                "filename": file_path.name,
                "file_type": "txt",
                "page": None,
                "total_pages": None,
                "text": text
            }
        ]

    # -----------------------------------------------------
    # Document ID
    # -----------------------------------------------------

    @staticmethod
    def _generate_document_id(
        file_path: Path
    ) -> str:

        hasher = hashlib.sha256()

        with open(file_path, "rb") as file:

            while True:

                block = file.read(
                    1024 * 1024
                )

                if not block:
                    break

                hasher.update(block)

        return hasher.hexdigest()[:16]