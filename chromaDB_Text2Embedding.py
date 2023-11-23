from Parser.file_parser import Parser
from Parser.file_identifier import file_extension
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from database_location import database_location
import os




def create_embeddings(chunks):
    os.environ["OPENAI_API_KEY"] = "ADD_YOUR_API_KEY"
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    #global vectordb 
    try:
        vectordb = Chroma.from_documents(documents=chunks, embedding=embedding_function, persist_directory=database_location)
        vectordb.persist()
    except:
        from main import Access_doc
        print("Brain Doesnot Exist......")
        Access_doc()
        

def find_data():
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb2=Chroma(persist_directory=database_location, embedding_function=embedding)
    prompt_cv = input("Enter Your Prompt: ")
    chain = load_qa_chain(OpenAI(temperature=1), chain_type="stuff")
    matched_content = vectordb2.similarity_search(prompt_cv)
    answer = chain.run(input_documents=matched_content, question=prompt_cv)
    print(f"\n\nResponse: {answer}")   
    return prompt_cv, answer
    



class Text2Embedding:
    def __init__(self, path):
        self.path = path

    @property
    def chunks_creator(self):

        file_name, extension = file_extension(self.path)
        extension = extension.lower()

        if extension == ".txt":
            document = Parser(self.path).text_file
        elif extension == ".md":
            document = Parser(self.path).markdown_file
        elif extension == ".pdf":
            document = Parser(self.path).pdf_file
        elif extension == ".ppt" or extension == ".pptx" or extension == ".pptm":
            document = Parser(self.path).powerpoint_file
        elif extension == ".csv":
            document = Parser(self.path).csv_file
        elif extension == ".docx" or extension == ".doc":
            document = Parser(self.path).docx_file
        elif extension == ".xlsx":
            document = Parser(self.path).excel_file
        else:
            raise TypeError(f"Filetype of '{extension}' is not supported.")

        text_spillter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=24,
            length_function=len,
        )
        chunks = text_spillter.split_documents(document)
        return chunks










