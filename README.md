# DocBot – RAG-Based PDF Question Answering System

DocBot is an AI-powered document question-answering system that allows users to upload PDF documents and interact with them using natural-language questions.

The application uses Retrieval-Augmented Generation(RAG) to retrieve relevant information from uploaded documents before generating an answer. This approach helps the system provide responses grounded in the document content rather than relying only on the language model's internal knowledge.

# 🚀 Key Features

* Upload and process PDF documents
* Extract text from documents
* Split documents into manageable text chunks
* Generate vector embeddings for document chunks
* Store and search embeddings using FAISS
* Retrieve relevant document content based on user questions
* Generate answers using an LLM
* Interactive question-answering interface
* Supports natural-language queries over uploaded documents
* Designed to reduce unsupported or hallucinated responses by grounding answers in retrieved document content

# 🏗️ System Architecture

                ┌──────────────────┐
                │    PDF Upload    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Text Extraction │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Text Chunking    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    Embeddings    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ FAISS Vector DB  │
                └────────┬─────────┘
                         │
                    User Question
                         │
                         ▼
                ┌──────────────────┐
                │ Similarity Search│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Relevant Context │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │      LLM         │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    Answer        │
                └──────────────────┘

# 🧠 Why RAG?

A traditional LLM may generate an answer based on its pretrained knowledge, which may result in inaccurate or unsupported information.

RAG adds a retrieval layer:
User Question
      ↓
Retrieve relevant information
      ↓
Provide retrieved information to LLM
      ↓
Generate grounded answer

This makes the system particularly useful for question answering over private or domain-specific documents.

# 🛠️ Technologies Used
Python - Programming Language
Streamlit – Interactive application interface
RAG – Retrieval-Augmented Generation
FAISS – Vector similarity search
Text Embeddings – Semantic representation of documents
LLM / Generative AI API – Answer generation
PDF Processing Libraries – Document text extraction

## 📂 Project Structure

DocBot/
│
├── app.py
├── requirements.txt
├── README.md
│
├── <RAG / processing modules>
├── <embedding / vector search modules>
├── <LLM integration modules>
├── <UI components>
│
"The exact structure may vary depending on the implementation."

# ⚙️ Installation
# 1. Clone the repository
git clone https://github.com/<your-username>/DocBot.git
cd DocBot
# 2. Create a virtual environment
python -m venv venv
# 3. Activate the virtual environment
Windows:
venv\Scripts\activate
Linux/macOS:
source venv/bin/activate
# 4. Install dependencies
pip install -r requirements.txt
# 5. Configure API credentials
If the application uses an external LLM API, create a `.env` file and add the required API key
Example:
LLM_API_KEY=your_api_key_here
*Never commit real API keys or secrets to GitHub.*
### 6. Run the application
streamlit run app.py
The application will then be available through the local Streamlit server.

## 🎯 Use Cases
DocBot can be used for:
* Research papers
* Technical documentation
* Academic notes
* Company documents
* User manuals
* Policy documents
* Reports
* Study materials
* Knowledge-base question answering

## 🔐 Security Considerations
When deploying a document-based AI application, security should be considered at multiple levels:
* Validate uploaded file types
* Restrict potentially unsafe files
* Protect API credentials
* Avoid exposing sensitive document contents
* Limit file size and processing resources
* Protect against prompt injection attacks
* Prevent unauthorized access to uploaded documents
* Avoid logging sensitive document information
  
## 📊 Evaluation

The quality of a RAG application should be evaluated using a representative set of questions and expected answers.

Useful evaluation areas include:

* Retrieval relevance
* Answer correctness
* Context relevance
* Faithfulness to source documents
* Response latency
* Failure cases
* Hallucination rate

Future versions of DocBot can include a dedicated evaluation dataset and automated RAG evaluation metrics.

## 🚧 Current Limitations

Depending on the current implementation, potential limitations include:

* PDF-only document support
* Limited document-management capabilities
* Retrieval quality depends on chunking and embedding configuration
* LLM responses depend on the quality of retrieved context
* No guarantee that every generated answer is completely correct
* API-dependent functionality may require external credentials

## 🔮 Future Improvements

Planned improvements include:

* [ ] Source citations with page numbers
* [ ] Multi-document question answering
* [ ] Document metadata management
* [ ] Improved chunking strategies
* [ ] Reranking of retrieved documents
* [ ] Conversation memory
* [ ] "I don't know" / insufficient-context handling
* [ ] Prompt-injection detection
* [ ] File validation and security controls
* [ ] FastAPI backend
* [ ] Authentication and authorization
* [ ] Query and system monitoring
* [ ] Improved UI/UX

## 👩‍💻 Author

**Dhruthi R**
Computer Science and Engineering – Cyber Security
Bengaluru, India

[LinkedIn](https://www.linkedin.com/in/dhruthir27/)

[GitHub](https://github.com/DhruthiR)

## 📄 License

This project is intended for educational and portfolio purposes.

Add an appropriate open-source license if you plan to distribute or modify the project for broader use.
