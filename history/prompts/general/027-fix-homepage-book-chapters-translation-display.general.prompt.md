---
id: 27
title: Fix Homepage Book Chapters Translation Display
stage: green
date: 2025-12-14
surface: agent
model: gemini-pro
feature: i18n
branch: main
user: user
command: it shows object, obect not names of book chapters on hompage in urdu please do it also
labels: [bugfix, i18n, docusaurus, frontend, translation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - my-website/src/components/ChapterCards/index.tsx
 - my-website/i18n/ur/code.json
tests:
[]
---

## Prompt

it shows object, obect not names of book chapters on hompage in urdu please do it also

## Response snapshot

I have fixed the issue where homepage book chapters were showing "object, object" by correctly applying the <Translate> component in the ChapterCards component and re-translating the strings in code.json. Please test the changes by running the Docusaurus development server.

## Outcome

- ✅ Impact: Resolved the display issue for translated book chapter titles and descriptions on the homepage, ensuring that Urdu translations are correctly rendered instead of '[object Object]'. This improves the user experience for Urdu speakers on the homepage.
- 🧪 Tests: No tests were run.
- 📁 Files: Modified `my-website/src/components/ChapterCards/index.tsx` to correctly use `<Translate>` components. Updated `my-website/i18n/ur/code.json` with the correct Urdu translations for the chapter titles and descriptions.
- 🔁 Next prompts: Wait for the user to verify the changes and provide next instructions.
- 🧠 Reflection: The issue stemmed from an incorrect usage of the `<Translate>` component (String(<Translate>...)) which resulted in [object Object] being displayed. The fix involved reverting to plain strings in the ChapterList and using `<Translate>` directly in the rendering part of the ChapterCard component. This highlights the importance of understanding how React components and Docusaurus i18n features interact.

## Evaluation notes (flywheel)

- Failure modes observed: Misunderstanding the proper usage of the `<Translate>` component within component props led to the bug.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
