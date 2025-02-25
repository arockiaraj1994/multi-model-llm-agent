import subprocess

# Generate TEST cases
subprocess.run(["python", "run_test_str.py"])

# Run the generated test cases
subprocess.run(["python", "integration-manager-test.py"])


# Clean up the test environment
subprocess.run(["python", "integration-manager-clean-up.py"])