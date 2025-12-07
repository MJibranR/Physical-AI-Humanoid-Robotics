---
id: 003
title: Feature Book on Homepage
stage: general
date: 2025-12-07
surface: agent
model: gemini-1.5-flash
feature: none
branch: main
user: 
command: I want to add about my book "Physical AI & Humanoid Robotics — Essentials"A comprehensive guide to building intelligent physical systemsa "GET STARTED" button toowith Table of Contents
labels: ["website", "docusaurus", "homepage", "book", "table-of-contents"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - my-website/docs/book-toc.md
  - my-website/sidebars.ts
  - my-website/src/pages/index.tsx
tests_yaml: []
prompt_text: |
  I want to add about my book "Physical AI & Humanoid Robotics — Essentials"A comprehensive guide to building intelligent physical systemsa "GET STARTED" button toowith Table of Contents
RESPONSE_TEXT: |
  I have completed all the requested changes to feature the book on the homepage.
outcome: The Docusaurus homepage was successfully updated to promote the user's book, including a new Table of Contents page and a "GET STARTED" button.
evaluation: The agent successfully implemented the request by creating new content, updating navigation, and modifying the homepage component to prominently feature the book.
