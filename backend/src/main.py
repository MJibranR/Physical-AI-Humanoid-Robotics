from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

app = FastAPI()

# Enhanced CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://physical-ai-humanoid-robotics-three.vercel.app",
        "https://www.physical-ai-humanoid-robotics-three.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Knowledge base from your textbook
KNOWLEDGE_BASE = [
    {
        "id": "intro_physical_ai",
        "title": "Introduction to Physical AI",
        "content": """Physical AI represents a transformative paradigm where intelligent systems are embodied within physical forms, enabling direct interaction with the real world. Key characteristics include:
        - Embodiment: AI housed within physical bodies (robots, drones, prosthetics)
        - Interaction: Continuous engagement through sensors and actuators
        - Autonomy: Independent decision-making and adaptation
        - Real-time Processing: High-speed data processing for dynamic environments
        
        Applications include industrial robotics, autonomous vehicles, healthcare robots, exploration in hazardous environments, and service robotics."""
    },
    {
        "id": "robotics_fundamentals",
        "title": "Robotics Fundamentals",
        "content": """Robotics fundamentals cover:
        
        Kinematics and Dynamics: Forward kinematics determines end-effector position from joint angles. Inverse kinematics calculates joint angles for desired positions. Dynamics relates motion to forces and torques.
        
        Sensors: Vision sensors (RGB, depth, stereo cameras), proprioceptive sensors (encoders, IMUs), proximity sensors (lidar, ultrasonic, infrared).
        
        Actuators: Motors (DC, servo, stepper), hydraulic/pneumatic systems for high-force applications.
        
        ROS (Robot Operating System): Framework providing tools, libraries, and conventions for robot software development."""
    },
    {
        "id": "ai_in_robotics",
        "title": "AI in Robotics",
        "content": """AI empowers robots with intelligence through:
        
        Machine Learning for Control: Reinforcement Learning (robots learn through trial and error), Imitation Learning (learning from human demonstrations).
        
        Computer Vision: Object detection (YOLO, R-CNN), semantic segmentation, 3D reconstruction, SLAM.
        
        Natural Language Processing: Speech recognition, natural language understanding, and generation for human-robot interaction."""
    },
    {
        "id": "humanoid_anatomy",
        "title": "Humanoid Robot Anatomy",
        "content": """Humanoid robots feature:
        
        Mechanical Design: Lightweight materials (aluminum alloys, carbon fiber), modular design, 20-60+ degrees of freedom for complex movements.
        
        Power Systems: High energy density batteries (Li-Po, Li-ion), efficient power distribution, thermal management.
        
        Communication: High-speed internal buses (EtherCAT, CAN), wireless technologies (Wi-Fi, Bluetooth, 5G) for external communication."""
    },
    {
        "id": "locomotion_balance",
        "title": "Locomotion and Balance",
        "content": """Bipedal locomotion concepts:
        
        Zero Moment Point (ZMP): Critical for stable walking - the point where the robot can apply force without generating angular momentum. ZMP must remain within the support polygon.
        
        Walking Gaits: Pattern generators create cyclic joint trajectories. Dynamic walking exploits robot dynamics for efficiency.
        
        Balance Control: Adjusting joint torques and foot placement to maintain stability.
        
        Advanced Control: Whole-body control, Model Predictive Control (MPC), Reinforcement Learning for robust gaits."""
    },
    {
        "id": "human_robot_interaction",
        "title": "Human-Robot Interaction",
        "content": """Effective HRI requires:
        
        Safe Interaction: Physical safety (compliant actuators, soft skins, collision detection), cognitive safety (predictable behavior), social safety (adhering to social norms).
        
        Gesture Recognition: Using computer vision and ML to interpret human gestures.
        
        Voice Commands: Automatic Speech Recognition (ASR) and Natural Language Understanding (NLU) for spoken language interaction."""
    },
    {
        "id": "ros2_fundamentals",
        "title": "ROS 2 Fundamentals",
        "content": """ROS 2 is an open-source framework for robot software with key concepts:
        
        Nodes: Smallest computation units performing specific tasks.
        Topics: Publish/subscribe messaging for asynchronous communication.
        Services: Synchronous request/reply mechanism.
        Actions: Long-running tasks with feedback and preemption.
        
        Key improvements over ROS 1: DDS integration, Quality of Service policies, multi-robot support, security (SROS 2), real-time capabilities, platform independence."""
    },
    {
        "id": "digital_twin",
        "title": "Digital Twin Simulation",
        "content": """Digital twins are virtual replicas of physical robots offering:
        
        Benefits: Cost reduction, accelerated development, enhanced safety, accessibility, reproducibility, synthetic data generation.
        
        Gazebo: Open-source 3D simulator with robust physics, sensor simulation, deep ROS integration.
        
        NVIDIA Isaac Sim: High-fidelity physics (PhysX 5), photorealistic rendering (RTX), powerful synthetic data generation, scalability for large multi-robot simulations."""
    },
    {
        "id": "vla_systems",
        "title": "Vision-Language-Action Systems",
        "content": """VLA systems bridge visual perception, language understanding, and physical action:
        
        Vision Component: Object detection, segmentation, pose estimation, scene understanding.
        
        Language Component: Understanding commands, generating responses, grounding linguistic concepts to physical referents.
        
        Action Component: Task planning, motion planning, control execution, manipulation.
        
        Applications: Service robotics, industrial automation, exploration, personal assistants, education."""
    },
    {
        "id": "ethics",
        "title": "Ethical Considerations",
        "content": """Key ethical considerations in robotics:
        
        AI Ethics: Addressing bias in algorithms, establishing accountability, ensuring transparency in decision-making.
        
        Privacy and Security: Managing data collection concerns, protecting against cybersecurity threats.
        
        Future Outlook: Integration into daily life, advancements in dexterity and mobility, sophisticated cognitive architectures."""
    }
]

