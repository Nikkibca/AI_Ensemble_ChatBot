# 🤖 AI Ensemble Chatbot (Gemini + ChatGPT)

## 🚀 Overview

The **AI Ensemble Chatbot** is a Python-based intelligent system that integrates two powerful AI models — **Google Gemini** and **OpenAI ChatGPT** — to deliver more accurate and reliable responses.

Instead of relying on a single AI model, this project queries both models, analyzes their responses using a custom scoring algorithm, and returns the best possible answer to the user.

---

## 🎯 Objective

* Improve response accuracy
* Reduce hallucination risk
* Increase system reliability
* Build a cost-efficient AI solution using free-tier APIs
* Demonstrate real-world AI system design

---

## ⚙️ How It Works

### 1️⃣ User Input

The user provides a prompt via CLI.

### 2️⃣ Dual AI Processing

The system sends the same prompt to:

* Gemini API
* OpenAI API

### 3️⃣ Response Collection

Both models return independent responses.

### 4️⃣ Response Analysis

A lightweight heuristic algorithm evaluates:

* Keyword relevance
* Content coverage
* Response length

### 5️⃣ Best Answer Selection

The system selects the most relevant and balanced response.

### 6️⃣ Output

The final answer is displayed to the user and saved in history.

---

## 🧠 Core Features

* ✅ Multi-model AI integration
* ✅ Automatic response comparison
* ✅ Lightweight scoring algorithm
* ✅ Local rule-based fallback chatbot
* ✅ Conversation history storage (JSON)
* ✅ CLI-based interaction
* ✅ Free-tier friendly design

---

## 🏗️ Project Structure

```
ai_ensemble_bot.py   # Main application file
chat_history.json    # Stored conversation history
.env                 # API keys (not included in repo)
```

---

## 🛠️ Technologies Used

* Python
* OpenAI API
* Google Gemini API
* JSON (for data storage)
* Regex (text processing)
* CLI (Command Line Interface)

---

## 🔍 Analysis Algorithm

The project uses a **heuristic scoring system**:

### Step 1: Keyword Extraction

* Remove stopwords
* Extract meaningful words from prompt

### Step 2: Scoring

* Count keyword matches in each response

### Step 3: Tie-Breaker

* Compare response length to ideal size

### Step 4: Selection

* Choose the response with the highest score

---

## 🧪 Example

**Input:**

```
Explain recursion in Python with example
```

**Process:**

* Extract keywords → recursion, python, example
* Compare responses from both models
* Select the answer with better keyword coverage

---

## 💡 Benefits

* ✔ Higher accuracy using multiple AI models
* ✔ Improved reliability (fallback support)
* ✔ Cost-efficient (no expensive evaluation models)
* ✔ Demonstrates system design & AI integration
* ✔ Scalable for future enhancements

---

## 🔐 Environment Setup

Create a `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

## 📦 Installation

```bash
pip install openai google-genai python-dotenv
```

---

## ▶️ Usage

```bash
python ai_ensemble_bot.py "Your question here"
```

Example:

```bash
python ai_ensemble_bot.py "What is machine learning?"
```

---

## 📁 Output

* Best answer displayed in terminal
* Response source (Gemini/OpenAI)
* Analysis details
* Saved chat history in `chat_history.json`

---

## 🧠 Skills Demonstrated

* API Integration
* Python Programming
* NLP Basics (Keyword Extraction)
* Heuristic Algorithm Design
* System Design Thinking
* Error Handling & Fallback Logic
* Data Storage (JSON)

---

## 🚀 Future Enhancements

* 🔹 Web UI (Flask / Streamlit)
* 🔹 Semantic similarity using embeddings
* 🔹 Response merging (hybrid answer)
* 🔹 Confidence scoring system
* 🔹 Database integration
* 🔹 Real-time chat interface

---

## 🎤 Interview Explanation (Short)

> Developed an AI ensemble chatbot integrating Gemini and OpenAI APIs. Implemented a keyword-based scoring algorithm to evaluate and select the most relevant response, improving accuracy, reliability, and cost efficiency.

---

## 📜 License

This project is for educational and personal use.

---

## 🙌 Acknowledgements

* OpenAI API
* Google Gemini API

---

⭐ If you like this project, consider giving it a star!
