## ⚕️ MedAssist AI: Your Intelligent Health Companion (v2)

An intelligent, AI-powered conversational assistant designed to provide accurate and contextually relevant information on medical, health, and mental health topics. This project showcases the power of Retrieval Augmented Generation (RAG) by combining Large Language Models (LLMs) with a specialized knowledge base, ensuring reliable and grounded responses, now with a beautiful, full-screen, and minimalist user interface, user authentication, and chat memory.

## ✨ Features

Intelligent Query Routing: Automatically classifies user queries as medical or non-medical to provide the most appropriate response.
Contextual RAG Pipeline: Leverages a local vector database to retrieve specific medical information, augmenting LLM responses for factual accuracy and reducing hallucinations.
General Medical Knowledge Fallback: If local data is insufficient for a medical query, the system intelligently defaults to the LLM's broader medical knowledge.
Polite Non-Medical Redirection: Graciously informs users when queries fall outside its specialized medical scope.
Dynamic & Extensible Knowledge Base: Easily update and expand the medical knowledge by modifying a simple text file, without needing to retrain the core LLM.
Modern, Full-Screen Web Interface: A responsive, intuitive, and aesthetically pleasing chat UI built with HTML, CSS, and JavaScript, offering a minimalist full-screen experience.
User Authentication & Registration: Secure user login and registration system with email and password, allowing for personalized experiences.
Persistent Chat Memory: The system remembers previous conversations and user concerns, enabling more natural and contextually aware interactions over time.
Scalable Architecture: Built on Python and Django, designed for potential expansion and production deployment.

## 🚀 Why This Project Matters (Importance & Industrial Uses)

In today's information-rich world, access to reliable and personalized health information is critical. This project addresses several key challenges and offers significant industrial value:

Enhanced Information Accessibility & Personalization: Provides an easy-to-use, personalized platform for individuals to quickly access general health knowledge, remembering their past interactions for a more tailored experience. This reduces the burden on healthcare professionals for routine queries.
Improved Accuracy & Trust: By grounding LLM responses with RAG, the system significantly minimizes the risk of misinformation and hallucinations, which is paramount in sensitive domains like healthcare.
Scalable Knowledge Management: The extensible knowledge base design means new research, guidelines, or medical updates can be integrated rapidly, keeping the assistant's information current without costly model retraining.
Operational Efficiency for Healthcare: Can serve as a preliminary information source, triage tool, or educational resource in various healthcare settings, freeing up human experts for more complex tasks.
Foundation for Specialized AI: The modular architecture provides a robust blueprint for developing highly specialized AI assistants in specific medical fields (e.g., drug interactions, rare disease information, clinical trial support).
Showcase of Advanced AI & Web Techniques: Demonstrates practical application of cutting-edge LLM, Vector Database, RAG technologies, secure user authentication, and modern web design, offering a valuable learning and development resource.

## 💻 Technologies Used

Python: The core programming language.
Django: High-level Python web framework for the backend, handling user authentication, chat memory, and API endpoints.
Large Language Model (LLM): Gemini 2.0 Flash API for intelligent response generation and query classification.
Vector Database: ChromaDB for efficient semantic search and knowledge retrieval.
Text Embeddings: Sentence Transformers (all-MiniLM-L6-v2) for converting text into vector representations.
Frontend: HTML, Custom CSS (mimicking Tailwind for a minimalist look), and JavaScript for a responsive, full-screen, and aesthetic user interface.
.env: For secure management of API keys and sensitive configurations.

## 📂 Project Structure

```Bash

medical_assistant_project_v2/
├── venv/                      # Python Virtual Environment
├── your_django_project/       # Main Django project container
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # Django project settings
│   ├── urls.py                # Main project URL configurations
│   └── wsgi.py
├── medical_assistant_app/     # Django application for the assistant
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   │   ├── auth.css       # CSS for authentication pages
│   │   │   └── style.css      # General CSS for chat interface
│   │   └── js/
│   │       ├── auth.js        # JavaScript for authentication interactivity
│   │       └── main.js        # Main JavaScript for chat interactivity
│   ├── templates/
│   │   ├── auth.html          # HTML template for login/registration
│   │   └── chat.html          # HTML template for the main chat interface
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── llm_rag.py             # Core RAG and LLM interaction logic
│   ├── models.py              # Includes User and Chat models for memory
│   ├── tests.py
│   ├── urls.py                # App-specific URL configurations
│   └── views.py               # Handles web requests, user authentication, and LLM logic
├── medical_data.txt           # Your curated medical knowledge base (text format)
├── load_data_to_vectordb.py   # Script to process medical_data.txt into ChromaDB
├── generate_medical_facts.py  # (Optional) Script to generate more facts using LLM
├── .env                       # Environment variables (e.g., GEMINI_API_KEY) - IMPORTANT: Add to .gitignore!
├── .gitignore                 # Specifies files/directories to ignore in Git
└── manage.py                  # Django's command-line utility
```
## ⚙️ How to Run
Clone the Repository:

```Bash

git clone https://github.com/Neerajramb/medical_assistant_project_v2.git
cd medical_assistant_project_v2
Create and Activate Virtual Environment:
```
```Bash

python -m venv venv
```
On Windows:
```Bash

.\venv\Scripts\activate
```
On macOS/Linux:

```Bash

source venv/bin/activate
``` 
3.  Install Dependencies:

Create a `requirements.txt` file in your root directory with the following content:

```
django
chromadb
sentence-transformers
requests
python-dotenv
numpy
```

Then, install them:

```bash
pip install -r requirements.txt
```
Set Up Environment Variables:

Create a file named .env in the root of your project (same directory as manage.py and medical_data.txt). Add your Gemini API Key:

GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
Replace "YOUR_ACTUAL_GEMINI_API_KEY" with your actual API key obtained from Google AI Studio. Remember to add .env to your .gitignore file!

Prepare Medical Knowledge Base:

Ensure you have medical_data.txt in the root directory with your desired medical facts.
Run the script to populate your vector database:

```Bash

python load_data_to_vectordb.py
(Optional: If you want to generate more data, run python generate_medical_facts.py)
```
Run Django Migrations:

```Bash

python manage.py makemigrations medical_assistant_app
python manage.py migrate
Create a Superuser (Optional, for Django Admin):
```
```Bash

python manage.py createsuperuser
Follow the prompts to create an administrator account.
```
Start the Django Development Server:

```Bash

python manage.py runserver
```
Access the Application:

Open your web browser and navigate to http://127.0.0.1:8000/. You will be directed to the login/registration page.

## 📈 Future Enhancements

Advanced Data Ingestion: Implement tools for ingesting PDFs, web pages, and other document formats directly into the knowledge base via the admin panel.
Source Citation: Display the source documents from the vector database that were used to generate a response, enhancing transparency.
Voice Input/Output: Integrate speech-to-text and text-to-speech capabilities for a more natural conversational experience.
Multi-modal Inputs: Allow users to upload images (e.g., rash photos) for analysis (requires a multi-modal LLM).
Real-time Streaming: Implement server-sent events (SSE) or WebSockets for streaming LLM responses, providing a more dynamic chat experience.
Admin Panel for Knowledge Base: Create a robust Django admin interface for managing medical_data.txt chunks and medical data directly.
Deployment to Cloud: Prepare for scalable production deployment on platforms like Google Cloud, AWS, or Heroku.
Disclaimer: This LLM-Based Medical Assistant System is for informational and educational purposes only and does not constitute professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare professional for any health concerns.

## 🧑‍💻 Author
**NEERAJ RAM B**
---
