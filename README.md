# Talk-To-Database

This is an end to end LLM project based on Google Gemini and Langchain. We are building a system that can talk to MySQL database. 
User asks questions in a natural language and the system generates answers by converting those questions to an SQL query and
then executing that query on MySQL database. 
AtliQ Tees is a T-shirt store where they maintain their inventory, sales and discounts data in MySQL database. A store manager 
will may ask questions such as,
- How many white color Adidas t shirts do we have left in the stock?
- How much sales our store will generate if we can sell all extra-small size t shirts after applying discounts?
The system is intelligent enough to generate accurate queries for given question and execute them on MySQL database

## Project Highlights

- AtliQ Tees is a t shirt store that sells Adidas, Nike, Van Heusen and Levi's t shirts 
- Their inventory, sales and discounts data is stored in a MySQL database
- We will build an LLM based question and answer system that will use following,
  - Google Palm LLM
  - Hugging face embeddings
  - Streamlit for UI
  - Langchain framework
  - Chromadb as a vector store
  - Few shot learning
- In the UI, store manager will ask questions in a natural language and it will produce the answers

## Installation

1  pip install -r requirements.txt

2.Acquire an api key through makersuite.google.com and put it in .env file
  GOOGLE_API_KEY="your_api_key_here"
  
3. For database setup, run database/db_creation_atliq_t_shirts.sql in your MySQL workbench

## Usage

1. Run the Streamlit app by executing:
streamlit run webprj.py

2.The web app will open in your browser where you can ask questions

## Sample Questions
  - How many total t shirts are left in total in stock?
  - How many t-shirts do we have left for Nike in XS size and white color?
  - How much is the total price of the inventory for all S-size t-shirts?
  - How much sales amount will be generated if we sell all small size adidas shirts today after discounts?
  
## Project Structure

- webprj.py: The main Streamlit application script and  has all the langchain code
- requirements.txt: A list of required Python packages for the project.
- few_shots.py: Contains few shot prompts
- .env: Configuration file for storing your Google API key.
