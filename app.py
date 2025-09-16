# app.py
import chainlit as cl
from dvnc_system import DVNCSystem
import asyncio

# Initialize the DVNC system
dvnc = DVNCSystem()

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    # Store the DVNC system in user session
    cl.user_session.set("dvnc_system", dvnc)
    
    # Send welcome message with animation
    await cl.Message(
        content="",
        elements=[
            cl.Text(
                name="welcome",
                content="🎨 **Welcome to DVNC.ai** - Leonardo's Intelligence Reimagined\n\n"
                       "I combine insights from Physics, Biomechanics, and Anatomy to help you "
                       "innovate like Leonardo da Vinci. Share your engineering challenge!",
                display="inline"
            )
        ]
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    # Get DVNC system from session
    dvnc_system = cl.user_session.get("dvnc_system")
    
    # Show thinking indicator
    msg = cl.Message(content="")
    await msg.send()
    
    # Simulate processing with streaming
    async with cl.Step(name="🧠 Analyzing with Da Vinci's Methods") as step:
        step.input = message.content
        
        # Process through DVNC
        await cl.sleep(0.5)  # Small delay for effect
        analysis = dvnc_system.analyze_prompt(message.content)
        
        # Show keywords found
        keywords_str = "\n".join([f"- {d}: {', '.join(kw) if kw else 'general principles'}" 
                                 for d, kw in analysis['keywords'].items()])
        step.output = f"**Detected Concepts:**\n{keywords_str}"
    
    # Stream the response
    response_parts = analysis['synthesis'].split('\n')
    full_response = ""
    
    for part in response_parts:
        if part:  # Skip empty lines for streaming
            full_response += part + "\n"
            await msg.stream_token(part + "\n")
            await asyncio.sleep(0.05)  # Streaming effect
    
    await msg.update()

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    """Optional authentication"""
    # Remove this decorator if you don't want authentication
    # For demo, accept any username/password
    return cl.User(identifier=username)