To run this application you need to: 

## setup
1. create a free Pinecone account: https://www.pinecone.io/
2. create an OpenAI premium account and add a small of amount of credits (like $5) to a project in: https://platform.openai.com/
3. create and save you API Keys for Pinecone and ChatGPT
4. have **python3** with **pip** installed
5. clone the repo
6. create a `.env` file in the project to store your environment variables

**ENV File:** <br>
```
OPENAI_API_KEY=<your API Key> 
INDEX_NAME=<name-you-database>
PINECONE_API_KEY=<your API Key>
PINECONE_ENVIRONMENT=us-east-1-aws
```

## run app:
1. navigate to the project in your terminal
2. run command: `pip install requirements.txt`
3. to run in a virtual environement (venv)
   run command:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Build your Pinecone Vector DB with a new Index
   open `ingestion.py` and run in your editor, or run command: `python ingestion.py`
5. Run the chatbot
      open `stateful-bot.py` and run in your editor, or run command: `python stateful-bot.py`


   
