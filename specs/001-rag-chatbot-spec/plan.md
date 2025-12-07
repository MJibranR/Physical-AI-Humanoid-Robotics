# Implementation Plan: RAG Chatbot

**Branch**: `001-rag-chatbot-spec` | **Date**: 2025-12-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-rag-chatbot-spec/spec.md`

## Summary

This plan outlines the technical implementation for the AI-Native Textbook's RAG (Retrieval-Augmented Generation) chatbot. The primary goal is to provide a simple, free-tier, and effective chat interface within the Docusaurus site. The technical approach involves a Python FastAPI backend for the RAG logic, a Qdrant vector database, and a lightweight sentence-transformer model for embeddings. The frontend will be a React component integrated into the existing Docusaurus application.

## Technical Context

**Language/Version**: Python 3.11, TypeScript (for Docusaurus/React)
**Primary Dependencies**: FastAPI, Qdrant-client, Sentence-Transformers, React
**Storage**: N/A (Chat history is not persisted, per `research.md`)
**Testing**: Pytest for backend, Jest/RTL for frontend components
**Target Platform**: Web (Docusaurus site) and Railway.app (for FastAPI backend)
**Project Type**: Web application (frontend/backend)
**Performance Goals**: < 3 seconds p90 response time for chat queries
**Constraints**: Must operate within free-tier service limits. No persisted user data.
**Scale/Scope**: Single chatbot for a 6-chapter textbook.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Simplicity & Minimalism**: ✅ Pass. The architecture is minimal, avoiding databases and user accounts.
- **II. Accuracy & Verifiability**: ✅ Pass. The plan is to use RAG exclusively from book content.
- **III. Free-Tier First Architecture**: ✅ Pass. All chosen components (Railway, Qdrant Cloud free tier, Hugging Face models) fit this principle.
- **IV. Fast & Efficient Builds**: ✅ Pass. The lightweight model and simple backend contribute to fast builds.
- **V. Docusaurus for Content**: ✅ Pass. The plan integrates directly with the existing Docusaurus site.
- **VI. RAG-Powered Interaction**: ✅ Pass. This is the core of the implementation.

**Result**: All gates pass.

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot-spec/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── openapi.yml
└── tasks.md             # To be created by /sp.tasks
```

### Source Code (repository root)

The project will follow a frontend/backend split. The Docusaurus site already exists in `my-website`, which will serve as the frontend. A new `backend` directory will be created for the FastAPI application.

```text
my-website/              # Existing Docusaurus site (Frontend)
├── src/
│   ├── components/
│   │   └── RAGChatbot/  # New component to be created
│   └── ...
└── ...

backend/                 # New directory for the RAG API
├── src/
│   ├── main.py          # FastAPI app entrypoint
│   ├── core/            # Core logic (RAG pipeline)
│   └── models.py        # Pydantic models for API
└── tests/
```

**Structure Decision**: A separate `backend` directory will be created to house the FastAPI application, keeping it decoupled from the Docusaurus frontend in `my-website`. This provides a clean separation of concerns.

## Complexity Tracking

No complexity tracking needed as all constitution gates passed.