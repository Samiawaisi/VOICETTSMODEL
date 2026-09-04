import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from utils.text_chunker import TextChunker


class TestTextChunker:
    """Tests for Text Chunker."""

    def setup_method(self):
        self.chunker = TextChunker(max_chunk_size=100)

    def test_short_text_single_chunk(self):
        text = "This is a short text."
        chunks = self.chunker.chunk_text(text)
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_long_text_multiple_chunks(self):
        text = "This is a sentence. " * 20  # ~400 chars
        chunks = self.chunker.chunk_text(text)
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk) <= 100

    def test_empty_text(self):
        chunks = self.chunker.chunk_text("")
        assert len(chunks) == 1
        assert chunks[0] == ""

    def test_paragraph_break_splitting(self):
        text = "First paragraph. " * 3 + "\n\n" + "Second paragraph. " * 3
        chunker = TextChunker(max_chunk_size=60)
        chunks = chunker.chunk_text(text)
        assert len(chunks) >= 2

    def test_sentence_boundary_splitting(self):
        text = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five. Sentence six."
        chunker = TextChunker(max_chunk_size=50)
        chunks = chunker.chunk_text(text)
        for chunk in chunks:
            # Each chunk should end at a sentence or be the last chunk
            assert len(chunk) <= 50

    def test_no_content_lost(self):
        text = "Word " * 100
        chunks = self.chunker.chunk_text(text)
        reconstructed = " ".join(" ".join(chunks).split())
        original = " ".join(text.split())
        assert reconstructed == original

    def test_get_chunk_info(self):
        text = "Hello world. " * 50
        info = self.chunker.get_chunk_info(text)
        assert "total_length" in info
        assert "total_words" in info
        assert "num_chunks" in info
        assert "chunk_sizes" in info
        assert info["num_chunks"] == len(info["chunk_sizes"])

    def test_very_long_word(self):
        text = "a" * 200
        chunks = self.chunker.chunk_text(text)
        assert len(chunks) >= 2

    def test_default_chunk_size(self):
        chunker = TextChunker()
        assert chunker.max_chunk_size == 5000
