# chatbot-app
## Task for AI Chatbot for the ifood data customers dataset
### The application utilises langchain's pandas dataframe agents and the Open AI gpt-3.5 and gpt-4 models to enable users to query the chatbot with questions about the given customers dataset. It provides a simple streamlit browser based UI.

#### Instructions to run:
1. Ensure that you are have python version 3.9 or 3.10 as well as pip installed (NOTICE: python 3.11+ may produce some library incompatibilities when installing the required libraries).
2. Install the necessary python packages by running `pip install -r ./requirements.txt` or `pip install langchain streamlit openai tabulate python-dotenv pandas`.
3. Run the application by running `streamlit run main.py` in the console.
4. After runninng the command a new browser tab will open with the chatbot. If it does not automatically open, you can access it at [http://172.20.10.6:8501]
5. Choose your preferred GPT model using the radio buttons (you can change whenever you like).
6. Ask your questions! NB! For more complex questions consider selecting the GPT-4 model, since it is more accurate (however slightly slower and more expensive).

#### Images:
App's UI: 
![alt text](https://github.com/aleksandar-ruskov/chatbot-app/blob/main/screenshots/app-screenshot-1.png "Apps UI")

Asking Questions 1:
![alt text](https://github.com/aleksandar-ruskov/chatbot-app/blob/main/screenshots/app-screenshot-2.png "Asking questions 1")

Asking Questions 2:
![alt text](https://github.com/aleksandar-ruskov/chatbot-app/blob/main/screenshots/app-screenshot-3.png "Asking questions 2")

Asking Questions 3:
![alt text](https://github.com/aleksandar-ruskov/chatbot-app/blob/main/screenshots/app-screenshot-4.png "Asking questions 3")
