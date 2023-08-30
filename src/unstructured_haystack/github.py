from typing import List, Optional
from haystack.preview import component, Document
from .unstuctured_haystack import UnstructuredConnector

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
       
    
    @component.output_types(documents=List[Document])
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
