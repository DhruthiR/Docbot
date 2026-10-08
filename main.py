import streamlit as st
import os
import csv
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION & CSS STYLING
# --------------------------------------------------
st.set_page_config(
    page_title="Academic Regulation Query Portal",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
        text-align: left;
        background-color: #f9f9f9;
        color: #333;
    }
    .stButton > button:hover {
        background-color: #e6f3ff;
        border-color: #1f77b4;
        color: #1f77b4;
    }
    .tech-badge {
        background-color: #f0f2f6;
        color: #333;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        margin: 2px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# IMPORTS & INITIALIZATION
# --------------------------------------------------
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_openai import ChatOpenAI
    from langchain.chains import ConversationalRetrievalChain
    from langchain.memory import ConversationBufferMemory
    from langchain.prompts import PromptTemplate
except Exception as e:
    st.error(f"Library import error: {e}")
    st.stop()

MATERIAL_FOLDER = "Material"
VECTOR_DB_FOLDER = "vectorstore"
FEEDBACK_FILE = "feedback.csv"

os.makedirs(MATERIAL_FOLDER, exist_ok=True)
os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def log_feedback(question, answer, feedback_type):
    """Logs user feedback to a CSV file for RLHF evaluation."""
    file_exists = os.path.isfile(FEEDBACK_FILE)
    with open(FEEDBACK_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Question", "Answer", "Feedback"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), question, answer, feedback_type])

# --------------------------------------------------
# LLM & VECTOR DB FUNCTIONS
# --------------------------------------------------
@st.cache_resource
def get_llm():
    api_key = st.secrets["GROQ_API_KEY"]
    return ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
        model="openai/gpt-oss-120b",
        temperature=0.3
    )

def create_vector_db(pdf_filename):
    with st.spinner(f"Processing document: {pdf_filename}..."):
        source_path = os.path.join(MATERIAL_FOLDER, pdf_filename)
        db_name = pdf_filename.split(".")[0]
        save_path = os.path.join(VECTOR_DB_FOLDER, db_name)

        try:
            loader = PyPDFLoader(source_path)
            documents = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = splitter.split_documents(documents)

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"}
            )
            db = FAISS.from_documents(texts, embeddings)
            db.save_local(save_path)
            st.toast("Document indexed successfully!", icon="✅")
            return True
        except Exception as e:
            st.error(f"Processing failed: {e}")
            return False

def get_retriever(pdf_filename):
    db_name = pdf_filename.split(".")[0]
    load_path = os.path.join(VECTOR_DB_FOLDER, db_name)

    if not os.path.exists(load_path):
        return None

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    db = FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)
    return db.as_retriever(search_kwargs={"k": 3})

