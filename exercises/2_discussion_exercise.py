import asyncio
import sys
from pathlib import Path

from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework.orchestrations import GroupChatBuilder
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
from process_event_stream import process_event_stream

rounds_of_discussion = 2
load_dotenv()

# EXERCISES:
# a) Make the orchestrator follow the RULES of a good discussion moderator:
#   "RULES:\n"
#   "1. Rotate through ALL participants - do not favor any single participant\n"
#   "2. Each participant should speak at least once before any participant speaks twice\n"
#   "3. Continue for at least {rounds_of_discussion - 1} rounds before ending the discussion\n"
#   "4. Do NOT select the same participant twice in a row"
# b) Ask the team to solve the task: "Write code that calculates the pi number."
# c) Give the Coder space: remove the limitation of keeping it short. Observe the quality of the output.
# d) Create a "critic" agent and add it to the discussion. The critic should:
#       "Provide constructive feedback. "
#       "Do not be too strict. Keep your answers somewhat short.",

async def main_stream(task: str) -> None:

    client = AzureOpenAIResponsesClient()

    # Create the coding agent.
    primary = client.as_agent(
        name="Coder",
        instructions="You are a helpful AI assistant",
    )

    # Create the critic agent.
    critic = client.as_agent(
        name="Critic",
        instructions="Provide constructive feedback. Do not be too strict. Keep your answers somewhat short.",
    )

    # Create the orchestrator coordinating the discussion
    orchestrator = client.as_agent(
        name="orchestrator",
        instructions=("Rotate through ALL participants. Each participant must speak once before anyone speaks twice. Never select the same participant twice in a row unless they are the only one who has not spoken. Keep track of who has spoken in the current round. Continue round-robin order. \n\n"),
        )

    team = (
        GroupChatBuilder(
            participants=[primary, critic],
            max_rounds=rounds_of_discussion,
            orchestrator_agent=orchestrator,
        )
        .build()
    )

    stream = team.run(task, stream=True)
    
    pending_responses = await process_event_stream(stream)
    while pending_responses is not None:
        # Run the team until there is no more human feedback to provide,
        # in which case this team completes.
        stream = team.run(stream=True, responses=pending_responses)
        pending_responses = await process_event_stream(stream)


if __name__ == "__main__":
    print("Starting team discussion...")
    task = "Finn ut hvem som er kulest av fredrik Schmid Bjørge og Sondre Nodenes-Fimland, du skal velge ?"
    asyncio.run(main_stream(task))
