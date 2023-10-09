import streamlit as st

from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType

from dotenv import load_dotenv

def main():
    load_dotenv()

    st.set_page_config(page_title='Ask me a question about the csv')
    st.header('Ask me a question about the data CSV')

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    

    user_question = st.chat_input('Ask a question about your CSV: ')

    agent = create_csv_agent( llm=OpenAI(temperature=0), 
                              path=['./data/data_csv.csv', 
                              './data/dictionary.csv'], 
                              verbose=True,  
                              agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                            )

    if user_question is not None and user_question != "":
        
        with st.chat_message("user"):
            st.markdown(user_question)

        st.session_state.messages.append({"role": "user", "content": user_question})

        placeholder = st.empty()
        
        with placeholder.container():
            with st.chat_message("assistant"):
                st.markdown('Thinking...')

        response = agent.run(user_question)
        placeholder.empty()
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()