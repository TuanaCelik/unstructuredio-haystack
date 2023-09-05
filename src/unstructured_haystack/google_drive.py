from typing import List, Optional
from haystack.preview import component, Document
from .unstuctured_haystack import UnstructuredConnector

@component
class UnstructuredGoogleDriveConnector(UnstructuredConnector):
    """
    A component that allows you to use Unstrucrured.io connectors to fetch Documents from various APIs.

    """
    def __init__(self, api_key: str, service_account_key: str, output_dir: str = "gdrive"):
        super().__init__(api_key=api_key, output_dir=output_dir)
        self.args.append("gdrive")
        self.opts.extend(["--service-account-key", service_account_key])
        self.output_dir = output_dir

    @component.output_types(documents=List[Document])
    def run(self,  drive_id: str):
         # Run the command
        self.opts.extend([
        "--drive-id", drive_id,
        "--structured-output-dir", self.output_dir,
        "--num-processes", "2",      
        "--partition-by-api"])
        
        return super().run()