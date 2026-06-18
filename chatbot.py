import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate   # FIX: was PromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from rag_pipeline import get_retriever
from dotenv import load_dotenv

load_dotenv()

def get_chatbot_response(user_message: str) -> str:
    """
    Takes a user message, retrieves relevant context from ChromaDB,
    and uses Groq to generate a grounded response.

    FIX: create_stuff_documents_chain requires a ChatPromptTemplate (not PromptTemplate).
    PromptTemplate produces a plain string prompt which the chain cannot correctly
    inject the retrieved documents into, causing a validation error at runtime.
    """
    load_dotenv(override=True)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return "System Error: Groq API Key is missing. Please configure the .env file."

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key,
        temperature=0.3
    )

    retriever = get_retriever()

    # FIX: Use ChatPromptTemplate.from_messages() instead of PromptTemplate().
    # create_stuff_documents_chain injects retrieved docs into {context},
    # and create_retrieval_chain injects the user question into {input}.
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "You are an expert AI Career Assistant helping students and professionals "
                "navigate the AI/ML landscape. Use the following retrieved context from our "
                "knowledge base to answer the user's question. If the answer is not in the "
                "context, do your best to answer based on general knowledge, but prioritize "
                "the retrieved context. Be encouraging, beginner-friendly, and concise.\n\n"
                "Context:\n{context}"
            )
        ),
        ("human", "{input}"),
    ])

    # Build the RAG chain
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

    try:
        response = rag_chain.invoke({"input": user_message})
        return response["answer"]
    except Exception as e:
     import traceback
     traceback.print_exc()
     return f"ERROR: {str(e)}"