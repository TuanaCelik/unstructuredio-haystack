from typing import List, Optional
from haystack.preview import component, Document
from .unstuctured_haystack import UnstructuredConnector

@component
class UnstructuredDiscordConnector(UnstructuredConnector):
    """
    A component that allows you to use Unstrucrured.io connectors to fetch Documents from various APIs.

    """
    def __init__(self, api_key: str, discord_token: str, output_dir: str = "discord-example"):
        super().__init__(api_key=api_key, output_dir=output_dir)
        self.args.append("discord")
        self.opts.extend(["--token", discord_token])
    
    @component.output_types(documents=List[Document])
    def run(self, channels: str, output_dir: Optional[str] = "discord-example", period: Optional[int] = 1):
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

# class UnstructuredGitHubConnectorV1(BaseComponent):
#     outgoing_edges = 1

#     def __init__(self, api_key: str, discord_token: str, output_dir: str = "discord-example"):
#         self.connector = UnstructuredGitHubConnector(api_key=api_key, repo=repo, git_branch=git_branch, output_dir=output_dir)
    
#     def run(self, api_key: str, discord_token: str, output_dir: str = "discord-example"):
#         documents = self.connector.run(repo=repo, git_branch=git_branch)
#         docs = []
#         for doc in documents:
#             docs.append(Document(content=doc.content, metadata=doc.metadata))
#         output = {"documents": docs}
#         return output, "output_1"
    
#     def run_batch(self, queries: str | List[str] | None = None, file_paths: List[str] | None = None, labels: MultiLabel | List[MultiLabel] | None = None, documents: List[Document] | List[List[Document]] | None = None, meta: Dict[str, Any] | List[Dict[str, Any]] | None = None, params: dict | None = None, debug: bool | None = None):
#         pass