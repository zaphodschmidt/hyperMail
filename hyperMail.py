import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from IPython.display import Image, display

load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

os.environ['OPEN_AI_API_KEY'] = OPEN_AI_API_KEY
os.environ['LANGCHAIN_TRACING_V2'] = LANGCHAIN_TRACING_V2
os.environ['LANGCHAIN_ENDPOINT'] = LANGCHAIN_ENDPOINT
os.environ['LANGCHAIN_API_KEY'] = LANGCHAIN_API_KEY
os.environ['LANGCHAIN_PROJECT'] = LANGCHAIN_PROJECT

llm = ChatOpenAI(api_key=OPEN_AI_API_KEY, model="gpt-4o")
class State(TypedDict):
    messages:Annotated[list, add_messages]

graphBuilder = StateGraph(State)

def chatbot(state:State):
    return {'messages': llm.invoke(state['messages'])} 

graphBuilder.add_node("chatbot", chatbot)
graphBuilder.add_edge(START, "chatbot")
graphBuilder.add_edge("chatbot" , END)

graph = graphBuilder.compile()

def streamGraphUpdates(userInput: str):
    for event in graph.stream({"messages": [("user", userInput)]}):
        for value in event.values():
            # print(type(value["messages"]))
            # print(dir(value["messages"]))
            # print(type(value["messages"][-1]))
            # print(dir(value["messages"][-1]))
            print("Assistant:", value["messages"].content)
            print("Assistant:", value)
            print("Assistant:", event)
            # print("Assistant:", value["messages"][-1].content)

while True:
    try:
        userInput = input("User: ")
        if userInput.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        streamGraphUpdates(userInput)
    except:
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        streamGraphUpdates(user_input)
        break