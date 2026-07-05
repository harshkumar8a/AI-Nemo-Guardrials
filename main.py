import os
import re
from typing import TypedDict, Literal
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from nemoguardrails import RailsConfig, LLMRails
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from nemoguardrails.llm.providers import register_llm_provider
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
load_dotenv()

# Using the groq api key from the .env file
groq_api_key = os.getenv("GROQ_API_KEY")

# Here, I am using the groq model is llama-3.1-8b-instant
llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    api_key = groq_api_key,
    temperature = 0.5
)

# Initialize Guardrails once
config = RailsConfig.from_path("./guardrails_config")
rails = LLMRails(config,llm=llm)

# State
class AgentState(TypedDict):
    user_input: str
    extracted_expression: str
    response: str
    status: Literal["processing", "blocked", "completed"]


# Input Guardrail Validation
async def input_guardrail_node(state: AgentState) -> dict:
    try:
        # Run user input through NeMo Guardrails
        result = await rails.generate_async(
            messages=[{"role": "user", "content": state["user_input"]}]
        )
        bot_response = result.get("content", "")
        
        # explicit guardrail rejections
        if "specialized math assistant" in bot_response:
            return {"response": bot_response, "status": "blocked"}
            
        # Groq completely ignores rules and answers the question anyway
        # If the response contains conversational text and no numbers/operators, block it.
        cleaned_check = "".join(ch for ch in state["user_input"] if ch in "0123456789+-*/(). ")
        if not cleaned_check.strip():
            return {
                "response": "I am a specialized math assistant. Please provide a mathematical calculation.",
                "status": "blocked"
            }
            
        return {"status": "processing"}
    except Exception as e:
        return {"response": f"Safety verification failed: {str(e)}", "status": "blocked"}


# Calculation Engine 
async def calculation_node(state: AgentState) -> dict:
    # Skip processing if previously blocked by input rails
    if state["status"] == "blocked":
        return {}
        
    user_query = state["user_input"]
    
    # Strip basic math characters to parse the equation out of potential text
    cleaned_expression = "".join(ch for ch in user_query if ch in "0123456789+-*/(). ")
    cleaned_expression = cleaned_expression.strip()
    
    if not cleaned_expression:
        return {
            "response": "Could not extract a valid mathematical expression to calculate.",
            "status": "blocked"
        }
        
    try:
        # Use a restrictive regex validation to completely block malicious string executions
        if not re.match(r"^[\d\s\+\-\*\/\(\)\.]+$", cleaned_expression):
            raise ValueError("Unsafe characters detected.")
            
        # Safely evaluate the basic string arithmetic
        result = eval(cleaned_expression, {"__builtins__": None}, {})
        
        return {
            "extracted_expression": cleaned_expression,
            "response": f"The result of {cleaned_expression} is {result}.",
            "status": "completed"
        }
    except ZeroDivisionError:
        return {"response": "Error: Division by zero is undefined.", "status": "completed"}
    except Exception:
        return {"response": "Sorry, I couldn't compute that mathematical formula.", "status": "blocked"}


# LangGraph Pipeline
workflow = StateGraph(AgentState)

workflow.add_node("input_guardrail", input_guardrail_node)
workflow.add_node("calculation_engine", calculation_node)

# Route sequentially: Input Guardrail Check -> Calculation Processing
workflow.add_edge(START, "input_guardrail")
workflow.add_edge("input_guardrail", "calculation_engine")
workflow.add_edge("calculation_engine", END)

app_graph = workflow.compile()

# FastAPI Implementation
app = FastAPI(title="Secure Math Calculation Service")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    expression_processed: str | None
    reply: str
    status: str

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    # Serves the index.html landing page on base path visit
    return FileResponse("static/index.html")

@app.post("/calculate", response_model=ChatResponse)
async def calculate_endpoint(payload: ChatRequest):
    initial_state = {
        "user_input": payload.message,
        "extracted_expression": "",
        "response": "",
        "status": "processing"
    }
    
    final_output = await app_graph.ainvoke(initial_state)
    
    return ChatResponse(
        expression_processed=final_output.get("extracted_expression"),
        reply=final_output["response"],
        status=final_output["status"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
