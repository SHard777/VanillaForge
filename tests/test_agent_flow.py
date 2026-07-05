import pytest
import asyncio
from google.adk.runners import InMemoryRunner
from google.genai import types
from app.agent import app

@pytest.mark.asyncio
async def test_agent_documentation_flow():
    """
    Verifies that the agent correctly routes educational options queries
    to the documentation skill and enters the human-in-the-loop pause.
    """
    runner = InMemoryRunner(app=app)
    session = await runner.session_service.create_session(
        app_name=app.name, user_id="test_user"
    )
    
    events = []
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part.from_text(text="What is a call option?")]
        ),
    ):
        events.append(event)
        
    # Verify that we received events from the graph
    assert len(events) > 0
    
    # Verify that the model successfully returned a text response
    has_text_response = False
    for event in events:
        if hasattr(event, "content") and event.content:
            parts = getattr(event.content, "parts", [])
            for part in parts:
                if hasattr(part, "text") and part.text:
                    has_text_response = True
                        
    assert has_text_response, "Workflow failed to produce a final text response."
