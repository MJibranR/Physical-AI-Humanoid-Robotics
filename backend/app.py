# app.py
import os
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Set env config
GENIE_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GENIE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "textbook_chunks")

if GENIE_API_KEY:
    genai.configure(api_key=GENIE_API_KEY)

# -- Paste your full KNOWLEDGE_BASE here (copy from your existing code) --
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
# -- end KB --

app = FastAPI(title="Physical AI RAG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy global for embedding model
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        # lazy import to avoid loading on startup
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return _embedding_model

# Simple in-memory vector store (builds on start)
class InMemoryVectorStore:
    def __init__(self, kb):
        self.documents = kb
        self.embeddings = []
        self._build()

    def _get_embedding(self, text: str):
        # Prefer Gemini embeddings if available
        if GENIE_API_KEY:
            try:
                res = genai.embed_content(model="models/text-embedding-004", content=text, task_type="retrieval_document")
                return res["embedding"]
            except Exception as e:
                print("Gemini embedding failed:", e)
        # fallback to local model
        model = get_embedding_model()
        return model.encode(text, convert_to_tensor=False).tolist()

    def _build(self):
        for d in self.documents:
            emb = self._get_embedding(d["content"])
            self.embeddings.append(emb)

    def search(self, query: str, top_k: int = 3):
        q_emb = self._get_embedding(query)
        sims = []
        for emb in self.embeddings:
            try:
                sim = float(cosine_similarity([q_emb], [emb])[0][0])
            except Exception:
                sim = 0.0
            sims.append(sim)
        idxs = np.argsort(sims)[-top_k:][::-1]
        return [{"document": self.documents[i], "score": float(sims[i])} for i in idxs]

vector_store = InMemoryVectorStore(KNOWLEDGE_BASE)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict] = []

@app.get("/")
async def root():
    return {"message": "Physical AI Humanoid Robotics RAG Backend", "version": "2.0"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    try:
        search_results = vector_store.search(req.message, top_k=3)
        context = "\n\n".join([f"[Source: {r['document']['title']}]\n{r['document']['content']}" for r in search_results])

        if GENIE_API_KEY:
            prompt = f"""You are an expert assistant for Physical AI and Humanoid Robotics.
Use the context below to answer the user concisely and cite sources when helpful.

Context:
{context}

User question: {req.message}

Answer:"""
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            gen = model.generate_content(prompt)
            answer = gen.text
        else:
            answer = f"Context used:\n{context}\n\n(no Gemini API configured)"

        sources = [{"title": r["document"]["title"], "relevance_score": round(r["score"], 3)} for r in search_results]
        return ChatResponse(response=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
