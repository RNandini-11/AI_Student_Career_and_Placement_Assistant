import asyncio
import os
import sys

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from langchain_mcp_adapters.client import MultiServerMCPClient


# Load Environment Variables
load_dotenv()


# Create MCP Client
def create_mcp_client():
    client = MultiServerMCPClient({
            "career_tools": {
                "transport": "stdio",
                "command": sys.executable,  #Which Python am I using right now?
                "args": [
                    "-m",
                    "src.mcp_server"
                ]
            }
        })
    return client


# Create AI Agent
async def create_career_agent():
    # Create MCP client
    client = create_mcp_client()

    # Get tools from MCP server
    tools = await client.get_tools()

    # Create LLM
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    # Create Agent
    agent = create_agent(
        model=llm,
        tools=tools
    )
    return agent


# Ask Agent
async def ask_agent(question):
    agent = await create_career_agent()
    response = await agent.ainvoke({
            "messages": [{
                    "role": "user",
                    "content": question
                }]
        })
    return response


# Main
async def main():
    question = input("\nAsk your career question: ")
    response = await ask_agent(question)
    print("\nAI Career Assistant:")
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())