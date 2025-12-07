---
id: 008
title: Customize Docusaurus Footer with New Links
stage: general
date: 2025-12-07
surface: agent
model: gemini-1.5-flash
feature: none
branch: main
user: 
command: Please change footer, and add TEXTBOOK having link of TOC, RESOURCES having links of ROS 2 Docs Gazebo Simulator, and NVIDIA Isaac Sim, AND MORE having github link of my page
labels: ["website", "docusaurus", "footer", "navigation", "links"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - my-website/docusaurus.config.ts
tests_yaml: []
prompt_text: |
  Please change footer, and add TEXTBOOK having link of TOC, RESOURCES having links of ROS 2 Docs Gazebo Simulator, and NVIDIA Isaac Sim, AND MORE having github link of my page
RESPONSE_TEXT: |
  I have completed the requested changes to the footer in `my-website/docusaurus.config.ts`.
outcome: The Docusaurus footer was successfully customized to include new sections for "TEXTBOOK," "RESOURCES," and "MORE," with appropriate links.
evaluation: The agent successfully identified and updated the footer configuration in `docusaurus.config.ts` to include all requested links and sections, using placeholders where necessary and providing clear instructions for the user to update.
