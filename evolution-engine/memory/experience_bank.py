"""
Experience Memory Bank - Implements AgentEvolver's Self-Navigating mechanism.
Uses vector embeddings for similarity-based retrieval.
"""
from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime


class ExperienceBank:
    """
    Vector-based experience memory for agents.

    Features:
    - Stores lessons learned from successes and failures
    - Vector similarity search for relevant experience retrieval
    - Importance scoring and decay
    - Human-in-the-loop curation (pin/delete)
    """

    def __init__(
        self,
        embedding_dim: int = 1536,  # OpenAI embedding dimension
        max_experiences: int = 10000,
        retention_rate: float = 0.9,
    ):
        """
        Initialize experience bank.

        Args:
            embedding_dim: Dimension of embedding vectors
            max_experiences: Maximum number of experiences to store
            retention_rate: Fraction of experiences to keep when pruning
        """
        self.embedding_dim = embedding_dim
        self.max_experiences = max_experiences
        self.retention_rate = retention_rate

        # In-memory storage (in production, would use pgvector)
        self.experiences: List[Dict[str, Any]] = []

    def add_experience(
        self,
        task_description: str,
        action_taken: str,
        outcome: str,
        lesson: str,
        embedding: Optional[np.ndarray] = None,
        importance_score: float = 1.0,
        metadata: Optional[Dict] = None,
    ) -> int:
        """
        Add a new experience to the bank.

        Args:
            task_description: Description of the task attempted
            action_taken: What the agent did
            outcome: "success" or "failure"
            lesson: Natural language lesson learned
            embedding: Vector embedding of the lesson
            importance_score: How important this lesson is
            metadata: Additional metadata

        Returns:
            Experience ID
        """
        experience_id = len(self.experiences)

        # Generate embedding if not provided
        if embedding is None:
            # TODO: Call embedding API (OpenAI, etc.)
            # For now, use random embedding
            embedding = np.random.randn(self.embedding_dim).astype(np.float32)

        experience = {
            "id": experience_id,
            "task_description": task_description,
            "action_taken": action_taken,
            "outcome": outcome,
            "lesson": lesson,
            "embedding": embedding,
            "importance_score": importance_score,
            "times_retrieved": 0,
            "last_retrieved": None,
            "created_at": datetime.utcnow(),
            "is_pinned": False,
            "is_active": True,
            "metadata": metadata or {},
        }

        self.experiences.append(experience)

        # Prune if exceeding max size
        if len(self.experiences) > self.max_experiences:
            self._prune_experiences()

        return experience_id

    def search_similar(
        self, query: str, query_embedding: Optional[np.ndarray] = None, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar experiences using vector similarity.

        Args:
            query: Text query describing current situation
            query_embedding: Optional pre-computed embedding
            top_k: Number of results to return

        Returns:
            List of most similar experiences
        """
        if query_embedding is None:
            # TODO: Generate embedding for query
            query_embedding = np.random.randn(self.embedding_dim).astype(np.float32)

        # Calculate cosine similarity with all active experiences
        similarities = []

        for exp in self.experiences:
            if not exp["is_active"]:
                continue

            # Cosine similarity
            exp_emb = exp["embedding"]
            similarity = np.dot(query_embedding, exp_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(exp_emb)
            )

            # Boost pinned experiences
            if exp["is_pinned"]:
                similarity *= 1.5

            similarities.append((similarity, exp))

        # Sort by similarity
        similarities.sort(key=lambda x: x[0], reverse=True)

        # Get top K
        top_experiences = [exp for _, exp in similarities[:top_k]]

        # Update retrieval stats
        for exp in top_experiences:
            exp["times_retrieved"] += 1
            exp["last_retrieved"] = datetime.utcnow()

        return top_experiences

    def pin_experience(self, experience_id: int):
        """Pin an important experience (human curation)."""
        if 0 <= experience_id < len(self.experiences):
            self.experiences[experience_id]["is_pinned"] = True
            self.experiences[experience_id]["importance_score"] = 10.0  # Max importance

    def delete_experience(self, experience_id: int):
        """Delete a bad experience (human curation)."""
        if 0 <= experience_id < len(self.experiences):
            self.experiences[experience_id]["is_active"] = False

    def get_experience(self, experience_id: int) -> Optional[Dict[str, Any]]:
        """Get experience by ID."""
        if 0 <= experience_id < len(self.experiences):
            return self.experiences[experience_id]
        return None

    def get_all_active(self) -> List[Dict[str, Any]]:
        """Get all active experiences."""
        return [exp for exp in self.experiences if exp["is_active"]]

    def _prune_experiences(self):
        """
        Remove low-quality experiences when bank is full.
        Implements experience decay.
        """
        # Never prune pinned experiences
        pinned = [exp for exp in self.experiences if exp["is_pinned"]]
        unpinned = [exp for exp in self.experiences if not exp["is_pinned"] and exp["is_active"]]

        # Sort unpinned by importance score
        unpinned.sort(key=lambda x: x["importance_score"], reverse=True)

        # Keep top percentage
        keep_count = int(len(self.experiences) * self.retention_rate) - len(pinned)
        kept_unpinned = unpinned[:keep_count]

        # Mark rest as inactive
        for exp in unpinned[keep_count:]:
            exp["is_active"] = False

        print(
            f"Pruned experience bank: kept {len(pinned) + len(kept_unpinned)} / {len(self.experiences)}"
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the experience bank."""
        active = self.get_all_active()
        successes = [e for e in active if e["outcome"] == "success"]
        failures = [e for e in active if e["outcome"] == "failure"]

        return {
            "total_experiences": len(self.experiences),
            "active_experiences": len(active),
            "pinned_experiences": len([e for e in active if e["is_pinned"]]),
            "success_count": len(successes),
            "failure_count": len(failures),
            "avg_importance": (
                np.mean([e["importance_score"] for e in active]) if active else 0.0
            ),
        }
