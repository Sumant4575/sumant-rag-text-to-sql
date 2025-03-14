README
#  AI-Powered Query Interface: RAG + Text-to-SQL  

This repository implements an **AI-driven Query Interface** that combines **Retrieval-Augmented Generation (RAG) and Text-to-SQL** capabilities. Using **LlamaIndex, OpenAI, SQLAlchemy, and Arize Phoenix**, this system enables natural language queries over both structured SQL data and unstructured knowledge sources.  

## **🌟 Features**  
✅ **Text-to-SQL Querying**: Convert natural language into SQL queries for structured databases.  
✅ **Retrieval-Augmented Generation (RAG)**: AI-powered retrieval for answering unstructured questions.  
✅ **Dynamic Query Routing**: Automatically decides whether to use SQL-based retrieval or LLM-based retrieval.  
✅ **Logging & Observability**: Integrated with Arize Phoenix for monitoring AI model performance.  
✅ **Graph Visualization**: Visualizes the query execution flow using NetworkX and Matplotlib.  

---

## **🛠 Installation**  

To get started, clone this repository and install the required dependencies.  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/your_username/your_repository.git
cd your_repository

python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate  # On Windows


pip install -r requirements.txt

pip install llama-index llama-index-llms-openai llama-index-embeddings-openai
pip install llama-index-callbacks-arize-phoenix arize-phoenix
pip install llama-index-indices-managed-llama-cloud sqlalchemy networkx matplotlib


