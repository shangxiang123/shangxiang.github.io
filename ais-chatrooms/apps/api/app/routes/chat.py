import json
import time
from typing import Generator

from flask import Blueprint, Response, request, jsonify, current_app
from sqlalchemy import select

from ..config import Settings
from ..db import init_engine, session_scope
from ..models import Base, Room, Message

bp = Blueprint("chat", __name__)


@bp.before_app_request
def _init_db_if_needed():
    settings: Settings = current_app.config["SETTINGS"]
    init_engine(settings.DATABASE_URL)
    # Create tables if not exist (sqlite local convenience)
    if settings.DATABASE_URL.startswith("sqlite"):
        from sqlalchemy import create_engine as _ce
        engine = _ce(settings.DATABASE_URL)
        Base.metadata.create_all(engine)


@bp.post("/rooms")
def create_room():
    data = request.get_json() or {}
    name = data.get("name", "Demo Room")
    mode = data.get("mode", "manual")
    with session_scope() as s:
        room = Room(name=name, mode=mode)
        s.add(room)
        s.flush()
        s.commit()
        return jsonify({"id": room.id, "name": room.name, "mode": room.mode})


@bp.get("/rooms/<int:room_id>/messages")
def list_messages(room_id: int):
    with session_scope() as s:
        msgs = s.scalars(select(Message).where(Message.room_id == room_id).order_by(Message.created_at.asc())).all()
        return jsonify([
            {
                "id": m.id,
                "room_id": m.room_id,
                "sender_type": m.sender_type,
                "sender_id": m.sender_id,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in msgs
        ])


@bp.post("/rooms/<int:room_id>/messages")
def send_message(room_id: int):
    data = request.get_json() or {}
    content = data.get("content", "")
    with session_scope() as s:
        msg = Message(room_id=room_id, sender_type="human", sender_id=None, content=content)
        s.add(msg)
        s.flush()
    return jsonify({"status": "accepted", "message_id": msg.id})


@bp.get("/rooms/<int:room_id>/stream")
def stream_room(room_id: int):
    def event_stream() -> Generator[str, None, None]:
        # very basic demo: when client connects, emit a greeting and then echo small chunks
        greeting = "AI: Hello! This is a demo streaming response."
        for chunk in [greeting[i : i + 5] for i in range(0, len(greeting), 5)]:
            yield f"data: {json.dumps({'type': 'message.delta', 'delta': chunk})}\n\n"
            time.sleep(0.1)
        yield f"data: {json.dumps({'type': 'run.status', 'status': 'idle'})}\n\n"

    headers = {"Content-Type": "text/event-stream", "Cache-Control": "no-cache", "Connection": "keep-alive"}
    return Response(event_stream(), headers=headers)