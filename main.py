import streamlit as st

from langchain.agents import create_csv_agent, create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

from langchain.callbacks import get_openai_callback

import pandas as pd

from dotenv import load_dotenv

def initCsvAgent(): 
    customer_df = pd.read_csv("./data/data_csv.csv")

    dictionary = open("./data/dictionary.txt", "r").read()
    prefix = """You are working with a pandas dataframe in Python which contains data about store customers. The name of the dataframe is `df`.
            These are the the descriptions of the feaures used as column titles in the data frame: {dictionary}. The current date is 9/Oct/2023. You should use the tools below and the feature descriptions to answer the question posed of you"""


    agent = create_pandas_dataframe_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        df=customer_df,
        prefix=prefix,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    return agent

def setUpUI():
    st.set_page_config(page_title='Ask me a question about the csv')
    st.header('Ask me a question about the data CSV')

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


def queryOpenAI( agent, user_question ):
    with get_openai_callback() as cb:
            response = agent.run(user_question)
            print(f"Total tokens: {cb.total_tokens}")
            print(f"Total cost: {cb.total_cost}")
            return response
            


def handleUserInput(agent):
        # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    user_question = st.chat_input('Ask a question about your CSV: ')

    if user_question is not None and user_question != "":
        
        with st.chat_message("user"):
            st.markdown(user_question)

        st.session_state.messages.append({"role": "user", "content": user_question})

        placeholder = st.empty()
        
        with placeholder.container():
            with st.chat_message("assistant"):
                st.markdown('Thinking...')


        placeholder.empty()

        response = queryOpenAI(agent, user_question)
        
        with st.chat_message("assistant"):
            st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})
    

def main():
    load_dotenv()
    agent = initCsvAgent()
    setUpUI()
    handleUserInput(agent)
   

if __name__ == "__main__":
    main()