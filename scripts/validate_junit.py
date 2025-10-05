#!/usr/bin/env python3
"""
JUnit XML Validator

This script validates JUnit XML files for basic structure and content.
It checks for required elements, valid XML structure, and reports any issues.

Usage:
    python validate_junit.py <junit_xml_file> [--verbose]

Arguments:
    junit_xml_file: Path to the JUnit XML file to validate
    --verbose: Enable verbose output

Returns:
    0 if validation passes
    1 if validation fails
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Tuple


class JUnitValidator:
    """Validates JUnit XML files according to basic JUnit XML schema."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_file(self, file_path: str) -> bool:
        """Validate a JUnit XML file."""
        if not Path(file_path).exists():
            self.errors.append(f"File does not exist: {file_path}")
            return False

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return self._validate_root(root)
        except ET.ParseError as e:
            self.errors.append(f"XML parsing error: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Unexpected error: {e}")
            return False

    def _validate_root(self, root: ET.Element) -> bool:
        """Validate the root element of the JUnit XML."""
        if root.tag != "testsuites":
            self.errors.append(f"Root element must be 'testsuites', found '{root.tag}'")
            return False

        if self.verbose:
            print(f"✓ Root element is valid: {root.tag}")

        # Validate testsuites attributes
        self._validate_testsuites_attributes(root)

        # Validate child testsuite elements
        testsuites = root.findall("testsuite")
        if not testsuites:
            self.warnings.append("No testsuite elements found")
        else:
            for i, testsuite in enumerate(testsuites):
                self._validate_testsuite(testsuite, i)

        return len(self.errors) == 0

    def _validate_testsuites_attributes(self, root: ET.Element) -> None:
        """Validate attributes of the testsuites element."""
        # Optional attributes that should be present
        optional_attrs = ["id", "name", "tests", "failures", "errors", "time", "disabled", "skipped"]

        for attr in optional_attrs:
            if attr in root.attrib and self.verbose:
                print(f"✓ Found attribute: {attr} = {root.attrib[attr]}")

    def _validate_testsuite(self, testsuite: ET.Element, index: int) -> None:
        """Validate a testsuite element."""
        if testsuite.tag != "testsuite":
            self.errors.append(f"Expected 'testsuite' element, found '{testsuite.tag}' at index {index}")
            return

        if self.verbose:
            print(f"✓ Testsuite {index}: {testsuite.get('name', 'unnamed')}")

        # Check for testcase elements
        testcases = testsuite.findall("testsuite") + testsuite.findall("testcase")
        if not testcases:
            self.warnings.append(f"Testsuite {index} contains no testcase elements")

        # Validate each testcase
        for testcase in testcases:
            if testcase.tag == "testcase":
                self._validate_testcase(testcase)

    def _validate_testcase(self, testcase: ET.Element) -> None:
        """Validate a testcase element."""
        name = testcase.get("name", "unnamed")
        classname = testcase.get("classname", "")

        if self.verbose:
            print(f"  ✓ Testcase: {classname}.{name}")

        # Check for failure/error elements
        failure = testcase.find("failure")
        error = testcase.find("error")

        if failure is not None:
            if self.verbose:
                print(f"    ⚠ Test failed: {failure.get('message', 'No message')}")
        elif error is not None:
            if self.verbose:
                print(f"    ✗ Test errored: {error.get('message', 'No message')}")

    def print_report(self) -> None:
        """Print validation report."""
        if self.errors:
            print("\n❌ Validation Errors:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\n⚠️  Validation Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("✅ JUnit XML validation passed!")
        elif not self.errors:
            print("✅ JUnit XML validation passed with warnings")
        else:
            print("❌ JUnit XML validation failed")


def main():
    parser = argparse.ArgumentParser(description="Validate JUnit XML files")
    parser.add_argument("file", help="Path to JUnit XML file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    validator = JUnitValidator(verbose=args.verbose)
    is_valid = validator.validate_file(args.file)
    validator.print_report()

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()