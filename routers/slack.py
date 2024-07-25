# routers/slack.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Request, Depends
from sqlalchemy.orm import Session
import db_module.db_config as db_config
from db_module.db_config import get_db
from db_module.models import SlackMessage, Messages
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, timedelta
from typing import List
from settings import SLACK_TOKEN, HOURS_TO_LAST_MESSAGE

# Create a new router instance
router = APIRouter()

# Initialize Slack client
client = WebClient(token=SLACK_TOKEN)

# Store active WebSocket connections
active_connections: List[WebSocket] = []

def get_username(user_id: str) -> str:
    try:
        response = client.users_info(user=user_id)
        user_info = response['user']
        return user_info['name']  # Or user_info['real_name'] if you prefer
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")
        return None

# Add routes to the router
@router.post("/send-message/")
async def send_message(slack_message: SlackMessage, db: Session = Depends(get_db)):
    try:
        # Calculate the timestamp for 6 hours ago
        hours_ago = datetime.utcnow() - timedelta(hours=HOURS_TO_LAST_MESSAGE)

        # Query for the most recent thread by this user within the last 6 hours
        recent_message = db.query(Messages).filter(
            Messages.user == slack_message.id,
            Messages.created_at >= hours_ago
        ).order_by(Messages.created_at.desc()).first()

        # Determine if we're replying to an existing thread or starting a new one
        if recent_message:
            # If a recent thread exists, send a message to that thread
            response = client.chat_postMessage(
                channel=slack_message.channel,
                text=slack_message.message,
                thread_ts=recent_message.thread_ts
            )
        else:
            # If no recent thread, post a new message to create a new thread
            response = client.chat_postMessage(
                channel=slack_message.channel,
                text=f"MENSAJE DE [{slack_message.username}] CON EL CORREO [{slack_message.email}] Y EL ID [{slack_message.id}] : {slack_message.message}"
            )

        # Add message to the database
        new_message = Messages(
            id=response['ts'],
            thread_ts=response['ts'] if not recent_message else recent_message.thread_ts,
            user=slack_message.id,
            text=slack_message.message
        )
        db.add(new_message)
        db.commit()

        # Broadcast new message to all connected clients
        await broadcast_message({"text": slack_message.message, "user": slack_message.id})

        return {"ok": response["ok"], "message": "Message sent successfully!"}
    except SlackApiError as e:
        # Handle Slack API errors
        raise HTTPException(status_code=400, detail=f"Slack API error: {e.response['error']}")

async def broadcast_message(message: dict):
    """Send message to all active WebSocket connections."""
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except WebSocketDisconnect:
            active_connections.remove(connection)

ctive_connections = []

@router.websocket("/ws/responses/{user_id}")
async def websocket_responses(websocket: WebSocket, user_id: str, db: Session = Depends(get_db)):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        # Initially send all messages for the user
        messages = db.query(Messages).filter(Messages.user == user_id).order_by(Messages.created_at.desc()).all()

        if messages:
            thread_ts = messages[0].thread_ts
            messages_in_thread = db.query(Messages).filter(Messages.thread_ts == thread_ts).all()

            # Convert datetime to string
            serialized_results = [
                {
                    "id": message.id,
                    "thread_ts": message.thread_ts,
                    "user": message.user,
                    "text": message.text,
                    "created_at": message.created_at.isoformat() if message.created_at else None
                }
                for message in messages_in_thread
            ]

            # Send initial responses to the WebSocket client
            await websocket.send_json({"responses": serialized_results})
        else:
            await websocket.send_json({"responses": []})

        # Keep the connection open and wait for disconnection
        while True:
            # Handle incoming messages if needed (for future extension)
            await websocket.receive_text()

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Client disconnected")

@router.post("/slack/events/")
async def handle_slack_event(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    if body.get("type") == "url_verification":
        # Respond with the challenge value
        return {"challenge": body["challenge"]}
    if body.get("event"):
        event = body["event"]

        # Ensure we're only processing message events and not from bots
        if event.get("type") == "message" and not event.get("bot_id"):
            # Check if it is a reply to a thread
            if "thread_ts" in event:
                # Check if the thread_ts is already in the database
                existing_thread = db.query(Messages).filter(Messages.thread_ts == event["thread_ts"]).first()

                if existing_thread:
                    # Insert the new response if the thread_ts exists
                    username = get_username(event["user"])
                    new_message = Messages(
                        id=event["ts"],
                        thread_ts=event["thread_ts"],
                        user=username,
                        text=event["text"]
                    )
                    db.add(new_message)
                    db.commit()

                    # Broadcast the new message to all WebSocket clients
                    await broadcast_message({"text": event["text"], "user": event["user"]})
                    return {"ok": True}
                else:
                    # Handle cases where the thread_ts doesn't exist
                    print("Thread not found in database")
            else:
                # Handle cases where there's no thread_ts
                print("No thread_ts found in event")

    return {"ok": False}