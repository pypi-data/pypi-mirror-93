"""Tests for the cli module."""

import logging
import sys
from io import StringIO
from typing import Any, Dict
from unittest import TestCase, skip
from unittest.mock import patch

from dphon.cli import __doc__ as doc
from dphon.cli import __version__ as version
from dphon.cli import process, run, setup, teardown

# disconnect logging for testing
logging.captureWarnings(True)
logging.disable(logging.CRITICAL)


class TestCommands(TestCase):
    """Test the --help and --version commands."""

    def test_help(self) -> None:
        """--help command should print cli module docstring"""
        sys.argv = ["dphon", "--help"]
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertRaises(SystemExit, run)
            self.assertEqual(output.getvalue().strip(), doc.strip())

    def test_version(self) -> None:
        """--version command should print program version"""
        sys.argv = ["dphon", "--version"]
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertRaises(SystemExit, run)
            self.assertEqual(output.getvalue().strip(), version.strip())


@patch("sys.stdout", new=StringIO())
class TestOptions(TestCase):
    """Test the various options available when running."""

    def setUp(self) -> None:
        """Set up a spaCy pipeline and CLI arguments for testing."""
        # default CLI arguments; would be populated by docopt
        self.args: Dict[str, Any] = {
            "<path>": ["tests/fixtures/laozi/"],  # testing fixture set
            "--min": None,
            "--max": None,
            "--all": False,
            "--format": "txt",
            "--ngram-order": "4",
            "--threshold": "0.7",
            "--len-limit": "50",
        }
        self.nlp = setup(self.args)

    def tearDown(self) -> None:
        """Unregister components to prevent name collisions."""
        teardown(self.nlp)

    def test_min(self) -> None:
        """--min option should limit to results with specified minimum length"""
        self.args["--min"] = "50"
        results = process(self.nlp, self.args).matches
        for result in results:
            self.assertTrue(len(result) >= 50)

    def test_max(self) -> None:
        """--max option should limit to results with specified maximum length"""
        self.args["--max"] = "4"
        results = process(self.nlp, self.args).matches
        for match in results:
            self.assertTrue(len(match) <= 4)

    def test_min_and_max(self) -> None:
        """--min and --max options together should limit to exact length"""
        self.args["--min"] = "8"
        self.args["--max"] = "8"
        results = process(self.nlp, self.args).matches
        for match in results:
            self.assertTrue(len(match) == 8)

    @skip("fixme")
    def test_keep_newlines(self) -> None:
        """--keep-newlines flag should preserve newlines in output"""
        self.args["--keep-newlines"] = True
        results = list(process(self.nlp, self.args).matches)
        self.assertTrue("\n" in results[0].utxt.text)

    @skip("todo")
    def test_variants_only(self) -> None:
        """--all flag should show results without graphic variation"""

    @skip("todo")
    def test_output_file(self) -> None:
        """--output option should write to a file"""
        pass
