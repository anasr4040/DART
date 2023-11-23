from chromaDB_Text2Embedding import create_embeddings
from database import Brains, File_Handling, add_file_to_brain, chunks_retrive, get_file_from_brain, add_chat_to_brain
#from crawl import Crawl


def upload_doc():
            option = input("Create New Brain(Y/N)\nOption: ")
            if option.lower() == 'y':
                
                brain = input("Enter the name of brain: ")
                Brains(brain).create_brain()
            else:
                print(".........................................")
            
            print("\n\nUpload in Existing Brain\n\n")
            brain = input("Enter the name of brain: ")
            collection = Brains(brain).get_brain
            add_file_to_brain(collection)

def Access_doc():
        print("\n\nAccessing Existing Brain\n\n")
        brain = input("Enter the name of brain: ")
        collection = Brains(brain).get_brain
        chunks=chunks_retrive(collection)
        create_embeddings(chunks)
        continue_prompt='y'
        while continue_prompt.lower()=='y':
            chat=get_file_from_brain(collection)
            print(f"{type(chat)}\n\nchat: {chat}")
            add_chat_to_brain(collection,chat)    
            continue_prompt=input("Do you want to give prompt again? (Y/N): ")

choice = "y"
while choice.lower() == "y":
    option_pdf_crawl = input("Upload File(press U)\n"
                             "Crawl Website(Press C)\n"
                             "Access already uploaded data(Press A)\n"
                             "Option: ")

    if option_pdf_crawl.lower() == 'u':
        upload_doc()                
        
    elif option_pdf_crawl.lower() == 'a':
        Access_doc()
        

    #elif option_pdf_crawl.lower() == 'c':
      #elif option_pdf_crawl.lower()=='q':
         #create_embeddings()
