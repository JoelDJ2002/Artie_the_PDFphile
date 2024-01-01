import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI, ChatGooglePalm
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from HTMLCSS import css,bot_template, user_template
from langchain.llms import HuggingFaceHub
# from transformers import AutoModelForCausalLM

def get_pdf_text(pdf_docs):
  text = ""
  try:
    for pdf in pdf_docs:
      pdf_reader = PdfReader(pdf)  
      for page in pdf_reader.pages:
        text += page.extract_text()
  except Exception as e:
    print(f"Error extracting text from PDF: {e}")
    text = ""

  return text

def get_text_chunks(text):
    try:  
    # existing splitting logic
      text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
      chunks = text_splitter.split_text(text)
    except Exception as e:
         print(f"Error splitting text: {e}")
         return []

    return chunks

def get_vectorstore(text_chunks):
    vectorstore = []
    vectorstore.clear()
    try:
        # embeddings = OpenAIEmbeddings()
        embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        print(type(vectorstore))
    except Exception as e:
        print(f"Error creating vectorstore: {e}")
        print(type(vectorstore))
        return None
    return vectorstore

def get_conversation_chain(vectorstore):
    # llm = ChatGooglePalm()
    llm = HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature":0.5, "max_length":512,})
    #llm = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history'][::-1]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

           

def main():
    load_dotenv()
    st.set_page_config(page_title="Artie the PDFphile", page_icon=":books:") 
    st.write(css, unsafe_allow_html=True)  

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs 🕮")
    st.caption("Which you can't do with girls when you have a girlfriend 💀")
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on Start Chat", accept_multiple_files=True)
        if st.button("Start Chat"):
            with st.spinner("Processing"):
                if pdf_docs: 
                    # get pdf text
                    raw_text = get_pdf_text(pdf_docs)

                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create vector store
                    vectorstore = get_vectorstore(text_chunks)
                    if vectorstore is None:
                        st.error("Error processing PDFs. Please check files.")
                        return

                    st.success("PDFs uploaded successfully!")
                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(
                        vectorstore)
                    
                    pdf_docs.clear()

                else:
                    st.error("Please upload your PDFs")
        st.divider()
        st.write('*Guess who\'s gonna play with your PDF files.*')
        st.caption('''**<p style ='color:white'>Artie fell from the sky when the same intern was too lazy to read research papers which were provided by his manager. 
               His laziness can be shown through Artie's performance. He did watch the full tutorial for this one. 
               And now he has upload Artie to Github as a proof that he can do something . <p style ='color:#85D17B'>If you are a recruiter <br>"Please....I can do better" <br> &nbsp;- The intern</p></p>**
    ''',unsafe_allow_html=True)
        st.caption("<p style ='color:white'>Artie is usnig <b>HuggingFaceHub API</b> for this purpose. If you ever feel like forking or cloning this project <p style ='color:white'>(First of all: WHY ?)</p><p style ='color:white'> Please use your own API key</p></p>", unsafe_allow_html=True)


    user_question = st.text_input("Ask any questions related to the PDF. PS: They don't get offended 😂")
    
    if st.button("Submit Question", key="submit_button"):
        handle_userinput(user_question)










if __name__ == '__main__':
    main()