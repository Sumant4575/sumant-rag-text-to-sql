import os
from typing import Any, Awaitable 
import streamlit as st
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    insert
)
from llama_index.core import SQLDatabase, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.core.workflow import Workflow, step, Event, StartEvent, StopEvent

# Set up OpenAI API key and Phoenix API key
os.environ["OPENAI_API_KEY"] = "Add here your openai_api_key"
PHOENIX_API_KEY = "Add phoenix_api_key here"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}"

# Streamlit app setup
st.title("City Statistics Query Application")

# Set up the database and the table
Settings.llm = OpenAI("gpt-3.5-turbo")
engine = create_engine("sqlite:///:memory:", future=True)
metadata_obj = MetaData()

# Create city SQL table
city_stats_table = Table(
    "city_stats",
    metadata_obj,
    Column("city_name", String(16), primary_key=True),
    Column("population", Integer),
    Column("state", String(16), nullable=False),
)

metadata_obj.create_all(engine)

# Insert data into the table
rows = [
    {"city_name": "New York City", "population": 8336000, "state": "New York"},
    {"city_name": "Los Angeles", "population": 3822000, "state": "California"},
    {"city_name": "Chicago", "population": 2665000, "state": "Illinois"},
    {"city_name": "Houston", "population": 2303000, "state": "Texas"},
    {"city_name": "Miami", "population": 449514, "state": "Florida"},
    {"city_name": "Seattle", "population": 749256, "state": "Washington"},
]

with engine.begin() as connection:
    for row in rows:
        stmt = insert(city_stats_table).values(**row)
        connection.execute(stmt)

# Initialize LlamaIndex tools
sql_database = SQLDatabase(engine, include_tables=["city_stats"])
sql_query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["city_stats"],
    embed_model=OpenAIEmbedding()
)

index = LlamaCloudIndex(
    name="rag_sql",
    project_name="llamacloud_demo",
    organization_id="07cff857-92f7-49cb-8716-46b683b8d997",
    api_key="Add here llama_index_api_key"
)
llama_cloud_query_engine = index.as_query_engine()

sql_tool = QueryEngineTool.from_defaults(
    query_engine=sql_query_engine,
    description=(
        "Useful for translating a natural language query into a SQL query over"
        " a table containing: city_stats, containing the population/state of"
        " each city located in the USA."
    ),
    name="sql_tool"
)

llama_cloud_tool = QueryEngineTool.from_defaults(
    query_engine=llama_cloud_query_engine,
    description=(
        f"Useful for answering semantic questions about certain cities in the US."
    ),
    name="llama_cloud_tool"
)

# Router workflow
class InputEvent(Event):
    """Input event."""

class RouterOutputAgentWorkflow(Workflow):
    """Custom router output agent workflow."""

    def __init__(self, tools, llm, chat_history=None):
        super().__init__(timeout=120, verbose=True)
        self.tools = tools
        self.llm = llm
        self.chat_history = chat_history or []

    @step()
    async def prepare_chat(self, ev: StartEvent):
        message = ev.get("message")
        self.chat_history.append(message)
        return InputEvent()

    @step()
    async def chat(self, ev: InputEvent):
        result = await self.llm.achat_with_tools(self.tools, self.chat_history)
        return StopEvent(result=result.message)

wf = RouterOutputAgentWorkflow(
    tools=[sql_tool, llama_cloud_tool],
    llm=OpenAI(temperature=0, model="gpt-3.5-turbo")
)

# Streamlit interface for user input
user_query = st.text_input("Ask a question about cities in the USA:")
if st.button("Submit"):
    result = wf.run(message=user_query)
    st.markdown(result)
