from backend.app.database import Base, engine

from backend.app.models.release import Release
from backend.app.models.case import TestCase
from backend.app.models.execution import TestExecution
from backend.app.models.defect import Defect
from backend.app.models.change import Change
from backend.app.models.agent_run import AgentRun
from backend.app.models.agent_tool_call import AgentToolCall


Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")