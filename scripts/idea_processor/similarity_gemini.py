"""
Similarity checker using Google Gemini API for semantic comparison.
"""

import json
from typing import List, Tuple
import google.generativeai as genai
from .models import Idea, UserStory, SimilarityResult
from .config import config


class GeminiSimilarityChecker:
    """Check for semantic similarity between ideas and user stories using Gemini."""
    
    def __init__(self):
        if not config.gemini_api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable."
            )
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.gemini_model)
    
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
        Use Gemini to analyze semantic similarity and provide reasoning.
        
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

Responde SOLO con un JSON válido (sin markdown ni texto adicional):
{{
    "similarity_score": 0.85,
    "is_duplicate": true,
    "reason": "Ambas tratan sobre..."
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            text = response.text.strip()
            # Remove markdown code blocks if present
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()
            
            result = json.loads(text)
            return (
                float(result.get("similarity_score", 0.0)),
                result.get("reason", "")
            )
        except Exception as e:
            print(f"Error in Gemini similarity check: {e}")
            return (0.0, "Error al analizar similitud")
    
    def find_similar_items(
        self,
        idea: Idea,
        user_stories: List[UserStory],
        other_ideas: List[Idea] = None
    ) -> List[SimilarityResult]:
        """
        Find similar user stories or ideas for a given idea using Gemini.
        
        Args:
            idea: The idea to check
            user_stories: List of existing user stories
            other_ideas: List of other ideas (optional, to check for duplicate ideas)
            
        Returns:
            List of SimilarityResult objects
        """
        results = []
        
        # Check against user stories
        for us in user_stories:
            # Use Gemini for detailed analysis
            ai_score, reason = self.check_similarity_with_ai(idea, us)
            
            # Only add if similarity is above a threshold
            if ai_score >= (config.similarity_threshold - 0.1):
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
                
                ai_score, reason = self.check_similarity_with_ai(idea, other_idea)
                
                if ai_score >= (config.similarity_threshold - 0.1):
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
