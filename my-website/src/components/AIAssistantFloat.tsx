import React from 'react';
import AIAssistantFloat from './RAGChatbot/index';

export default function Root({children}) {
  return (
    <>
      {children}
      <AIAssistantFloat />
    </>
  );
}