from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.youtube import YouTubeTools

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[YouTubeTools()],
    show_tool_calls=True,
    description="You are a YouTube agent. Obtain the captions of a YouTube video and answer questions.",
)
agent.print_response(
    "Give me main points of this video https://www.youtube.com/watch?v=jCk3m4RA9ns", markdown=True
)