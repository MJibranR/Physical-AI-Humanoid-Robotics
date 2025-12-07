# Development Tasks: RAG Chatbot

**Branch**: `001-rag-chatbot-spec` | **Date**: 2025-12-07 | **Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

This document outlines the actionable development tasks for implementing the RAG Chatbot feature, ordered by dependencies and categorized by development phases and user stories.

## Project Dependencies

- User Story 1 ("Ask a Question") is the primary and only P1 user story for the initial MVP.

## Task Breakdown

### Phase 1: Setup (Project Initialization)

- [x] T001 Create backend project directory structure at `backend/`
- [x] T002 Initialize Python environment and install core dependencies (`FastAPI`, `uvicorn`, `python-multipart`, `qdrant-client`, `sentence-transformers`) in `backend/`
- [x] T003 Initialize basic FastAPI app in `backend/src/main.py`
- [x] T004 Create `backend/src/core/` directory for RAG logic
- [x] T005 Create `backend/src/models.py` for Pydantic models
- [x] T006 Update Docusaurus `my-website/package.json` to install Axios for API calls
- [x] T007 Create `my-website/src/components/RAGChatbot/` directory for chatbot React component

### Phase 2: Book Content Population

- [x] T008 Populate content for "1. Introduction to Physical AI" in `my-website/docs/tutorial-basics/introduction.md`
- [x] T009 Populate content for "2. Basics of Humanoid Robotics" in `my-website/docs/tutorial-basics/humanoid-robotics-basics.md`
- [x] T010 Populate content for "3. ROS 2 Fundamentals" in `my-website/docs/tutorial-basics/ros2-fundamentals.md`
- [x] T011 Populate content for "4. Digital Twin Simulation (Gazebo + Isaac)" in `my-website/docs/tutorial-basics/digital-twin-simulation.md`
- [x] T012 Populate content for "5. Vision-Language-Action Systems" in `my-website/docs/tutorial-basics/vla-systems.md`
- [x] T013 Populate content for "6. Capstone: Simple AI-Robot Pipeline" in `my-website/docs/tutorial-basics/capstone-ai-robot-pipeline.md`

### Phase 3: Book Content Setup (Blocking Prerequisites for RAG)

- [x] T014 Update Docusaurus sidebar configuration (`my-website/sidebars.ts`) to include the new chapters
- [x] T015 Create a script or utility in `backend/src/core/ingestion.py` to read markdown files from Docusaurus `my-website/docs/`
- [x] T016 Implement text splitting and chunking logic within `backend/src/core/ingestion.py`
- [x] T017 Implement logic to generate embeddings for each chunk using `backend/src/core/embedding_model.py`
- [x] T018 Implement logic to upload chunks and their embeddings to Qdrant using `backend/src/core/qdrant_client.py`
- [ ] T019 Create an initial ingestion process to populate Qdrant with the book content

### Phase 4: Foundational (Blocking Prerequisites)

- [ ] T020 Implement Pydantic `APIRequest` and `APIResponse` models in `backend/src/models.py` matching `contracts/openapi.yml`
- [ ] T021 Implement Qdrant client initialization in `backend/src/core/qdrant_client.py`
- [ ] T022 Implement embedding model loading (`sentence-transformers/all-MiniLM-L6-v2`) in `backend/src/core/embedding_model.py`
- [ ] T023 Create a basic RAG pipeline interface in `backend/src/core/rag_pipeline.py` (e.g., a function that accepts a query and returns a placeholder answer)

### Phase 5: User Story 1 - Ask a Question [US1] (Priority: P1)

*Goal*: A student reading the textbook has a question about a concept and uses the integrated chatbot to get a quick answer without leaving the page.
*Independent Test*: The chatbot UI can be loaded, a question can be submitted, and a response is returned. This delivers the core value of the RAG functionality.

#### Backend Implementation

- [ ] T024 [P] [US1] Implement the `/chat` POST endpoint in `backend/src/main.py`
- [ ] T025 [US1] Integrate `qdrant_client.py` and `embedding_model.py` into `rag_pipeline.py`
- [ ] T026 [US1] Implement RAG logic in `backend/src/core/rag_pipeline.py` to retrieve relevant chunks from Qdrant based on the user's question
- [ ] T027 [US1] Implement prompt engineering and LLM call (e.g., using a free-tier LLM API or local inference if feasible) to generate an answer from retrieved chunks in `backend/src/core/rag_pipeline.py`
- [ ] T028 [P] [US1] Implement CORS middleware in `backend/src/main.py` to allow requests from the Docusaurus frontend

#### Frontend Implementation

- [ ] T029 [P] [US1] Create React component for the chatbot UI (`RAGChatbot.tsx`) in `my-website/src/components/RAGChatbot/`
- [ ] T030 [US1] Implement chat input field, message display, and send button in `my-website/src/components/RAGChatbot/RAGChatbot.tsx`
- [ ] T031 [US1] Integrate `RAGChatbot.tsx` component into a suitable Docusaurus page or layout (e.g., via a plugin or custom theme layout)
- [ ] T032 [US1] Implement API call using Axios from `my-website/src/components/RAGChatbot/RAGChatbot.tsx` to the backend `/chat` endpoint
- [ ] T033 [US1] Display chatbot responses, including sourced text snippets, in `my-website/src/components/RAGChatbot/RAGChatbot.tsx`
- [ ] T034 [P] [US1] Implement basic loading and error states in the chatbot UI (`my-website/src/components/RAGChatbot/RAGChatbot.tsx`)

### Final Phase: Polish & Cross-Cutting Concerns

- [ ] T035 Implement robust error handling and logging for backend components in `backend/src/`
- [ ] T036 Develop deployment script/configuration for FastAPI backend to Railway.app
- [ ] T037 Refine chatbot UI for responsiveness and user experience in `my-website/src/components/RAGChatbot/`
- [ ] T038 Prepare comprehensive documentation for running and deploying the RAG chatbot
- [ ] T039 Conduct end-to-end testing of the integrated system

## Dependencies

- Phase 1 tasks must be completed before Phase 2.
- Phase 2 tasks must be completed before Phase 3.
- Phase 3 tasks must be completed before Phase 4.
- Phase 4 tasks must be completed before Phase 5.
- All tasks within User Story 1 are dependent on each other to form a functional chatbot.

## Parallel Execution Examples

- Backend (T030, T034) and Frontend (T035, T040) development within US1 can proceed in parallel once foundational tasks are complete, assuming adherence to the defined API contract.
- Within Phase 1, T001-T005 and T006-T007 can be started in parallel.
- Within Phase 2, T008-T013 (frontend content population) and T014-T019 (book content setup for ingestion) can be started in parallel.
- Within Phase 3, T020-T025 (frontend content population) and T026-T029 (backend ingestion setup) can be started in parallel.

## Implementation Strategy

The implementation will follow an MVP-first approach, focusing initially on completing User Story 1 "Ask a Question" to deliver core RAG chatbot functionality, which now includes the critical step of ingesting the book content. Subsequent enhancements or additional user stories will be addressed in future iterations.