"""
Unit tests for Experience Bank (memory system).
Tests vector-based experience retrieval and management.
"""
import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from evolution_engine.memory.experience_bank import ExperienceBank


class TestExperienceBank:
    """Test the Experience Bank memory system."""

    def setup_method(self):
        """Setup experience bank before each test."""
        self.bank = ExperienceBank(
            embedding_dim=128,  # Smaller for testing
            max_experiences=100,
            retention_rate=0.8
        )

    def test_initialization(self):
        """Test that bank initializes correctly."""
        assert self.bank.embedding_dim == 128
        assert self.bank.max_experiences == 100
        assert len(self.bank.experiences) == 0

    def test_add_experience(self):
        """Test adding a new experience."""
        exp_id = self.bank.add_experience(
            task_description="Solve math problem",
            action_taken="Used calculator",
            outcome="success",
            lesson="Always double-check calculations",
            importance_score=0.8
        )

        assert exp_id == 0
        assert len(self.bank.experiences) == 1

        exp = self.bank.get_experience(exp_id)
        assert exp["task_description"] == "Solve math problem"
        assert exp["outcome"] == "success"
        assert exp["is_active"] is True

    def test_add_multiple_experiences(self):
        """Test adding multiple experiences."""
        for i in range(10):
            self.bank.add_experience(
                task_description=f"Task {i}",
                action_taken=f"Action {i}",
                outcome="success" if i % 2 == 0 else "failure",
                lesson=f"Lesson {i}",
                importance_score=float(i) / 10
            )

        assert len(self.bank.experiences) == 10

        stats = self.bank.get_statistics()
        assert stats["total_experiences"] == 10
        assert stats["active_experiences"] == 10
        assert stats["success_count"] == 5
        assert stats["failure_count"] == 5

    def test_search_similar(self):
        """Test similarity search."""
        # Add some experiences with known embeddings
        embedding1 = np.ones(128, dtype=np.float32)
        embedding2 = np.ones(128, dtype=np.float32) * -1
        embedding3 = np.ones(128, dtype=np.float32) * 0.5

        self.bank.add_experience(
            task_description="Task A",
            action_taken="Action A",
            outcome="success",
            lesson="Lesson A",
            embedding=embedding1
        )

        self.bank.add_experience(
            task_description="Task B",
            action_taken="Action B",
            outcome="success",
            lesson="Lesson B",
            embedding=embedding2
        )

        self.bank.add_experience(
            task_description="Task C",
            action_taken="Action C",
            outcome="success",
            lesson="Lesson C",
            embedding=embedding3
        )

        # Search with query similar to embedding1
        query_embedding = np.ones(128, dtype=np.float32)
        results = self.bank.search_similar("test query", query_embedding, top_k=2)

        assert len(results) == 2
        # First result should be most similar (Task A)
        assert results[0]["task_description"] == "Task A"

    def test_pin_experience(self):
        """Test pinning important experiences."""
        exp_id = self.bank.add_experience(
            task_description="Important task",
            action_taken="Critical action",
            outcome="success",
            lesson="Never forget this",
            importance_score=0.5
        )

        # Pin the experience
        self.bank.pin_experience(exp_id)

        exp = self.bank.get_experience(exp_id)
        assert exp["is_pinned"] is True
        assert exp["importance_score"] == 10.0

    def test_delete_experience(self):
        """Test deleting experiences."""
        exp_id = self.bank.add_experience(
            task_description="Bad experience",
            action_taken="Wrong action",
            outcome="failure",
            lesson="This was wrong"
        )

        # Delete the experience
        self.bank.delete_experience(exp_id)

        exp = self.bank.get_experience(exp_id)
        assert exp["is_active"] is False

        # Should not appear in active experiences
        active = self.bank.get_all_active()
        assert len(active) == 0

    def test_pruning(self):
        """Test that pruning works when bank is full."""
        # Add more than max_experiences
        for i in range(150):
            self.bank.add_experience(
                task_description=f"Task {i}",
                action_taken=f"Action {i}",
                outcome="success",
                lesson=f"Lesson {i}",
                importance_score=float(i) / 150
            )

        # Should have been pruned
        assert len(self.bank.experiences) <= 150

        # Higher importance experiences should be retained
        active = self.bank.get_all_active()
        assert len(active) > 0

    def test_pinned_experiences_not_pruned(self):
        """Test that pinned experiences are never pruned."""
        # Add experiences and pin some
        for i in range(10):
            exp_id = self.bank.add_experience(
                task_description=f"Task {i}",
                action_taken=f"Action {i}",
                outcome="success",
                lesson=f"Lesson {i}",
                importance_score=0.1  # Low importance
            )

            if i < 3:
                self.bank.pin_experience(exp_id)

        # Force pruning by adding many more experiences
        for i in range(100):
            self.bank.add_experience(
                task_description=f"Filler {i}",
                action_taken="Filler",
                outcome="success",
                lesson="Filler",
                importance_score=0.9  # High importance
            )

        # Pinned experiences should still be active
        for i in range(3):
            exp = self.bank.get_experience(i)
            assert exp["is_pinned"] is True
            assert exp["is_active"] is True

    def test_retrieval_statistics(self):
        """Test that retrieval statistics are tracked."""
        exp_id = self.bank.add_experience(
            task_description="Test task",
            action_taken="Test action",
            outcome="success",
            lesson="Test lesson"
        )

        exp = self.bank.get_experience(exp_id)
        assert exp["times_retrieved"] == 0
        assert exp["last_retrieved"] is None

        # Search for similar (which updates stats)
        self.bank.search_similar("test", top_k=1)

        exp = self.bank.get_experience(exp_id)
        assert exp["times_retrieved"] == 1
        assert exp["last_retrieved"] is not None

    def test_get_statistics(self):
        """Test statistics reporting."""
        # Add mixed experiences
        for i in range(20):
            self.bank.add_experience(
                task_description=f"Task {i}",
                action_taken=f"Action {i}",
                outcome="success" if i < 15 else "failure",
                lesson=f"Lesson {i}",
                importance_score=0.5
            )

        stats = self.bank.get_statistics()

        assert stats["total_experiences"] == 20
        assert stats["active_experiences"] == 20
        assert stats["success_count"] == 15
        assert stats["failure_count"] == 5
        assert 0 <= stats["avg_importance"] <= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
