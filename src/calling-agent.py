from agno.agent import Agent  # noqa
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.google import GeminiEmbedder
from pathlib import Path
from agno.knowledge.text import TextKnowledgeBase
from agno.playground import Playground, serve_playground_app


# Initialize the TextKB
knowledge_base = TextKnowledgeBase(
    path=Path("../knowledge/"),
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="recipes",
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="models/embedding-001"),
    ),
    num_documents=5,
)
# Load the knowledge base
knowledge_base.load(recreate=False)

# Initialize agent with knowledge base directly
agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    markdown=True,
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    knowledge=knowledge_base  # Use kb parameter instead of knowledge_base
)

# Ask a question using the knowledge base

# agent.print_response("What is the recipe for a chocolate cake?", markdown=True)


app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)