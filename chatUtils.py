from langchain.agents import initialize_agent,AgentType
from langchain_community.llms.openai import OpenAI
from retriever_agent import policyRetriever
from agents.db_agent import queryDB
from langchain.memory import ConversationBufferMemory

tools=[policyRetriever,queryDB]
llm=OpenAI(api_key="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")

#Initialize Memory
memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)

agent_executor=initialize_agent(
    tools=tools,
    llm=llm,
    agent="conversational-react-description",
    handle_parsing_errors=True,
    verbose=True,
    memory=memory
)

def processPrompt(prompt:str):
    print(prompt)
    response=agent_executor.run(prompt)
    print("this is agent response",response)
    return response
