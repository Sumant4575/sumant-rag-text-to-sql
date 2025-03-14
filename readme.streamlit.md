README: City Statistics Query Application

A Streamlit-based interactive chatbot powered by LlamaIndex, OpenAI, and SQL that allows users to query city statistics using natural language. The application utilizes RAG (Retrieval-Augmented Generation) techniques, integrating SQL query processing with semantic search over city data

Features
•	✅ Natural Language Query to SQL: Converts user queries into SQL statements for city statistics.
•	✅ LlamaCloud Integration: Uses LlamaIndex for enhanced semantic search.
•	✅ Streamlit Interface: Simple UI for users to input questions.
•	✅ On-the-fly Database Creation: A temporary SQLite database is initialized in-memory.
•	✅ Workflow-based Routing: Implements a query-routing mechanism

Prerequisites
🔧 System Requirements
•	Python >= 3.8
•	An OpenAI API key (for GPT-3.5 Turbo)
•	A LlamaCloud API key
•	A Phoenix API key (for observability)
•	Internet connection (to fetch responses via APIs)
pip install -r requirements.txt

Set Up API Keys
export OPENAI_API_KEY="your-openai-key"
export LLAMA_CLOUD_API_KEY="your-llama-cloud-key"
export PHOENIX_API_KEY="your-phoenix-api-key"

Running the Application
Once installed and configured, run the Streamlit app
streamlit run app.py

Key Components & Code Structure
Component	Description
SQLDatabase	Connects SQLite to LlamaIndex
NLSQLTableQueryEngine	Converts natural language to SQL queries
LlamaCloudIndex	Enables semantic search over indexed city data
RouterOutputAgentWorkflow	Implements multi-tool query routing

Example Queries
•  What is the population of Los Angeles?" 
•  📍 "Which state is Miami located in?" 
•  🔍 "Tell me the population of all cities with more than 1 million people.
