import subprocess
import os
from typing import Dict, List, Any, Optional
from canals.serialization import default_to_dict, default_from_dict
from haystack.preview import component, Document
import glob, json

@component
class UnstructuredConnector:
    def __init__(self, api_key: str, output_dir: str):
        self.args = ["unstructured-ingest"]
        self.opts = ["--api-key", api_key]
       
        self.output_dir = output_dir
    
    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(self, args=self.args, opts = self.opts, output_dir=self.output_dir)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnstructuredConnector":
        return default_from_dict(cls, data)
    
    def run(self):
        command = self.args + self.opts
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, error = process.communicate()

        # Print output
        if process.returncode == 0:
            haystack_docs=[]

            for json_file in glob.glob('{self.output_dir}/**/*.json', recursive=True):
                with open(json_file,'r') as fin:
                    unstructured_doc = json.load(fin)
                for el in unstructured_doc:
                    text = "\n".join(el['text'] for el in unstructured_doc)
                    haystack_docs.append(Document(content=text, metadata=el['metadata']))
        else:
            print('Command failed. Error:')
            print(error.decode())
        return haystack_docs
    
@component
class UnstructuredGitHubConnector(UnstructuredConnector):
    """
    A component that allows you to use Unstrucrured.io connectors to fetch Documents from various APIs.

    """
    def __init__(self, api_key: str, repo: str, git_branch: str = "main", output_dir: str = "github-ingest-output"):
        super().__init__(api_key=api_key, output_dir = output_dir)

        self.args.append("github")
        self.repo = repo
        self.git_branch = git_branch
        self.output_dir = output_dir
       
    
    @component.output_types(documents=List[List[Document]])
    def run(self, repo: Optional[str] = None, git_branch: Optional[str] = None):
         # Run the command
        self.opts.append("--url")
        if repo !=  None:
            self.opts.append(repo)
        else:
            self.opts.append(self.repo)
        
        self.opts.append("--git-branch")
        if git_branch !=  None:
            self.opts.append(git_branch)
        else:
            self.opts.append(self.git_branch)
        
        self.opts.extend([
        "--structured-output-dir",  self.output_dir,
        "--num-processes", "2",
        "--verbose",
        "--partition-by-api"
        ])
        
        return super().run()


@component
class UnstructuredDiscordConnector(UnstructuredConnector):
    """
    A component that allows you to use Unstrucrured.io connectors to fetch Documents from various APIs.

    """
    def __init__(self, api_key: str, discord_token: str, output_dir: str = "discord-example"):
        super().__init__(api_key=api_key, output_dir=output_dir)
        self.args.append("discord")
        self.opts.extend(["--token", discord_token])
    
    @component.output_types(documents=List[List[Document]])
    def run(self, channels: str, output_dir: str = "discord-example", period: int = 1):
         # Run the command
        self.opts.extend([
        "--channels", channels,
        "--download-dir", "discord-ingest-download",
        "--structured-output-dir", output_dir,
        "--period", str(period),
        "--preserve-downloads",
        "--verbose",
        "--partition-by-api"])
        
        return super().run()