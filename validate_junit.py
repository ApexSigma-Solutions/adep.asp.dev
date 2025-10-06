validate_junit.py
Generated File

import xml.etree.ElementTree as ET
import sys
import os
from pathlib import Path

def validate_junit_xml(file_path):
    """Validate JUnit XML file structure and content"""
    print(f"🔍 Validating JUnit XML: {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ Error: File {file_path} not found")
        return False

    try:
        # Parse XML
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Check root element
        if root.tag not in ['testsuites', 'testsuite']:
            print(f"❌ Error: Root element should be 'testsuites' or 'testsuite', found '{root.tag}'")
            return False

        print(f"✅ Root element: {root.tag}")

        # Count test cases
        test_cases = root.findall('.//testcase')
        test_count = len(test_cases)

        # Count failures and errors
        failures = root.findall('.//failure')
        errors = root.findall('.//error')
        skipped = root.findall('.//skipped')

        failure_count = len(failures)
        error_count = len(errors)
        skipped_count = len(skipped)

        print(f"📊 Test Statistics:")
        print(f"   Total Tests: {test_count}")
        print(f"   Failures: {failure_count}")
        print(f"   Errors: {error_count}")
        print(f"   Skipped: {skipped_count}")
        print(f"   Passed: {test_count - failure_count - error_count - skipped_count}")

        # Check for required attributes
        required_attrs = []
        if root.tag == 'testsuite':
            required_attrs = ['name', 'tests']
        elif root.tag == 'testsuites':
            for suite in root.findall('testsuite'):
                if not suite.get('name'):
                    print(f"⚠️  Warning: testsuite missing 'name' attribute")
                if not suite.get('tests'):
                    print(f"⚠️  Warning: testsuite missing 'tests' attribute")

        # Check testcase elements
        for i, testcase in enumerate(test_cases):
            if not testcase.get('name'):
                print(f"⚠️  Warning: testcase {i+1} missing 'name' attribute")
            if not testcase.get('classname'):
                print(f"⚠️  Warning: testcase {i+1} missing 'classname' attribute")

        print(f"✅ JUnit XML validation completed successfully")
        print(f"📁 File size: {os.path.getsize(file_path)} bytes")

        return True

    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_junit.py <junit_xml_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_junit_xml(file_path)
    sys.exit(0 if success else 1)