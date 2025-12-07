# Research & Decisions for RAG Chatbot

This document records the key technical decisions made to resolve ambiguities in the initial implementation plan.

## 1. Backend Deployment Platform

- **Decision**: Railway.app
- **Rationale**: Railway offers a simple, Git-based deployment workflow and a generous free tier that includes a small amount of compute and database resources. This aligns perfectly with the project's "Free-Tier First Architecture" and "Fast & Efficient Builds" principles. It is generally easier to get started with for simple FastAPI apps compared to Vercel (which is more frontend-focused) or Fly.io (which is powerful but more complex).
- **Alternatives Considered**:
    - **Vercel**: Excellent for frontends and serverless functions, but can be less straightforward for a standard stateful backend service.
    - **Fly.io**: Very powerful and offers a great free tier, but its `fly.toml` configuration and Docker-centric workflow introduce more complexity than needed for this project's initial phase.

## 2. Text Embeddings Model

- **Decision**: `sentence-transformers/all-MiniLM-L6-v2`
- **Rationale**: This model provides an excellent balance of performance and size. It is lightweight, fast, and widely used, making it a reliable choice for a free-tier project. It is readily available from Hugging Face and integrates seamlessly with Qdrant. This aligns with the "Lightweight embeddings" and "Free-tier friendly" requirements.
- **Alternatives Considered**:
    - **OpenAI `text-embedding-ada-002`**: Higher performance but requires API keys and budget management, violating the "Free-Tier First" principle.
    - **Larger `sentence-transformer` models**: Offer slightly better accuracy but come with higher computational and memory costs, which could strain a free-tier backend.

## 3. Chat History Persistence

- **Decision**: No chat history persistence (for now).
- **Rationale**: For the initial version (MVP), chat history will be ephemeral and exist only for the current session in the frontend's state. This decision strongly aligns with the "Simplicity & Minimalism" principle. It avoids the need for user accounts, database schema management for conversations, and compliance concerns around storing user data. This feature can be added in a future iteration if it's identified as a high-value enhancement.
- **Alternatives Considered**:
    - **Persist in PostgreSQL (Neon)**: Would require creating tables for users and conversations, adding complexity to the backend and data model.
    - **Persist in browser `localStorage`**: A viable stateless option, but can lead to a cluttered UX if not managed carefully and doesn't support history across devices. Deferring this keeps the initial implementation cleaner.
