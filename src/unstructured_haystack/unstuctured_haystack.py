import subprocess
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
    
    @component.output_types(documents=List[Document])    
    def run(self):
        command = self.args + self.opts
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, error = process.communicate()

        # Print output
        if process.returncode == 0:
            haystack_docs=[]
            print(f'{self.output_dir}/**/*.json')
            for json_file in glob.glob(f'{self.output_dir}/**/*.json', recursive=True):
                with open(json_file,'r') as fin:
                    unstructured_doc = json.load(fin)
                for el in unstructured_doc:
                    metadata = el['metadata']
                    metadata['unstructured_type'] = el['type']
                    haystack_docs.append(Document(content=el['text'], metadata=metadata))
        else:
            print('Command failed. Error:')
            print(error.decode())
        return {"documents": haystack_docs}