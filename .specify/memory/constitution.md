# Physical AI & Humanoid Robotics - Essentials Constitution

## Core Principles

### I. Simplicity & Minimalism
The project must prioritize simplicity in design, architecture, and user experience. The UI must be clean and uncluttered. Content should be concise and easy to understand, focusing on essential concepts.

### II. Accuracy & Verifiability
All content within the textbook must be accurate and fact-checked. The RAG chatbot must provide answers derived *only* from the book's text, ensuring all information is verifiable against the source material.

### III. Free-Tier First Architecture
All components must be designed to run within the free tiers of cloud services (e.g., Neon, and hosting for FastAPI/Docusaurus). This ensures the project is accessible and low-cost. No components requiring heavy GPU usage are permitted.

### IV. Fast & Efficient Builds
The development process must be optimized for fast build times and smooth deployments, particularly to GitHub Pages. This includes using lightweight embeddings and minimizing dependencies to ensure a streamlined workflow.

### V. Docusaurus for Content
The textbook content will be built and maintained using Docusaurus. This provides a modern, searchable, and easy-to-navigate interface for the educational material, enhancing the learning experience.

### VI. RAG-Powered Interaction
The primary interactive element will be a RAG (Retrieval-Augmented Generation) chatbot using a stack of Qdrant, Neon, and FastAPI. The chatbot's knowledge is strictly limited to the textbook's content to ensure relevance and accuracy.

## Governance

This Constitution is the foundational document for all development within this project. It supersedes all other practices and conventions. Amendments to this constitution require a formal proposal, a peer review, and a documented migration plan for existing systems. All code reviews must include a check for compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07