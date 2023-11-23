from langchain.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities import ApifyWrapper
import os


class Crawl:
    def webcrawl(self):
        os.environ['OPENAI_API_KEY'] = "API_KEY"
        os.environ["APIFY_API_TOKEN"] = "API_KEY"

        apify = ApifyWrapper()
        url = input("Enter URL: ")
        loader = apify.call_actor(
            actor_id="apify/website-content-crawler",
            run_input={"startUrls": [{"url": url}]},
            dataset_mapping_function=lambda item: Document(
                page_content=item["text"] or "", metadata={"source": item["url"]}
            ),
        )

        index = VectorstoreIndexCreator().from_loaders([loader])

        query = input("Enter Prompt: ")
        result = index.query_with_sources(query)
        print(result["answer"])
        print(result["sources"])

