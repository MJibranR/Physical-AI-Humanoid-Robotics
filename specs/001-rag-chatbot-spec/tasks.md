# Development Tasks: RAG Chatbot

**Branch**: `001-rag-chatbot-spec` | **Date**: 2025-12-07 | **Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

This document outlines the actionable development tasks for implementing the RAG Chatbot feature, ordered by dependencies and categorized by development phases and user stories.

## Project Dependencies

- User Story 1 ("Ask a Question") is the primary and only P1 user story for the initial MVP.

## Task Breakdown

### Phase 1: Setup (Project Initialization)

- [ ] T001 Create backend project directory structure at `backend/`
- [ ] T002 Initialize Python environment and install core dependencies (`FastAPI`, `uvicorn`, `python-multipart`, `qdrant-client`, `sentence-transformers`) in `backend/`
- [ ] T003 Initialize basic FastAPI app in `backend/src/main.py`
- [ ] T004 Create `backend/src/core/` directory for RAG logic
- [ ] T005 Create `backend/src/models.py` for Pydantic models
- [ ] T006 Update Docusaurus `my-website/package.json` to install Axios for API calls
- [ ] T007 Create `my-website/src/components/RAGChatbot/` directory for chatbot React component

### Phase 2: Foundational (Blocking Prerequisites)

- [ ] T008 Implement Pydantic `APIRequest` and `APIResponse` models in `backend/src/models.py` matching `contracts/openapi.yml`
- [ ] T009 Implement Qdrant client initialization in `backend/src/core/qdrant_client.py`
- [ ] T010 Implement embedding model loading (`sentence-transformers/all-MiniLM-L6-v2`) in `backend/src/core/embedding_model.py`
- [ ] T011 Create a basic RAG pipeline interface in `backend/src/core/rag_pipeline.py` (e.g., a function that accepts a query and returns a placeholder answer)

### Phase 3: User Story 1 - Ask a Question [US1] (Priority: P1)

*Goal*: A student reading the textbook has a question about a concept and uses the integrated chatbot to get a quick answer without leaving the page.
*Independent Test*: The chatbot UI can be loaded, a question can be submitted, and a response is returned. This delivers the core value of the RAG functionality.

#### Backend Implementation

- [ ] T012 [P] [US1] Implement the `/chat` POST endpoint in `backend/src/main.py`
- [ ] T013 [US1] Integrate `qdrant_client.py` and `embedding_model.py` into `rag_pipeline.py`
- [ ] T014 [US1] Implement RAG logic in `backend/src/core/rag_pipeline.py` to retrieve relevant chunks from Qdrant based on the user's question
- [ ] T015 [US1] Implement prompt engineering and LLM call (e.g., using a free-tier LLM API or local inference if feasible) to generate an answer from retrieved chunks in `backend/src/core/rag_pipeline.py`
- [ ] T016 [P] [US1] Implement CORS middleware in `backend/src/main.py` to allow requests from the Docusaurus frontend

#### Frontend Implementation

- [ ] T017 [P] [US1] Create React component for the chatbot UI (`RAGChatbot.tsx`) in `my-website/src/components/RAGChatbot/`
- [ ] T018 [US1] Implement chat input field, message display, and send button in `my-website/src/components/RAGChatbot/RAGChatbot.tsx`
- [ ] T019 [US1] Integrate `RAGChatbot.tsx` component into a suitable Docusaurus page or layout (e.g., via a plugin or custom theme layout)
- [ ] T020 [US1] Implement API call using Axios from `my-website/src/components/RAGChatbot/RAGChatbot.tsx` to the backend `/chat` endpoint
- [ ] T021 [US1] Display chatbot responses, including sourced text snippets, in `my-website/src/components/RAGChatbot/RAGChatbot.tsx`
- [ ] T022 [P] [US1] Implement basic loading and error states in the chatbot UI (`my-website/src/components/RAGChatbot/RAGChatbot.tsx`)

### Final Phase: Polish & Cross-Cutting Concerns

- [ ] T023 Implement robust error handling and logging for backend components in `backend/src/`
- [ ] T024 Develop deployment script/configuration for FastAPI backend to Railway.app
- [ ] T025 Refine chatbot UI for responsiveness and user experience in `my-website/src/components/RAGChatbot/`
- [ ] T026 Prepare comprehensive documentation for running and deploying the RAG chatbot
- [ ] T027 Conduct end-to-end testing of the integrated system

## Dependencies

- Phase 1 tasks must be completed before Phase 2.
- Phase 2 tasks must be completed before Phase 3.
- All tasks within User Story 1 are dependent on each other to form a functional chatbot.

## Parallel Execution Examples

- Backend (T012, T016) and Frontend (T017, T022) development within US1 can proceed in parallel once foundational tasks are complete, assuming adherence to the defined API contract.
- Within Phase 1, T001-T005 and T006-T007 can be started in parallel.

## Implementation Strategy

The implementation will follow an MVP-first approach, focusing initially on completing User Story 1 "Ask a Question" to deliver core RAG chatbot functionality. Subsequent enhancements or additional user stories will be addressed in future iterations.

