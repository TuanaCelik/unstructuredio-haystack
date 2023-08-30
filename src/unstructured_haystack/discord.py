from typing import List
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