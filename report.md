# 📄 ChatWithPDF – Intelligent Chatbot for Documents

## 🧠 Overview

**ChatWithPDF** is an intelligent, interactive chatbot that allows users to upload a **PDF**, **image**, or **text** file and interact with the content using natural language. The chatbot reads and understands the uploaded documents and provides **context-aware answers**, **summaries**, and **insights**. 

This project blends **AI-powered document understanding** with a clean **authentication system** using **Supabase**, and integrates **DeepSeek** as the LLM backend for real-time, accurate responses.

---

## 🚀 Features

- ✅ Upload and parse PDF documents
- ✅ Accept image (OCR-based), text, or PDF files as input
- ✅ Ask questions directly from the document
- ✅ AI-generated **summary of the entire PDF**
- ✅ Email-based **sign-up and login** (via Supabase)
- ✅ Chat interface to **interact with documents conversationally**
- ✅ Stores and retrieves document history per user
- ✅ Fast, smart, and scalable using **DeepSeek API**

---

## 🛠️ Tech Stack

| Layer           | Technology            |
|----------------|------------------------|
| Frontend       | Cursor (React/Next.js) |
| Backend        | Supabase (Auth + DB)   |
| LLM/Chat API   | DeepSeek               |
| File Handling  | PDF.js / Tesseract.js (OCR) |
| State Handling | Zustand / Redux (optional) |
| Auth           | Supabase Email Auth    |

---

## ⚙️ Workflow

1. **User Login**  
   🔐 Sign up or log in via email using Supabase Auth.

2. **Document Upload**  
   📄 Upload PDF / 📷 Image / 📜 Text.

3. **Processing**  
   - PDFs: Extract text using `pdfjs-dist`
   - Images: Use OCR (`Tesseract.js`)
   - Text: Process directly

4. **LLM Interaction**  
   - Use **DeepSeek API** to summarize and answer questions
   - Prompts are enhanced with the extracted document content

5. **Chat Interface**  
   - A React-based interface displays user queries and AI responses
   - Maintains document and query context

6. **Data Storage**  
   - Store user metadata and document history in **Supabase**

---

