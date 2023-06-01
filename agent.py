import os

from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from api_key import ApiKey

os.environ["OPENAI_API_KEY"] = ApiKey.OPENAI_API_KEY
memory = ConversationBufferMemory()
llm = ChatOpenAI(model_name="gpt-4", temperature=0.2)
tools = load_tools([
    'python_repl',
], llm=llm)

agent = initialize_agent(
    llm=llm,
    tools=tools,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
)

agent.run("What's up ChatGPT?")
