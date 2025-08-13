from flask import Blueprint, request, jsonify
from sqlalchemy import select

from ..db import session_scope
from ..models import Agent

bp = Blueprint("agents", __name__)


@bp.get("/rooms/<int:room_id>/agents")
def list_agents(room_id: int):
    with session_scope() as s:
        agents = s.scalars(select(Agent).where(Agent.room_id == room_id)).all()
        return jsonify([
            {
                "id": a.id,
                "room_id": a.room_id,
                "name": a.name,
                "model": a.model,
                "temperature": a.temperature,
                "is_active": a.is_active,
            }
            for a in agents
        ])


@bp.post("/rooms/<int:room_id>/agents")
def create_agent(room_id: int):
    data = request.get_json() or {}
    name = data.get("name", "Agent")
    model = data.get("model", "gpt-4o-mini")
    temperature = float(data.get("temperature", 0.7))
    system_prompt = data.get("system_prompt", "You are a helpful AI.")

    with session_scope() as s:
        agent = Agent(
            room_id=room_id,
            name=name,
            model=model,
            temperature=temperature,
            system_prompt=system_prompt,
        )
        s.add(agent)
        s.flush()
        return jsonify({
            "id": agent.id,
            "room_id": agent.room_id,
            "name": agent.name,
            "model": agent.model,
            "temperature": agent.temperature,
            "is_active": agent.is_active,
        })