# --------------------------------------------------
# SIDEBAR (Professional Dashboard Style)
# --------------------------------------------------
with st.sidebar:
    try:
        st.image("assets/college_logo.png", width=100)
    except:
        st.warning("Logo not found in assets folder.")
        
    st.markdown("## RV College of Engineering")
    st.caption("Academic Regulation & Scheme Query Portal")
    st.divider()

    st.subheader("📄 Indexed Documents")
    pdf_files = [f for f in os.listdir(MATERIAL_FOLDER) if f.endswith(".pdf")]
    
    if pdf_files:
        for pdf in pdf_files:
            st.markdown(f"- {pdf}")
    else:
        st.markdown("*No documents indexed yet.*")

    st.divider()
    
    st.subheader("⚙️ Control Panel")
    uploaded_file = st.file_uploader("Upload official PDF document", type=["pdf"])

    if uploaded_file and st.button("Process Document", use_container_width=True):
        file_path = os.path.join(MATERIAL_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        create_vector_db(uploaded_file.name)
        st.rerun()

    st.divider()

    # Chat Export Feature
    if "messages" in st.session_state and st.session_state.messages:
        chat_text = ""
        for msg in st.session_state.messages:
            sender = "User" if msg["role"] == "user" else "Assistant"
            chat_text += f"{sender}: {msg['content']}\n\n"
        
        st.download_button(
            label="📥 Export Chat (TXT)",
            data=chat_text,
            file_name="chat_export.txt",
            mime="text/plain",
            use_container_width=True
        )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    
    st.subheader("🛠️ Built With")
    st.markdown("""
    <span class="tech-badge">LangChain</span>
    <span class="tech-badge">FAISS DB</span>
    <span class="tech-badge">Groq API</span>
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">HuggingFace</span>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# MAIN INTERFACE
# --------------------------------------------------
st.markdown("<h1 style='text-align: center;'>📄 Academic Regulation DocBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 18px;'>Ask questions strictly based on official academic documents.</p>", unsafe_allow_html=True)
st.divider()

if not pdf_files:
    st.info("👈 Please upload an official PDF document in the sidebar to begin.")
    st.stop()
else:
    selected_pdf = st.selectbox("Select Active Document to Query", pdf_files)
    db_name = selected_pdf.split(".")[0]
    if not os.path.exists(os.path.join(VECTOR_DB_FOLDER, db_name)):
        st.warning("Document not indexed yet. Indexing now...")
        create_vector_db(selected_pdf)
        st.rerun()

st.markdown("### 💡 Example Questions")
quick_questions = [
    "Explain SEE evaluation process",
    "What is the PVP process?",
    "Explain fast track examination",
    "Attendance requirements for semester"
]

cols = st.columns(2)
for i, q in enumerate(quick_questions):
    if cols[i % 2].button(q):
        st.session_state["auto_query"] = q

st.divider()

# --------------------------------------------------
# CHAT INTERFACE
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        if "sources" in msg:
            with st.expander("📄 View Sources"):
                for src in msg["sources"]:
                    st.markdown(f"- **Page {src}**")
        
        # User Feedback Feature (Thumbs Up/Down)
        if msg["role"] == "assistant":
            current_feedback = msg.get("feedback", None)
            
            fb_col1, fb_col2, _ = st.columns([1, 1, 10])
            
            if fb_col1.button("👍", key=f"like_{i}", disabled=(current_feedback is not None)):
                st.session_state.messages[i]["feedback"] = "up"
                # Find the corresponding user question
                user_q = st.session_state.messages[i-1]["content"] if i > 0 else "N/A"
                log_feedback(user_q, msg["content"], "up")
                st.toast("Feedback logged! Thank you.", icon="👍")
                st.rerun()
                
            if fb_col2.button("👎", key=f"dislike_{i}", disabled=(current_feedback is not None)):
                st.session_state.messages[i]["feedback"] = "down"
                user_q = st.session_state.messages[i-1]["content"] if i > 0 else "N/A"
                log_feedback(user_q, msg["content"], "down")
                st.toast("Feedback logged! We will improve.", icon="👎")
                st.rerun()

            if current_feedback:
                st.caption(f"*You rated this response: {current_feedback}*")

user_input = st.chat_input("Ask your academic query here...")

if "auto_query" in st.session_state:
    user_input = st.session_state.pop("auto_query")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    retriever = get_retriever(selected_pdf)
    if not retriever:
        st.error("Vector database not found. Please process the document.")
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Generating verified academic response..."):
            try:
                llm = get_llm()

                prompt_template = """
You are an academic regulation assistant.

Rules:
- Answer strictly using the provided context.
- Do not use external knowledge.
- If the answer is not present, clearly state that it is not available in the document.
- Format the answer using bullet points and bold text where appropriate for readability.

Context:
{context}

Question:
{question}

Answer:
"""
                PROMPT = PromptTemplate(
                    template=prompt_template,
                    input_variables=["context", "question"]
                )

                chain = ConversationalRetrievalChain.from_llm(
                    llm=llm,
                    retriever=retriever,
                    memory=ConversationBufferMemory(
                        memory_key="chat_history",
                        return_messages=True,
                        output_key="answer"
                    ),
                    combine_docs_chain_kwargs={"prompt": PROMPT},
                    return_source_documents=True
                )

                response = chain.invoke({"question": user_input})
                answer = response["answer"]

                source_docs = response.get("source_documents", [])
                source_pages = list(set([doc.metadata.get('page', 'Unknown') + 1 for doc in source_docs]))

                st.markdown(answer)
                
                if source_pages:
                    with st.expander("📄 View Sources"):
                        for pg in source_pages:
                            st.markdown(f"- **Page {pg}**")

                # Append to session state with feedback initialized as None
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": source_pages, "feedback": None}
                )
                st.rerun() # Rerun to display the feedback buttons immediately

            except Exception as e:
                st.error(f"Error generating response: {e}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<hr>
<p style='text-align:center; color:gray; font-size:13px;'>
© 2025 RV College of Engineering | Examination & Academic Regulations Portal
</p>
""", unsafe_allow_html=True)