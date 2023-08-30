# Unstructured Haystack

[![PyPI - Version](https://img.shields.io/pypi/v/unstructured-haystack.svg)](https://pypi.org/project/unstructured-haystack)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/unstructured-haystack.svg)](https://pypi.org/project/unstructured-haystack)

-----

## Unstructured Connectors for Haystack

This is an example Haystack 2.0 integration. It's an integration for Unstructured.io connectors. Please contribute 🚀

The current version has 2 available Unstructured connectors:
- Discord
- GitHub

## How to use in a Haystack 2.0 Pipeline 
For example, you can write documents fetched from Discord using the `UnstructuredDiscordConnector`:

```python
from haystack.preview import Pipeline
from haystack.preview.components.writers import DocumentWriter
from unstructured_haystack import UnstructuredDiscordConnector
from chroma_haystack import ChromaDocumentStore

# Chroma is used in-memory so we use the same instances in the two pipelines below
document_store = ChromaDocumentStore()
connector = UnstructuredDiscordConnector(api_key="UNSTRUCTURED_API_KEY", discord_token="DISCORD_TOKEN")

indexing = Pipeline()
indexing.add_component("connector", connector)
indexing.add_component("writer", DocumentWriter(document_store))
indexing.connect("connector.documents", "writer.documents")
indexing.run({"connector": {"channels" : "993539071815200889", "period": 3, "output_dir" : "discord-example"}})

```