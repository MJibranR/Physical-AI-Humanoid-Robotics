# Data Model for RAG Chatbot

This document describes the data structures used by the RAG chatbot feature. Based on the decisions in `research.md`, these entities are treated as in-memory data structures and are not persisted to a database in the initial implementation.

## Entity: ChatMessage

Represents a single message in the chat interface.

| Attribute | Type   | Description                               |
|-----------|--------|-------------------------------------------|
| `id`      | String | A unique identifier for the message (e.g., UUID). |
| `content` | String | The text content of the message.          |
| `sender`  | Enum   | Indicates who sent the message (`USER` or `BOT`). |
| `sources` | Array  | (Optional) For bot messages, a list of source snippets from the textbook. |

## Entity: APIRequest

Represents the JSON payload sent to the chatbot backend.

| Attribute  | Type   | Description                       |
|------------|--------|-----------------------------------|
| `question` | String | The user's question to the chatbot. |

## Entity: APIResponse

Represents the JSON payload returned by the chatbot backend.

| Attribute | Type   | Description                                            |
|-----------|--------|--------------------------------------------------------|
| `answer`  | String | The chatbot's generated answer.                        |
| `sources` | Array  | A list of source text snippets used to generate the answer. |
