import os
os.environ["USER_AGENT"] = "myagent"

from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()








# llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)


# # Recherche Web
# search = TavilySearchResults()


# # Recherche locale
# loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
# docs = loader.load()
# documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
# vector_db = FAISS.from_documents(documents, OpenAIEmbeddings())

# retriever_tool = create_retriever_tool(
#     vector_db.as_retriever(),
#     "langsmith_search",
#     "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
# )



# tools = [search, retriever_tool]




# # Get the prompt to use - you can modify this!
# prompt = hub.pull("hwchase17/openai-functions-agent")
# prompt.messages

# # [SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template='You are a helpful assistant')),
# #  MessagesPlaceholder(variable_name='chat_history', optional=True),
# #  HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')),
# #  MessagesPlaceholder(variable_name='agent_scratchpad')]





# from langchain.agents import create_tool_calling_agent, AgentExecutor

# agent = create_tool_calling_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# agent_executor.invoke({"input": "hi!"})










from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_experimental.tools import PythonREPLTool

tools = [PythonREPLTool()]

instructions = """You are an agent designed to write and execute python code to answer questions.
You have access to a python REPL, which you can use to execute python code. If you get an error, debug your code and try again.
Only use the output of your code to answer the question. You might know the answer without running any code, but you should still run the code to get the answer.
If it does not seem like you can write code to answer the question, just return "I can't use code to answer" as the answer.
"""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

agent = create_openai_functions_agent(llm, tools, prompt)



agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke({"input": "What is the sum of the 20th and the 21th fibonacci numbers?"})

# agent_executor.invoke({"input": """Understand, write a single neuron neural network in PyTorch.
#     Take synthetic data for y=2x. Train for 1000 epochs and print every 100 epochs.
#     Return prediction for x = 5"""}
# )