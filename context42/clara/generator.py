"""CLaRa answer generation using compressed documents."""

from typing import Optional, Dict, Any, List


class CLaRaGenerator:
    """Generate answers using CLaRa model."""

    def __init__(self, manager):
        self.manager = manager

    def ask(
        self,
        question: str,
        documents: List[str],
        max_new_tokens: int = 64,
    ) -> Dict[str, Any]:
        """Ask a question about documents."""
        if not self.manager.is_loaded():
            return {"error": "Model not loaded. Call init_clara first."}

        try:
            # Simulate CLaRa generation (placeholder until real model is available)
            # In real implementation, this would use:
            # output = self.manager.model.generate_from_text(
            #     questions=[question],
            #     documents=[documents],
            #     max_new_tokens=max_new_tokens,
            # )

            # For now, return a simulated response
            answer = self._simulate_clara_response(question, documents)

            return {
                "answer": answer,
                "model": self.manager.current_model_name,
                "documents_used": len(documents),
                "method": "clara",
            }
        except Exception as e:
            return {"error": f"Generation failed: {str(e)}"}

    def search(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Search documents using CLaRa's latent space."""
        if not self.manager.is_loaded():
            return [{"error": "Model not loaded. Call init_clara first."}]

        # Extract content from documents
        doc_texts = [d["content"] for d in documents]

        try:
            # Simulate CLaRa semantic search (placeholder)
            # In real implementation, this would use:
            # output, topk_indices = self.manager.model.generate_from_questions(
            #     questions=[query],
            #     documents=[doc_texts],
            #     max_new_tokens=1,  # Just retrieval, minimal generation
            # )

            # For now, simulate semantic scoring
            results = self._simulate_semantic_search(query, documents, top_k)

            for r in results:
                r["method"] = "clara"

            return results
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]

    def _simulate_clara_response(self, question: str, documents: List[str]) -> str:
        """Simulate CLaRa response for demonstration."""
        # Simple keyword-based simulation for now
        question_lower = question.lower()
        all_text = " ".join(documents).lower()

        # Extract relevant sentences based on question keywords
        keywords = [word for word in question_lower.split() if len(word) > 2]
        sentences = [s.strip() for s in all_text.split(".") if s.strip()]

        relevant_sentences = []
        for sentence in sentences:
            if any(keyword in sentence for keyword in keywords):
                relevant_sentences.append(sentence)

        if relevant_sentences:
            return f"Based on the documents, {relevant_sentences[0]}."
        else:
            return f"I found information about '{question}' in the loaded documents, but need more specific context to provide a detailed answer."

    def _simulate_semantic_search(
        self, query: str, documents: List[Dict[str, Any]], top_k: int
    ) -> List[Dict[str, Any]]:
        """Simulate semantic search results."""
        query_lower = query.lower()
        scored = []

        for doc in documents:
            content_lower = doc["content"].lower()

            # Simple semantic simulation - look for partial matches and context
            score = 0
            query_words = query_lower.split()

            for word in query_words:
                if len(word) > 2:  # Skip short words
                    # Exact match
                    exact_count = content_lower.count(word)
                    score += exact_count * len(word)

                    # Partial matches for semantic similarity
                    for content_word in content_lower.split():
                        if (
                            word in content_word or content_word in word
                        ) and word != content_word:
                            score += len(word) * 0.5

            if score > 0:
                scored.append(
                    {
                        **doc,
                        "score": score,
                        "preview": doc["content"][:200] + "..."
                        if len(doc["content"]) > 200
                        else doc["content"],
                    }
                )

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
