import tkinter as tk

import pytest

from src.artifactcalculator.main import ArtifactCalculatorApp, process_file


def test_process_file():
    test_path = "tests/test_artifact.md"
    expected_output = "Level 3+ (1920)"
    assert process_file(test_path) == expected_output


def test_select_file(monkeypatch):
    # Mock the file dialog to return a specific file path
    def mock_askopenfilename(**kwargs):
        return "tests/test_artifact.md"

    monkeypatch.setattr("tkinter.filedialog.askopenfilename", mock_askopenfilename)

    # Create a function to mock Label's config method
    mock_config_calls = []

    def mock_config(self, **kwargs):
        mock_config_calls.append(kwargs)

    monkeypatch.setattr(tk.Label, "config", mock_config)

    # Create a Tkinter root window
    root = tk.Tk()

    # Create an instance of the ArtifactCalculatorApp with the mock root
    app = ArtifactCalculatorApp(root)

    # Call the select_file method
    app.select_file()

    # Check that Label.config was called with the expected text
    assert {"text": "Level 3+ (1920)"} in mock_config_calls
