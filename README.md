NLQ-to-SQL Query Generator
A Streamlit-based web app that converts natural language queries (NLQ) into SQL queries, powered by a background sql_agent.py script that leverages LangChain and an LLM for query generation. Inspired by ChatGPT, this app features chat history persistence, LLM-generated chat titles, and a user-friendly search interface, making it a unique blend of Gen AI and data analytics for my data analyst portfolio.
🚀 Project Overview
This app enables users to input natural language questions (e.g., "Show sales by region") and generates executable SQL queries via an LLM-driven agent defined in sql_agent.py. Built with Streamlit, SQLite, and LangChain, it offers a sidebar for chat management, dynamic title generation, and robust error handling. The project took ~2 months to develop, overcoming persistence and UI challenges, showcasing my ability to integrate Gen AI with analytics.
Features

NLQ-to-SQL Conversion: Converts natural language queries into SQL using an LLM-powered agent in sql_agent.py, which runs in the background for reasoning and query generation.
Chat History Persistence: Stores chats and messages in a SQLite database, ensuring conversations persist across sessions.
LLM-Generated Titles: Automatically generates chat titles (e.g., "Sales Query") via an LLM, defaulting to "Untitled Chat" for empty chats.
Sidebar Chat Management: Displays all chats in a sidebar, sorted by recency, with buttons to select and edit chat titles.
Search Functionality: Filters chats by title, showing "No chats found" for non-matching searches (triggered by Enter or a Search button).
Error Handling: Gracefully manages database and API errors for a stable user experience.

🛠️ Tech Stack

Python: Core programming language.
Streamlit: Web app framework for the UI.
SQLite: Lightweight database for chat and message storage.
LangChain: Powers NLQ-to-SQL conversion and LLM interactions in sql_agent.py.
OpenAI API: Used for title generation and SQL query generation (replaceable with other LLMs).
UUID: Generates unique IDs for chats and messages.

📂 Project Structure
├── app.py              # Main Streamlit app
├── sql_agent.py        # Background script for LLM-driven SQL query generation
├── conversations.db    # SQLite database for chats and messages
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation

🚧 Challenges Overcome

Chat History Persistence: Initially used JSON for storage, but scalability issues led to a switch to SQLite. This taught me schema design (CREATE TABLE, ALTER TABLE) and SQL queries (INSERT, SELECT ... LIKE).
ChatGPT-Like UI: Aimed for a sleek, ChatGPT-style interface but was limited by Streamlit’s capabilities. Focused on functionality (e.g., sidebar persistence, title generation) while keeping the UI clean.
LLM API Issues: The LLM API was unavailable at times, resulting in fallback titles like "Pending LLM Title." Implemented robust error handling in sql_agent.py and app.py.
Time Investment: Took ~2 months to pivot from a Docker-based chatbot to an NLQ-to-SQL generator, integrating sql_agent.py for LLM-driven query generation and learning SQLite/LangChain.

🎯 Why This Project?
Data analyst resumes often feature dashboards or Pandas projects. To stand out, I built an NLQ-to-SQL tool with Gen AI, showcasing:

SQL Skills: Schema management, queries (SELECT, UPDATE, LIKE), and database optimization.
Python Proficiency: Streamlit for UI, LangChain in sql_agent.py for AI reasoning, and error handling.
Problem-Solving: Overcame persistence, UI, and API challenges through iteration.
Portfolio Edge: Combines analytics with Gen AI, a unique angle for analyst roles.

🖥️ Setup Instructions

Clone the Repository:git clone https://github.com/yourusername/nlq-to-sql-generator.git
cd nlq-to-sql-generator


Install Dependencies:pip install -r requirements.txt

Ensure requirements.txt includes:streamlit
sqlite3
langchain
openai


Set Up Environment:
Create a .env file with your OpenAI API key:OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1


Note: My initial API key was invalid, causing "Pending LLM Title." Use a valid key for full functionality.


Run the App:streamlit run app.py

The app runs at http://localhost:8501, with sql_agent.py handling SQL query generation in the background.

💻 Usage

Start a New Chat: Click "➕ New Chat" in the sidebar to create a chat titled "Untitled Chat."
Enter NLQ: Type a natural language query (e.g., "List users by age") in the chat input.
Get SQL Query: The sql_agent.py script uses LangChain and an LLM to generate and display the SQL query.
Manage Chats:
Select chats from the sidebar to view messages.
Edit chat titles using the text input.
Search chats by title; "No chats found" appears for non-matching searches.


View SQL: Enable "Show Raw SQL" to see generated queries.

📊 Example SQL Query
Analyze chat activity in the database:
SELECT c.title, COUNT(m.msg_id) as message_count
FROM chats c
LEFT JOIN messages m ON c.chat_id = m.chat_id
GROUP BY c.chat_id
ORDER BY c.last_updated DESC;

🙌 Credits

Streamlit Forum: Guided me on chat history persistence with SQLite.
Code with Dilip: Explained SQLite integration for robust storage.
Hrishi Gupta: Introduced LangChain, enabling sql_agent.py to power AI reasoning and memory for NLQ-to-SQL.

📈 Future Improvements

Enhance UI to closer match ChatGPT’s polish.
Support multiple LLM providers in sql_agent.py for redundancy.
Add query execution to display results alongside generated SQL.
Optimize SQLite queries for larger datasets.

🤝 Contributing
Fork, submit issues, or send pull requests! I’m open to feedback and improvements.
📬 Contact
Connect with me on LinkedIn to discuss this project or data analytics opportunities!
#DataAnalytics #GenAI #SQL #Python #Streamlit #Portfolio
