import re
from typing import List, Dict, Any

class MarkdownChunker:
    def __init__(self, target_chunk_size: int = 500, overlap: int = 80):
        self.target_chunk_size = target_chunk_size
        self.overlap = overlap

    def chunk_document(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Split a markdown document into clean semantic chunks by sections."""
        content = doc["content"]
        filename = doc["filename"]
        category = doc["category"]
        main_title = doc["title"]
        
        # Split by markdown H2 or H1 headings
        sections = re.split(r'\n(?=##?\s+)', content)
        chunks = []
        chunk_idx = 0

        for section in sections:
            section_clean = section.strip()
            if not section_clean:
                continue

            lines = section_clean.splitlines()
            section_title = lines[0].replace("#", "").strip() if lines and lines[0].startswith("#") else main_title

            # If section is small enough, keep as single chunk
            words = section_clean.split()
            if len(words) <= self.target_chunk_size or len(words) < 100:
                chunk_id = f"{category}_{chunk_idx:03d}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "filename": filename,
                    "category": category,
                    "title": f"{main_title} — {section_title}",
                    "section": section_title,
                    "content": section_clean,
                    "word_count": len(words)
                })
                chunk_idx += 1
            else:
                # Sub-chunk with overlap
                start = 0
                while start < len(words):
                    end = min(start + self.target_chunk_size, len(words))
                    sub_words = words[start:end]
                    sub_text = " ".join(sub_words)
                    chunk_id = f"{category}_{chunk_idx:03d}"
                    chunks.append({
                        "chunk_id": chunk_id,
                        "filename": filename,
                        "category": category,
                        "title": f"{main_title} — {section_title} (Part {chunk_idx+1})",
                        "section": section_title,
                        "content": sub_text,
                        "word_count": len(sub_words)
                    })
                    chunk_idx += 1
                    if end >= len(words):
                        break
                    start += self.target_chunk_size - self.overlap

        return chunks
