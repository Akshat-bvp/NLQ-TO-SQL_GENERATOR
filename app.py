import sqlite3
import uuid
import datetime
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from sql_agent import get_sql_and_explanation  # Mock or your actual function

# LLM setup (replace with valid key and endpoint)
main_llm = ChatOpenAI(
    model="openai/gpt-4.1-nano",
    base_url="BASE_URL",  # Replace with valid endpoint, e.g., "https://api.openai.com/v1"
    api_key="API_KEY"  # Replace with valid key, e.g., "sk-..."
)

DB_FILE = "conversations.db"

def init_db():
    """Initialize database with chats and messages tables, ensuring correct schema."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS chats (
                         chat_id TEXT PRIMARY KEY,
                         title TEXT,
                         last_updated TEXT
                     )""")
        c.execute("""CREATE TABLE IF NOT EXISTS messages (
                         msg_id TEXT PRIMARY KEY,
                         chat_id TEXT,
                         sender TEXT,
                         content TEXT,
                         timestamp TEXT
                     )""")
        conn.commit()
        c.execute("PRAGMA table_info(messages)")
        columns = {col[1]: col[2] for col in c.fetchall()}
        expected_columns = {
            "msg_id": "TEXT",
            "chat_id": "TEXT",
            "sender": "TEXT",
            "content": "TEXT",
            "timestamp": "TEXT"
        }
        for col, col_type in expected_columns.items():
            if col not in columns:
                c.execute(f"ALTER TABLE messages ADD COLUMN {col} {col_type}")
        conn.commit()

def load_chats_from_db(search_query=""):
    """Load chats and messages from DB, filtered by search query."""
    chats = {}
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT chat_id, title, last_updated FROM chats WHERE title LIKE ? ORDER BY last_updated DESC",
                  (f"%{search_query}%",))
        for chat_id, title, last_updated in c.fetchall():
            chats[chat_id] = {"title": title, "last_updated": last_updated, "messages": []}
            try:
                c.execute("SELECT sender, content FROM messages WHERE chat_id = ? ORDER BY timestamp ASC", (chat_id,))
                chats[chat_id]["messages"] = [{"role": sender, "content": content, "saved": True}
                                             for sender, content in c.fetchall()]
            except sqlite3.OperationalError as e:
                print(f"Error loading messages for chat {chat_id}: {e}")
                chats[chat_id]["messages"] = []
    return chats

def save_message_to_db(chat_id, sender, content):
    """Save message and update chat's last_updated timestamp."""
    timestamp = datetime.datetime.now().isoformat()
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO messages (msg_id, chat_id, sender, content, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (str(uuid.uuid4()), chat_id, sender, content, timestamp))
        c.execute("UPDATE chats SET last_updated = ? WHERE chat_id = ?", (timestamp, chat_id))
        conn.commit()

def create_new_chat(title="Untitled Chat"):
    """Create a new chat in the database."""
    chat_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO chats (chat_id, title, last_updated) VALUES (?, ?, ?)", (chat_id, title, timestamp))
        conn.commit()
    return chat_id

def update_chat_title(chat_id, new_title):
    """Update chat title in the database."""
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("UPDATE chats SET title = ? WHERE chat_id = ?", (new_title, chat_id))
        conn.commit()

def generate_chat_title(prompt):
    """Generate a chat title solely using LLM."""
    print(f"Generating title for prompt: {prompt}")  # Debug log
    try:
        response = main_llm.invoke([HumanMessage(content=(
            f"Create a chat title (max 5 words) based on: '{prompt}'"
        ))])  # Wrap HumanMessage in a list
        title = response.content  # Use raw LLM output
        print(f"Generated title: {title}")  # Debug log
        return title
    except Exception as e:
        print(f"LLM title generation failed: {e}")
        return "Pending LLM Title"  # Temporary placeholder for LLM failure

# Initialize DB and session state
init_db()
if "all_chats" not in st.session_state:
    st.session_state.all_chats = load_chats_from_db()
    st.session_state.selected_chat = (list(st.session_state.all_chats.keys())[0]
                                     if st.session_state.all_chats else create_new_chat())
    st.session_state.all_chats = load_chats_from_db()

# Sidebar
with st.sidebar:
    st.title("My Chats")
    with st.form(key="search_form", clear_on_submit=False):
        search_query = st.text_input("Search Chats", key="chat_search")
        search_submitted = st.form_submit_button("Search")
    if st.button("➕ New Chat"):
        st.session_state.selected_chat = create_new_chat()
        st.session_state.all_chats = load_chats_from_db()
        st.rerun()
    st.markdown("---")
    if search_submitted:
        st.session_state.all_chats = load_chats_from_db(search_query.lower())
        if not st.session_state.all_chats:
            st.write("No chats found.")
    else:
        st.session_state.all_chats = load_chats_from_db()
    if st.session_state.all_chats:
        for chat_id, chat_data in st.session_state.all_chats.items():
            if st.button(chat_data["title"], key=f"chat_{chat_id}", use_container_width=True):
                st.session_state.selected_chat = chat_id
                st.rerun()
    # Handle case where selected_chat is a list or invalid
    selected_chat = st.session_state.selected_chat
    if isinstance(selected_chat, list):
        # If it's a list, pick the first chat_id or create a new chat
        selected_chat = selected_chat[0] if selected_chat else create_new_chat()
        st.session_state.selected_chat = selected_chat
        st.session_state.all_chats = load_chats_from_db()
        st.rerun()
    current_title = st.session_state.all_chats.get(selected_chat, {"title": "Untitled Chat"})["title"]
    new_title = st.text_input("Edit Title", value=current_title, key="title_edit")
    if new_title and new_title != current_title:
        update_chat_title(selected_chat, new_title)
        st.session_state.all_chats[selected_chat]["title"] = new_title
        st.session_state.all_chats = load_chats_from_db()
        st.rerun()
    st.markdown("---")
    llm_temp = st.slider("Model Temperature", 0.0, 1.0, 0.7)
    show_sql = st.checkbox("Show Raw SQL", value=True)

# Main UI
st.header("Chat")
current_messages = st.session_state.all_chats.get(st.session_state.selected_chat, {"messages": []})["messages"]
if current_messages:
    for msg in current_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
else:
    st.write("Start a new conversation")

# Handle user input
if prompt := st.chat_input("Type your message"):
    print(f"Processing prompt: {prompt}")  # Debug log
    current_messages.append({"role": "user", "content": prompt})
    if len(current_messages) == 1 and st.session_state.all_chats[st.session_state.selected_chat]["title"] == "Untitled Chat":
        print("Triggering title generation")  # Debug log
        new_title = generate_chat_title(prompt)
        update_chat_title(st.session_state.selected_chat, new_title)
        st.session_state.all_chats[st.session_state.selected_chat]["title"] = new_title
        print(f"Updated title to: {new_title}")  # Debug log
        st.session_state.all_chats = load_chats_from_db()  # Refresh to ensure DB sync
    sql_query, explanation = get_sql_and_explanation(prompt)
    assistant_response = f"SQL:\n{sql_query}\n\nExplanation:\n{explanation}"
    current_messages.append({"role": "assistant", "content": assistant_response})
    st.session_state.all_chats[st.session_state.selected_chat]["messages"] = current_messages
    with st.chat_message("assistant"):
        if show_sql:
            st.code(sql_query, language="sql")
        st.markdown("**Explanation**")
        st.write(explanation)
    for msg in current_messages:
        if "saved" not in msg:
            save_message_to_db(st.session_state.selected_chat, msg["role"], msg["content"])
            msg["saved"] = True
    st.rerun()
