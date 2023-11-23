from Parser.file_parser import Parser
from Parser.file_identifier import file_extension
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os
import openai



openai.api_key = "ADD_YOUR_API_KEY"
os.environ["OPENAI_API_KEY"] = "ADD_YOUR_API_KEY"


path = r"PathToTheFileYouWantToScan"
text = ""
file_name, extension = file_extension(path)

extension = extension.lower()

if extension == ".txt":
    document = Parser(path).text_file
elif extension == ".md":
    document = Parser(path).markdown_file
elif extension == ".pdf":
    document = Parser(path).pdf_file
elif extension == ".ppt" or extension == ".pptx" or extension == ".pptm":
    document = Parser(path).powerpoint_file
elif extension == ".csv":
    document = Parser(path).csv_file
elif extension == ".docx" or extension == ".doc":
    document = Parser(path).docx_file
else:
    raise TypeError(f"Filetype of '{extension}' is not supported.")

for page in document:
    text += page.page_content

text_spillter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=24,
    length_function=len,
)

chunks = text_spillter.split_text(text)
embeddings = OpenAIEmbeddings()
db = FAISS.from_texts(chunks, embeddings)

prompt_cv = "List all the skills and past experiences that uploaded CV contains.Your response must be in the following format:" \
            "\nFormat:{" \
            "\n1:Skill 1" \
            "\n2:Skill 2" \
            "\n}"

chain = load_qa_chain(OpenAI(temperature=0.7), chain_type="stuff")
matched_content = db.similarity_search(prompt_cv)
print(matched_content)
answer = chain.run(input_documents=matched_content, question=prompt_cv)

print(answer)








