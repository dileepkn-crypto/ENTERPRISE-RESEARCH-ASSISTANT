from pathlib import Path

from core.document_processor import (
    DocumentProcessor
)

from core.chunker import (
    DocumentChunker
)


def main():

    print()
    print("=" * 60)
    print("ResearchIQ Document Pipeline Test")
    print("=" * 60)

    document_path = input(
        "\nEnter PDF path: "
    ).strip().strip('"')

    path = Path(document_path)

    if not path.exists():

        print(
            f"\nFile not found: {path}"
        )

        return

    processor = DocumentProcessor()

    print("\nProcessing document...")

    pages = processor.process_document(
        path
    )

    print(
        f"Extracted pages: {len(pages)}"
    )

    if not pages:

        print(
            "No readable text was extracted."
        )

        return

    chunker = DocumentChunker()

    print(
        "\nCreating chunks..."
    )

    chunks = chunker.chunk_documents(
        pages
    )

    print(
        f"Generated chunks: {len(chunks)}"
    )

    print()
    print("=" * 60)
    print("SAMPLE CHUNKS")
    print("=" * 60)

    for chunk in chunks[:3]:

        print()
        print(
            f"Chunk ID : {chunk['chunk_id']}"
        )

        print(
            f"Document : {chunk['filename']}"
        )

        print(
            f"Page     : {chunk['page']}"
        )

        print(
            f"Index    : {chunk['chunk_index']}"
        )

        print("-" * 60)

        preview = chunk["text"][:500]

        print(preview)

        print()
        print("-" * 60)


if __name__ == "__main__":
    main()