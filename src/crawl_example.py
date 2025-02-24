from agno.agent import Agent
from agno.tools.crawl4ai import Crawl4aiTools
from agno.models.google import Gemini   




agent = Agent( model=Gemini(id="gemini-2.0-flash-exp"),tools=[Crawl4aiTools(max_length=None)], show_tool_calls=True)
agent.print_response("Tell me about https://karavan.space/")