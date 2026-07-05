from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sqlite3
import pandas as pd

from google.genai import types
from google.adk.runners import InMemoryRunner

# Import the existing ADK App without modifying it
from app.agent import app as adk_app

app = FastAPI(title="VanillaForge Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vanillaforge_memory.db")

@app.get("/api/data/chart")
async def get_chart_data(ticker: str):
    """Reads the Parquet file and returns JSON data for Apache ECharts."""
    parquet_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data_temp", ticker, f"{ticker}_history.parquet")
    if not os.path.exists(parquet_path):
        return {"error": f"No data found for {ticker}."}
    
    try:
        df = pd.read_parquet(parquet_path)
        if df.index.name == 'Date' or isinstance(df.index, pd.DatetimeIndex):
            df = df.reset_index()
        
        if 'Date' in df.columns:
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            
        return {"ticker": ticker, "data": df.to_dict(orient='records')}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/mcp/journal")
async def get_journal_data(type: str = "trade"):
    """Reads from the local SQLite MCP database."""
    if not os.path.exists(DB_PATH):
        return {"error": "Database not initialized yet."}
        
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Determine table name based on type
        table_name = "trade_journal" if type == "trade" else "sentiment_history" if type == "sentiment" else None
        if not table_name:
            return {"error": "Invalid journal type"}
            
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY timestamp DESC")
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {"type": type, "data": data}
    except Exception as e:
        return {"error": str(e)}

# Setup the ADK runner
runner = InMemoryRunner(app=adk_app)

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Create a new session for this connection
    session = await runner.session_service.create_session(
        app_name=adk_app.name, user_id="dashboard_user"
    )
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            prompt = payload.get("prompt", "")
            
            if not prompt:
                continue
                
            try:
                # Run the ADK graph asynchronously
                async for event in runner.run_async(
                    user_id="dashboard_user",
                    session_id=session.id,
                    new_message=types.Content(
                        role="user", parts=[types.Part.from_text(text=prompt)]
                    ),
                ):
                    # We look for text updates to stream back
                    # The graph emits various events. We look for the model's text response.
                    # This logic mimics what `agents-cli run` does to extract text.
                    if hasattr(event, "content") and event.content:
                        parts = getattr(event.content, "parts", [])
                        for part in parts:
                            if hasattr(part, "text") and part.text:
                                await websocket.send_text(json.dumps({
                                    "type": "chunk", 
                                    "content": part.text
                                }))
                
                # Signal the frontend that the response is complete
                await websocket.send_text(json.dumps({"type": "done"}))
                
            except Exception as e:
                await websocket.send_text(json.dumps({"type": "error", "content": str(e)}))
                
    except WebSocketDisconnect:
        print(f"Client session {session.id} disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
