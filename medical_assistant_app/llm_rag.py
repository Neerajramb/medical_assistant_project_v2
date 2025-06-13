# medical_assistant_app/llm_rag.py
from django.conf import settings
import chromadb
from sentence_transformers import SentenceTransformer
import requests
import json
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()

CHROMA_DB_PATH = os.path.join(settings.BASE_DIR, 'chroma_db')

COLLECTION_NAME = 'medical_knowledge'
MODEL_NAME = 'all-MiniLM-L6-v2'
N_RESULTS = 3

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# --- Global Component Initialization ---
_chroma_client = None
_embedding_model = None
_chroma_collection = None

def _initialize_rag_components():
    """Initializes ChromaDB client and embedding model if not already initialized."""
    global _chroma_client, _embedding_model, _chroma_collection
    if _chroma_client is None:
        try:
            print(f"Initializing ChromaDB client at path: {CHROMA_DB_PATH}")
            _chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
            _chroma_collection = _chroma_client.get_or_create_collection(name=COLLECTION_NAME)
            print(f"ChromaDB client and collection '{COLLECTION_NAME}' initialized.")
        except Exception as e:
            print(f"Error initializing ChromaDB: {e}")
            _chroma_client = None; _chroma_collection = None
            return False

    if _embedding_model is None:
        try:
            _embedding_model = SentenceTransformer(MODEL_NAME)
            print(f"Embedding model '{MODEL_NAME}' loaded.")
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            _embedding_model = None
            return False
    return True

def _call_gemini_api(prompt_text: str) -> str:
    """Helper function to send a prompt to the Gemini API and return the response."""
    if not GEMINI_API_KEY:
        return "LLM API key is not configured. Please set GEMINI_API_KEY in your .env file."

    payload = {"contents": [{"role": "user", "parts": [{"text": prompt_text}]}]}
    headers = {'Content-Type': 'application/json'}
    api_url_with_key = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

    print("--- Sending request to LLM ---")
    
    try:
        response = requests.post(api_url_with_key, headers=headers, data=json.dumps(payload), timeout=60)
        response.raise_for_status()
        result = response.json()

        if result.get("candidates") and result["candidates"][0].get("content", {}).get("parts"):
            return result["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            print("LLM response structure unexpected or empty:", result)
            return "I apologize, but I received an unusual response from the AI. This might be due to a content filter. Please try rephrasing."
    except requests.exceptions.HTTPError as e:
        error_details = f"HTTP Error: {e.response.status_code}"
        try:
            error_message = e.response.json().get("error", {}).get("message", "No details.")
            error_details += f" - {error_message}"
        except json.JSONDecodeError:
            pass
        print(f"Error communicating with LLM API: {error_details}")
        return "There was an issue connecting to the AI. Please check the API key and model name."
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with LLM API: {e}")
        return f"There was an issue connecting to the AI. Error: {e}"
    except Exception as e:
        print(f"An unexpected error occurred during AI call: {e}")
        return "An internal error occurred with the AI. Please try again later."

# medical_assistant_app/llm_rag.py
# (Add this function somewhere in the file, for example, after _call_gemini_api)

def generate_follow_up_greeting(last_user_query: str) -> str:
    """
    Generates a context-aware greeting based on the user's last message.
    """
    if not GEMINI_API_KEY: # Ensure API key is available
        return "Welcome back! How can I help you today?"

    prompt = f"""You are a friendly and caring medical information assistant.
A user has just returned to the chat. Their last message to you was about: "{last_user_query}"

Your task is to craft a warm, welcoming, and polite follow-up question.
- Acknowledge their return.
- Gently refer to their previous concern without being too specific or clinical.
- Ask how they are doing regarding that issue or if they have any more questions about it.
- Keep it concise (1-2 sentences).

Example: "Welcome back! I hope you're doing well. I was just thinking about your question regarding [topic], and I wanted to see how things are going."

Your Answer:"""

    try:
        # Use the existing helper function to call the LLM
        return _call_gemini_api(prompt)
    except Exception as e:
        print(f"Error generating follow-up greeting: {e}")
        # Provide a safe fallback message
        return "Welcome back! I hope you're doing well. How can I assist you further today?"
    
# <<< THIS IS THE MODIFIED FUNCTION YOU NEEDED >>>
def get_rag_response(user_query: str, conversation_history: list[dict]) -> str:
    """
    Handles user queries by building a prompt that includes conversation history
    and retrieved context, instructing the LLM to be context-aware.
    """
    if not _initialize_rag_components():
        return "Error: RAG components failed to initialize. Please check server logs."

    try:
        # Step 1: Retrieve context from ChromaDB (same as before)
        query_embedding = _embedding_model.encode([user_query]).tolist()
        results = _chroma_collection.query(
            query_embeddings=query_embedding,
            n_results=N_RESULTS,
            include=['documents']
        )
        retrieved_docs = results['documents'][0] if results.get('documents') else []
        context_str = "\n".join(retrieved_docs)

        # NEW: Format the conversation history for the prompt
        history_str = "\n".join([f"{msg['sender'].capitalize()}: {msg['message']}" for msg in conversation_history])

        # Step 2: Build the enhanced, context-aware prompt
        prompt = f"""### Persona
You are a knowledgeable, friendly, and helpful medical information assistant. You have a memory of the recent conversation.

### Core Task
Your goal is to answer the user's latest message accurately by following these rules in order.

### Recent Conversation History
(This is the conversation so far. Use it for context, for example, to see if the user is asking a follow-up question.)
{history_str}

### Rules of Engagement
1.  **Off-Topic**: If the user's latest message is clearly NOT related to medicine, health, or wellness, you MUST politely state your purpose. Respond with: "I apologize, but as a medical information assistant, I can only provide information related to health topics. How can I help you with a health question?"

2.  **Medical Question**: If the user asks a medical question, you MUST follow this process:
    a. **Prioritize Provided Information:** First, check if the "Provided Medical Information" below contains a relevant answer to the user's question. If it does, use it to construct your answer.
    b. **Seamless Fallback:** If the "Provided Medical Information" is empty or does not answer the question, you MUST immediately use your own general knowledge to provide a complete and accurate answer. **Never state that you couldn't find it in your database.** Simply proceed to answer.
    c. **Disclaimer:** Always end any medical-related answer with this disclaimer: "Please remember, this information is for educational purposes only and is not a substitute for professional medical advice."

### Provided Medical Information
(This is extra information retrieved from a knowledge base that may be relevant to the user's latest message.)
{context_str}

### User's Latest Message
"{user_query}"

### Your Answer:"""
        
        # Step 3: Call the LLM with the single, powerful prompt
        return _call_gemini_api(prompt)

    except Exception as e:
        print(f"An unexpected error occurred during RAG process: {e}")
        return "An internal error occurred. Please try again later."