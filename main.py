import streamlit as st

from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

from langchain.callbacks import get_openai_callback

import pandas as pd

from dotenv import load_dotenv


# Function initialising the chatbot agent which will be used
# to 'talk to the csv'
# Takes the gptVersionSelection argument, which is the option selected by the user in the UI
# This will dictate if we use the GPT-3.5 or GPT-4 model for the LLM.
def initCsvAgent(gptVersionSelection): 
    # Read the Customers data csv and turn it into a Pandas 
    # dataframe which will be used by the agent to analyze during the prompts
    customer_df = pd.read_csv("./data/data_csv.csv")

    # Read the dictionary text file which contains the descriptions of the features in the dataframe
    dictionary = open("./data/dictionary.txt", "r").read()

    # Modify the default prefix and provide additional contex. That includes:
    # 1) Providing the dictionary of feature descriptions
    # 2) Providing the current date, in order to ensure that the model is up to date and can correctly
    #    answer questions which depend on the date (for instance anything related to customer age, etc.)
    prefix = """You are working with a pandas dataframe in Python which contains data about store customers. The name of the dataframe is `df`.
            These are the the descriptions of the feaures used as column titles in the data frame:""" + dictionary + """\nThe current date is 10/Oct/2023. You should use the tools below and the feature descriptions to answer the question posed of you:"""

    # Based on the user selection for model version define the model
    modelVersion = "gpt-3.5-turbo-0613"
    if(gptVersionSelection == "***GPT-4***"):
        modelVersion = "gpt-4"

    # Initialise the pandas dataframe agent with the given llm model version.
    # Here we have a few important details:
    #  1) We use the ChatOpenAI chat model instead of OpenAI, due to its incorporation of chat-related methods
    #     which provide the ability to make a chatbot more user-friendly
    #  2) We use OPENAI_FUNCTIONS agent type as it would perform better than the default ZERO_SHOT_REACT_DESCRIPTION
    #     agent type in detecting what pandas dataframe python functions should be called and with what inputs
    #     in order to analyze the data more accurately and provide better quality responses.
    agent = create_pandas_dataframe_agent(
        llm=ChatOpenAI(temperature=0, model=modelVersion),
        df=customer_df,
        prefix=prefix,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )  

    return agent

# Function which sets up the streamlit UI (header, chat area, input etc). 
# Also sets up the radio button which will allow the user to select the 
# gpt model they would prefer to use.
def setUpChatUIAndVersionSelect():
    st.set_page_config(page_title='Ask me a question about the Customers data csv')
    st.header('Hi, I am your Customers data chatbot.')
    st.subheader('Ask me a question about the Customers data CSV.')

    # Create the radiobutton which will be used to select the LLM model
    # Once that is set up return the current selection
    # This function is re-executed every time an interaction occurs, so if we select
    # a new option the reuturn value will contain the newly selected option.
    gptVersionSelection = st.radio(
    "Choose the GPT version to be used with the chat bot:",
    ["***GPT-3.5***", "***GPT-4***"],
    captions = ["Quicker and cheaper but less accurate. (Average prompt price: $0.005)", "Better accuracy but slower and more expensive. (Average prompt price: $0.09)"])

    # Initialize chat history if it has not been done yet which is stored in the streamlit session state
    # This will allow us to show the whole conversation in the UI and not only the
    # most recent interaction
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    return gptVersionSelection

# Query the Pandas open ai based Agent with the user's question and return the response
def queryOpenAI( agent, user_question ):
    with get_openai_callback() as cb:
        response = agent.run(user_question)
        print(f"Total tokens: {cb.total_tokens}")
        print(f"Total cost: {cb.total_cost}")
        return response
            

# Function handling the user's input question when it is submitted
def handleUserInput(agent):
    # Obtain the user's input
    user_question = st.chat_input('Ask a question about your CSV: ')

    if user_question is not None and user_question != "":
        
        # Display the new user message
        with st.chat_message("user"):
            st.markdown(user_question)

        # Add the new user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})

        # Create a placeholder while we wait for the agent's response and display it
        responseWaitPlaceholder = st.empty()
        with responseWaitPlaceholder.container():
            with st.chat_message("assistant"):
                st.markdown('Thinking...')

        # Query the agent and get its response
        response = queryOpenAI(agent, user_question)

        # Remove the placeholder when we have obtained the query's response
        responseWaitPlaceholder.empty()
        
        # Display the agent's response and store it in the chat history
        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    

def main():
    load_dotenv()
    gptVersionSelection = setUpChatUIAndVersionSelect()
    agent = initCsvAgent(gptVersionSelection)
    handleUserInput(agent)
   

if __name__ == "__main__":
    main()