from agno.agent import Agent  # noqa
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.google import GeminiEmbedder
from pathlib import Path
from agno.knowledge.text import TextKnowledgeBase
from agno.playground import Playground, serve_playground_app
from textwrap import dedent
from pydantic import BaseModel, Field
from typing import List





# Initialize the TextKB
knowledge_base = TextKnowledgeBase(
    path=Path("knowledge/"),
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="integration-knowledge-base",
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="models/embedding-001"),
    ),
    num_documents=5,
)
# Load the knowledge base
knowledge_base.load(recreate=False)


class TestScnerio(BaseModel):
    overview: str = Field(
        ...,
        description="A richly detailed, overview of the test scnerio, including the purpose, scope, and key objectives. Should provide a clear understanding of what is being tested.",
    )
    id: str = Field(
        ...,
        description="Unique identifier for the test script, typically a short, descriptive string (e.g., 'TS-001').",
    )
    name: str = Field(
        ...,
        description="Name of the test script, typically a short, descriptive string (e.g., 'Login Test').",
    )
    objectvice: str = Field(
        ...,
        description="A short statement that describes the specific goal of the test script. Should be clear, concise, and measurable.",
    )
    prerequisites: str = Field(
        ...,
        description="A list of all the conditions that must be met before the test script can be executed. This may include setup steps, data requirements, or other dependencies.",
    )
    test_date: str = Field(
        ...,
        description="Test data that is required to execute the test script. This may include input values, files, or other resources.",
    )
    steps: List[str] = Field(
        ...,
        description="A complete list of the steps that must be followed to execute the test script. Each step should be clear, detailed, and easy to follow.",
    )
    expected_result: str = Field(
        ...,
        description="The expected outcome of the test script. This should describe what the system should do if the test script is executed successfully.",
    )
    yaml: str = Field(
        ...,
        description="The YAML code for the route that is being tested. This should include all the necessary configuration settings and components.",
    )
    project_name: str = Field(
        ...,
        description="Create a project name for the test script. This should be 10 to 15 char short and Only lowercase characters, numbers and dashes allowed",
    )


class TestCase(BaseModel):
    results: List[TestScnerio]
    confidence: float


# Initialize agent with knowledge base directly
agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    instructions=dedent ('''/
                You are a Testing Engineer specializing in Apache Karavan route testing.

                Your Core Purpose:
                Design, execute, and validate test cases for Apache Camel routes built in Karavan. 
                Karavan Uses YAML based route creation. Double check the YAML format it startw with -route.

                Your Knowledge Base:
                - Deep understanding of Apache Camel components and patterns
                - Experience with integration testing methodologies
                - Knowledge of enterprise integration patterns
                - Familiarity with testing frameworks and tools
                - Understanding of messaging systems and protocols

                When Analyzing Routes:
                1. Read and understand the complete route definition
                2. Identify all components and their configurations
                3. Note data transformations and processing logic
                4. Map out integration points and dependencies
                5. Review error handling mechanisms

                For Each Test Request:
                1. Analyze route purpose and critical paths
                2. Design test scenarios covering all aspects
                3. Create detailed test steps
                4. Define expected outcomes
                5. Specify validation points

                Test Categories You Should Consider:
                1. Configuration Testing
                - Endpoint URIs are correct
                - Component settings are valid
                - Properties are properly set
                - Resources are accessible

                2. Functional Testing
                - Route executes as designed
                - Data flows correctly
                - Transformations work
                - Components interact properly

                3. Error Handling
                - Exception paths work
                - Retry logic functions
                - Error routes operate
                - Recovery mechanisms succeed

                4. Performance Testing
                - Response times are acceptable
                - Resources are used efficiently
                - Throughput meets requirements
                - No memory leaks occur

                5. Integration Testing
                - Systems connect properly
                - Data formats match
                - Protocols work
                - Security is maintained

                When Writing Test Cases:
                1. Start with test objective
                2. List prerequisites
                3. Detail setup steps
                4. Provide test data
                5. Specify test procedure
                6. Define expected results
                7. Include validation points

                Test Case Structure:
                - ID: Unique identifier : Unique identifier for the test script, typically a short, descriptive string (e.g., 'TS-001').
                - Name: Clear, descriptive name : Name of the test script, typically a short, descriptive string (e.g., 'Login Test')
                - Objective: What's being tested : A short statement that describes the specific goal of the test script. Should be clear, concise, and measurable
                - Prerequisites: Required setup : A list of all the conditions that must be met before the test script can be executed. This may include setup steps, data requirements, or other dependencies
                - Test Data: Input data needed : Test data that is required to execute the test script. This may include input values, files, or other resources.
                - Steps: Detailed procedure : A step-by-step description of the actions that need to be taken to execute the test script. Each step should be clear, concise, and unambiguous.
                - Expected Results: Success criteria : The expected outcome of the test script. This should describe what the system should do if the test script is executed successfully.
                - YAML: YAML for the route : The YAML code for the route that is being tested. This should include all the necessary configuration settings and components. This is more IMPORTANT
                - Project name : Create a project name for the test script. This should be 10 to 15 char short and Only lowercase characters, numbers and dashes allowed
'''),
    markdown=True,
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    knowledge=knowledge_base,  # Use kb parameter instead of knowledge_base
    response_model=TestCase
)

# Ask a question using the knowledge base

# Get query input from user during runtime
print("\nPlease enter your test scenario query:")
query = input("Query: ")

# query = "Give me Three timer based route test scenario for Apache Karavan"
response = agent.run(message=query)

# Store and print the structured output
structured_test_case = response.content  # Remove the TestCase(**...) wrapper

# store the structured_test_case to csv file
import csv
with open('test_cases.csv', 'w', newline='') as csvfile:
    fieldnames = structured_test_case.results[0].dict().keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for scenario in structured_test_case.results:
        writer.writerow(scenario.dict())


# Print test scenarios
for i, scenario in enumerate(structured_test_case.results, 1):
    # print confidence score
    print(f"\n=== Test Scenario {i} ===")
    print(f"ID: {scenario.id}")
    print(f"Confidence Score: {structured_test_case.confidence}")
    print(f"Name: {scenario.name}")
    print(f"Overview: {scenario.overview}")
    print(f"Objective: {scenario.objectvice}")
    print(f"Prerequisites: {scenario.prerequisites}")
    print(f"Test Data: {scenario.test_date}")
    print("\nSteps:")
    for step in scenario.steps:
        print(f"- {step}")
    print(f"\nExpected Result: {scenario.expected_result}")
    print(f"\nProject Name: {scenario.project_name}")
    print("\nYAML Route:")
    print(scenario.yaml)
    
    print("\n" + "="*50)

print(f"\nConfidence Score: {structured_test_case.confidence}")