class VectorStore:
    def __init__(self):
        self.embeddings = []
        self.documents = []
        self.model = genai.GenerativeModel("models/gemini-2.0-flash")
        self._initialize_embeddings()
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embeddings using Gemini's embedding model"""
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            # Fallback: simple bag-of-words representation
            return [hash(word) % 1000 for word in text.lower().split()[:100]]
    
    def _initialize_embeddings(self):
        """Pre-compute embeddings for all documents"""
        print("Initializing vector store with document embeddings...")
        for doc in KNOWLEDGE_BASE:
            embedding = self._get_embedding(doc["content"])
            self.embeddings.append(embedding)
            self.documents.append(doc)
        print(f"Initialized {len(self.documents)} documents in vector store")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for most relevant documents"""
        try:
            query_embedding = self._get_embedding(query)
            
            # Calculate cosine similarities
            similarities = []
            for doc_embedding in self.embeddings:
                similarity = cosine_similarity(
                    [query_embedding], 
                    [doc_embedding]
                )[0][0]
                similarities.append(similarity)
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                results.append({
                    "document": self.documents[idx],
                    "score": float(similarities[idx])
                })
            
            return results
        except Exception as e:
            print(f"Search error: {e}")
            # Fallback: return first 3 documents
            return [{"document": doc, "score": 0.5} for doc in self.documents[:top_k]]

# Initialize vector store
vector_store = VectorStore()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict] = []

@app.get("/")
async def root():
    return {
        "message": "Physical AI Humanoid Robotics RAG Backend",
        "version": "2.0",
        "features": ["RAG", "Vector Search", "Context-Aware Responses"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Physical AI Humanoid Robotics RAG System",
        "documents_indexed": len(KNOWLEDGE_BASE)
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        if not req.message or req.message.strip() == "":
            return ChatResponse(
                response="Please provide a message.",
                sources=[]
            )
        
        # Step 1: Retrieve relevant documents
        search_results = vector_store.search(req.message, top_k=3)
        
        # Step 2: Build context from retrieved documents
        context = "\n\n".join([
            f"[Source: {result['document']['title']}]\n{result['document']['content']}"
            for result in search_results
        ])
        
        # Step 3: Generate response with context
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        
        system_prompt = f"""You are an expert AI assistant specializing in Physical AI and Humanoid Robotics. 
You have access to a comprehensive textbook on the subject.

Your role is to:
1. Answer questions accurately based on the provided context
2. Be helpful, clear, and educational
3. Cite specific concepts from the context when relevant
4. If the question is outside the context, acknowledge it and provide general guidance
5. Use technical terms appropriately but explain them when necessary

Context from the textbook:
{context}

Guidelines:
- Always prioritize information from the context
- Be concise but thorough
- Use examples from the context when helpful
- If uncertain, acknowledge limitations
"""
        
        full_prompt = f"{system_prompt}\n\nUser Question: {req.message}\n\nAssistant Response:"
        
        response = model.generate_content(full_prompt)
        
        # Step 4: Prepare sources for frontend
        sources = [
            {
                "title": result['document']['title'],
                "relevance_score": round(result['score'], 3)
            }
            for result in search_results
        ]
        
        return ChatResponse(
            response=response.text,
            sources=sources
        )
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return ChatResponse(
            response=f"I apologize, but I encountered an error: {str(e)}. Please try again.",
            sources=[]
        )

@app.options("/api/chat")
async def options_chat():
    return {"message": "OK"}

@app.get("/api/documents")
async def list_documents():
    """List all documents in the knowledge base"""
    return {
        "total": len(KNOWLEDGE_BASE),
        "documents": [
            {"id": doc["id"], "title": doc["title"]}
            for doc in KNOWLEDGE_BASE
        ]
    }

@app.get("/api/document/{doc_id}")
async def get_document(doc_id: str):
    """Get a specific document by ID"""
    doc = next((d for d in KNOWLEDGE_BASE if d["id"] == doc_id), None)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)