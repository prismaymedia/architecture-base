"""
Similarity checker using OpenAI embeddings and GPT for semantic comparison.
"""

import json
from typing import List, Tuple
from openai import OpenAI
from .models import Idea, UserStory, SimilarityResult
from .config import config


class SimilarityChecker:
    """Check for semantic similarity between ideas and user stories."""
    
    def __init__(self):
        if not config.openai_api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
            )
        self.client = OpenAI(api_key=config.openai_api_key)
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text using OpenAI's embedding model.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        response = self.client.embeddings.create(
            model=config.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score between 0 and 1
        """
        import math
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def check_similarity_with_ai(
        self,
        idea: Idea,
        existing_item: UserStory | Idea
    ) -> Tuple[float, str]:
        """
        Use GPT to analyze semantic similarity and provide reasoning.
        
        Args:
            idea: The new idea to check
            existing_item: Existing user story or idea to compare against
            
        Returns:
            Tuple of (similarity_score, reasoning)
        """
        prompt = f"""Analiza si estas dos descripciones representan la misma idea o funcionalidad.

IDEA NUEVA:
Título: {idea.title}
Contexto: {idea.context}
Problema: {idea.problem}
Valor: {idea.value}

ELEMENTO EXISTENTE ({existing_item.id}):
{self._format_existing_item(existing_item)}

Por favor:
1. Determina si son duplicadas o muy similares (>80% similitud)
2. Da un score de similitud entre 0.0 y 1.0
3. Explica brevemente por qué son similares o diferentes

Responde en formato JSON:
{{
    "similarity_score": 0.85,
    "is_duplicate": true,
    "reason": "Ambas tratan sobre..."
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente experto en análisis de requerimientos de software. Tu tarea es identificar ideas duplicadas o muy similares en un backlog de producto."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return (
                float(result.get("similarity_score", 0.0)),
                result.get("reason", "")
            )
        except Exception as e:
            print(f"Error in AI similarity check: {e}")
            return (0.0, "Error al analizar similitud")
    
    def find_similar_items(
        self,
        idea: Idea,
        user_stories: List[UserStory],
        other_ideas: List[Idea] = None
    ) -> List[SimilarityResult]:
        """
        Find similar user stories or ideas for a given idea.
        
        Args:
            idea: The idea to check
            user_stories: List of existing user stories
            other_ideas: List of other ideas (optional, to check for duplicate ideas)
            
        Returns:
            List of SimilarityResult objects
        """
        results = []
        
        # Get embedding for the idea
        idea_embedding = self.get_embedding(idea.full_text)
        
        # Check against user stories
        for us in user_stories:
            us_embedding = self.get_embedding(us.full_text)
            similarity = self.cosine_similarity(idea_embedding, us_embedding)
            
            # If similarity is above a certain threshold, use AI for detailed analysis
            if similarity >= (config.similarity_threshold - 0.1):  # Check slightly below threshold
                ai_score, reason = self.check_similarity_with_ai(idea, us)
                is_duplicate = ai_score >= config.similarity_threshold
                
                results.append(SimilarityResult(
                    idea_id=idea.id,
                    similar_item_id=us.id,
                    similarity_score=ai_score,
                    is_duplicate=is_duplicate,
                    reason=reason
                ))
        
        # Check against other ideas if provided
        if other_ideas:
            for other_idea in other_ideas:
                if other_idea.id == idea.id:
                    continue
                
                other_embedding = self.get_embedding(other_idea.full_text)
                similarity = self.cosine_similarity(idea_embedding, other_embedding)
                
                if similarity >= (config.similarity_threshold - 0.1):
                    ai_score, reason = self.check_similarity_with_ai(idea, other_idea)
                    is_duplicate = ai_score >= config.similarity_threshold
                    
                    results.append(SimilarityResult(
                        idea_id=idea.id,
                        similar_item_id=other_idea.id,
                        similarity_score=ai_score,
                        is_duplicate=is_duplicate,
                        reason=reason
                    ))
        
        # Sort by similarity score (highest first)
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return results
    
    def _format_existing_item(self, item: UserStory | Idea) -> str:
        """Format existing item for comparison prompt."""
        if isinstance(item, UserStory):
            return f"""Título: {item.title}
Como: {item.as_a}
Quiero: {item.i_want}
Para: {item.so_that}
Criterios de Aceptación:
{chr(10).join(['- ' + ac.text for ac in item.acceptance_criteria[:5]])}"""
        else:  # Idea
            return f"""Título: {item.title}
Contexto: {item.context}
Problema: {item.problem}
Valor: {item.value}"""
