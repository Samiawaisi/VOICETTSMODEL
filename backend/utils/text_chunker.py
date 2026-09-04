import re
from typing import List
from config import MAX_CHUNK_SIZE


class TextChunker:
    """Splits long text into manageable chunks for TTS processing."""

    def __init__(self, max_chunk_size: int = MAX_CHUNK_SIZE):
        self.max_chunk_size = max_chunk_size

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks, preferring natural break points."""
        text = text.strip()

        if len(text) <= self.max_chunk_size:
            return [text]

        chunks = []
        remaining = text

        while remaining:
            if len(remaining) <= self.max_chunk_size:
                chunks.append(remaining.strip())
                break

            # Find the best split point
            split_pos = self._find_split_point(remaining)
            chunk = remaining[:split_pos].strip()
            if chunk:
                chunks.append(chunk)
            remaining = remaining[split_pos:].strip()

        return chunks

    def _find_split_point(self, text: str) -> int:
        """Find the best position to split text."""
        max_pos = self.max_chunk_size

        # Priority 1: Split at paragraph break
        para_break = text.rfind("\n\n", 0, max_pos)
        if para_break > max_pos * 0.3:
            return para_break + 2

        # Priority 2: Split at sentence end (. ! ?)
        sentence_pattern = re.compile(r'[.!?]\s', re.DOTALL)
        matches = list(sentence_pattern.finditer(text[:max_pos]))
        if matches and matches[-1].end() > max_pos * 0.3:
            return matches[-1].end()

        # Priority 3: Split at newline
        newline = text.rfind("\n", 0, max_pos)
        if newline > max_pos * 0.3:
            return newline + 1

        # Priority 4: Split at comma or semicolon
        for sep in ["; ", ", "]:
            pos = text.rfind(sep, 0, max_pos)
            if pos > max_pos * 0.3:
                return pos + len(sep)

        # Priority 5: Split at space
        space = text.rfind(" ", 0, max_pos)
        if space > 0:
            return space + 1

        # Fallback: Hard split
        return max_pos

    def get_chunk_info(self, text: str) -> dict:
        """Get information about how text would be chunked."""
        chunks = self.chunk_text(text)
        return {
            "total_length": len(text),
            "total_words": len(text.split()),
            "num_chunks": len(chunks),
            "chunk_sizes": [len(c) for c in chunks],
            "chunk_words": [len(c.split()) for c in chunks]
        }
