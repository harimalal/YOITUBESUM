import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("GEMINI_KEY", "test-key")

from app import extract_id


def test_extract_id_standard_url():
    assert extract_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_extract_id_short_url():
    assert extract_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_extract_id_shorts_url():
    assert extract_id("https://www.youtube.com/shorts/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_extract_id_invalid_url():
    assert extract_id("https://example.com") is None


def test_extract_id_empty():
    assert extract_id("") is None
