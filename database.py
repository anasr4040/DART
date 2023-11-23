from chromaDB_Text2Embedding import Text2Embedding, find_data
from Parser.file_identifier import file_extension
from langchain.docstore.document import Document
from database_location import database_location
import chromadb
import uuid
import ast


def add_file_to_brain(collection):
    global path
    documents = []
    metadata = []
    ids = []
    path = input("Enter Path of Document: ")
    chunks = Text2Embedding(path).chunks_creator
    file_name, extension = file_extension(path)
    #print(f"Chunks uploaded:\n{chunks}")

    for chunk in chunks:
        documents.append(str({"page_content": chunk.page_content, "metadata": chunk.metadata}))
        ids.append(str(uuid.uuid4()))
        metadata.append({"file": file_name})

    #print(documents[0])

    collection.add(
        documents=documents,
        metadatas=metadata,
        ids=ids
    )
    print(f"File at the path '{path}' uploaded. ")


def add_chat_to_brain(collection, chat):
    print(chat)
    collection.upsert(
        ids=str(uuid.uuid5(uuid.NAMESPACE_DNS, "chat")),
        metadatas=[{"file": 'chat'}],
        documents=chat
    )
    
    print("\n\nCHAT UPDATED SUCCESSFULLY\n\n")



'''def chat_again(chat,total_chunk):
    create_embeddings(total_chunk)
    prompt,answer=find_data()
    chat.append(str({"Prompt": prompt, "Response": answer}))'''

def chunks_retrive(collection):
    total_chunk = []
    chunks_object = collection.get(where={
        "file": {
            "$ne": "chat"
        }
    })

    chunks = chunks_object["documents"]
   
    for chunk in chunks:
        temp_chunk = ast.literal_eval(chunk)
        total_chunk.append(Document(page_content=temp_chunk['page_content'], metadata=temp_chunk['metadata']))
        
    return total_chunk

def get_file_from_brain(collection):
    
    chat = []
    chat_object = collection.get(ids=str(uuid.uuid5(uuid.NAMESPACE_DNS, "chat")))
    #print(chat_object['documents'])
    if len(chat_object["documents"]) != 0:
        chat.append(chat_object["documents"])
        for msg in chat:
            print(msg)
        #print(chat_object["documents"])
      # print(chat)
    

    prompt,answer=find_data()
    print(type(prompt))
    chat.append(str({"Prompt": prompt, "Response": answer}))
    print(f"get file from brain function:\n{chat}")
    return str(chat)


class Brains:

    def __init__(self, brain_name):
        self.brain_name = brain_name
        
       
        
    def create_brain(self):
        client = chromadb.PersistentClient(path=database_location)
        
        try:
            client.create_collection(name=self.brain_name)
            File_Handling.add_brain(self.brain_name)
            print(f"\n\nCollection of name '{self.brain_name}' is created.")
        except:
            print(f"{self.brain_name} already exists!!!! Enter other name....\n")
            brain = input("Enter the brain name: ")
            Brains(brain).create_brain()
            

        

    @property
    def get_brain(self):
        client = chromadb.PersistentClient(path=database_location)
        collection = client.get_or_create_collection(name=self.brain_name)
        return collection


class File_Handling:
    def __init__(self) -> None:
        pass

    def add_brain(brain_name):
        try:
            with open("brains.txt", 'a') as f:
                f.write(brain_name +'\n')
            print("New brain added")
        except IOError:
         print("Error: could not create file brain.txt")

    def read_file(self):
        try:
            with open("brains.txt", 'r') as f:
                contents = f.read()
                print(contents)
        except IOError:
            print("Error: could not read file brains.txt")