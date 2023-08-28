import subprocess
from typing import Dict, List, Any, Optional
from canals.serialization import default_to_dict, default_from_dict
from haystack.preview import component, Document

@component
class UnstructuredGitHubConnector:
    """
    A component that allows you to use Unstrucrured.io connectors to fetch Documents from various APIs.

    """
    def __init__(self, api_key: str = None):
        
        self.command = [
        "unstructured-ingest",
        "github",
        "--api-key", api_key,
        ]
        self.api_key = api_key

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(self, connector=self.connector, api_key=self.api_key)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnstructuredGitHubConnector":
        return default_from_dict(cls, data)
    
    @component.output_types(documents=List[List[Document]])
    def run(self, url: str, git_branch: str = "main", num_processes: int = 2):
         # Run the command
        options = [
        "--url", url,
        "--git-branch", git_branch,
        "--structured-output-dir",  "github-ingest-output",
        "--num-processes", str(num_processes),
        "--verbose",
        "--partition-by-api"]
        
        self.command.extend(options)

        process = subprocess.Popen(self.command, stdout=subprocess.PIPE)
        output, error = process.communicate()

        # Print output
        if process.returncode == 0:
            print('Command executed successfully. Output:')
            print(output.decode())
        else:
            print('Command failed. Error:')
            print(error.decode())
        return [Document(content="blablabla")]


@component
class UnstructuredDiscordConnector:
    """
    A component that allows you to use Unstrucrured.io connectors to fetch Documents from various APIs.

    """
    def __init__(self, api_key: str = None, discord_token: str = None):
        
        self.command = [
        "unstructured-ingest",
        "discord",
        "--token", discord_token,
        "--api-key", api_key,
        ]
        self.api_key = api_key
        self.discord_token = discord_token

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(self, discord_token=self.discord_token, api_key=self.api_key)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnstructuredDiscordConnector":
        return default_from_dict(cls, data)
    
    @component.output_types(documents=List[List[Document]])
    def run(self, channels: str = None, download_dir: str = "discord-ingest-download"):
         # Run the command
        options = [
        "--channels", channels,
        "--download-dir", download_dir,
        "--structured-output-dir", "discord-example",
        "--preserve-downloads",
        "--verbose",
        "--partition-by-api"]
        
        self.command.extend(options)

        process = subprocess.Popen(self.command, stdout=subprocess.PIPE)
        output, error = process.communicate()

        # Print output
        if process.returncode == 0:
            print('Command executed successfully. Output:')
            print(output.decode())
        else:
            print('Command failed. Error:')
            print(error.decode())
        return [Document(content="blablabla")]