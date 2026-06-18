from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

# Import modules
from resume_parser import parse_resume
from skill_extractor import extract_details_from_resume
from role_matcher import match_skills
from chatbot import get_chatbot_response
from rag_pipeline import init_rag_pipeline

app = FastAPI(title="AI Resume Analyzer & Career Assistant")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple in-memory storage to simulate sessions for the college project
session_data = {
    "extracted_details": {},
    "analysis_results": []
}

# Initialize RAG on startup
@app.on_event("startup")
async def startup_event():
    try:
        init_rag_pipeline()
        print("RAG pipeline initialized successfully.")
    except Exception as e:
        print(f"Warning: RAG initialization failed (Check API keys): {e}")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = parse_resume(contents, file.filename)
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from file.")
        
        return {"message": "Resume uploaded and parsed successfully", "text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AnalyzeRequest(BaseModel):
    resume_text: str

@app.post("/analyze-resume")
async def analyze_resume(request: AnalyzeRequest):
    try:
        # 1. Extract Details
        details = extract_details_from_resume(request.resume_text)
        session_data["extracted_details"] = details
        
        # 2. Match Skills
        skills = details.get("skills", [])
        recommendations = match_skills(skills)
        session_data["analysis_results"] = recommendations
        
        return {
            "message": "Analysis complete",
            "details": details,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommended-roles")
async def get_recommended_roles():
    return {"recommendations": session_data.get("analysis_results", [])}

@app.get("/skill-gap-analysis")
async def get_skill_gap_analysis():
    # Return missing skills for the top recommendation
    results = session_data.get("analysis_results", [])
    if results:
        top_role = results[0]
        return {
            "role": top_role["role"],
            "current_skills": session_data["extracted_details"].get("skills", []),
            "missing_skills": top_role["missing_skills"]
        }
    return {"message": "No analysis available"}

@app.get("/career-roadmap")
async def get_career_roadmap():
    results = session_data.get("analysis_results", [])
    if results:
        top_role = results[0]["role"]
        # Use RAG to fetch a roadmap for the top role
        prompt = f"What is the learning roadmap to become a {top_role}?"
        roadmap = get_chatbot_response(prompt)
        return {"role": top_role, "roadmap": roadmap}
    return {"message": "No analysis available"}

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_assistant(request: ChatRequest):
    try:
        response = get_chatbot_response(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
