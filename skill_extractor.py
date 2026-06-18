import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

def extract_details_from_resume(resume_text: str) -> dict:
    """
    Uses Groq to extract Name, Email, Phone Number, Education, and Technical Skills
    from the raw resume text.
    """
    load_dotenv(override=True)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError("Please configure a valid GROQ_API_KEY in the .env file.")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key,
        temperature=0.0
    )

    prompt = PromptTemplate(
        input_variables=["resume_text"],
        template="""
        You are an expert HR AI Assistant. Extract the following details from the given resume text.
        Return ONLY a valid JSON object with the following keys and correct data types. Do not include markdown code blocks.

        Keys to extract:
        - name (string, if not found return "")
        - email (string, if not found return "")
        - phone (string, if not found return "")
        - education (list of strings, if not found return [])
        - skills (list of strings, focusing on technical skills like Python, Machine Learning, React, etc.)

        Resume Text:
        {resume_text}
        """
    )

    chain = prompt | llm
    
    try:
        response = chain.invoke({"resume_text": resume_text})
        # Clean up the response in case the LLM wrapped it in markdown
        output_text = response.content.strip()
        if output_text.startswith("```json"):
            output_text = output_text[7:-3]
        elif output_text.startswith("```"):
            output_text = output_text[3:-3]
            
        return json.loads(output_text.strip())
    except Exception as e:
        print(f"Error extracting details: {e}")
        # Return empty template on failure
        return {
            "name": "",
            "email": "",
            "phone": "",
            "education": [],
            "skills": []
        }
