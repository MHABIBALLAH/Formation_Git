import unittest
import sys
import os

def run_all_tests():
    """
    Discovers and runs all tests in the 'tests' directory.
    This script should be run from the root of the project.
    """
    # Add the 'src' directory to the Python path to allow imports of application code
    # This is the key to making imports like `from core.ocr.reader import ...` work
    # from within the test files.
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)

    print("--- ComptaAI Test Suite ---")
    print(f"Project root added to path: {project_root}")
    print("Starting test discovery in 'tests/' directory...")

    # Discover and run all tests found in the 'tests' directory
    loader = unittest.TestLoader()
    suite = loader.discover('tests', top_level_dir=project_root)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("--- Test Run Complete ---")

    # Exit with a non-zero status code if any tests failed
    if not result.wasSuccessful():
        print("Some tests failed.")
        sys.exit(1)
    else:
        print("All tests passed successfully!")
        sys.exit(0)

if __name__ == '__main__':
    run_all_tests()
