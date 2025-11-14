"""
User story generator using Google Gemini API - converts ideas into formal user stories.
"""

import json
from typing import List
import google.generativeai as genai
from .models import Idea, UserStory, AcceptanceCriteria
from .config import config
from .parser import MarkdownParser


class GeminiUserStoryGenerator:
    """Generate formal user stories from ideas using Gemini."""
    
    def __init__(self):
        if not config.gemini_api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable."
            )
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.gemini_model)
    
    def generate_user_story(
        self,
        idea: Idea,
        next_us_number: int,
        backlog_template: str = ""
    ) -> UserStory:
        """
        Generate a formal user story from an idea using Gemini.
        
        Args:
            idea: The idea to convert
            next_us_number: The next available US number
            backlog_template: Optional template content for reference
            
        Returns:
            Generated UserStory object
        """
        prompt = f"""Eres un Product Owner experto. Tu tarea es convertir una idea en una historia de usuario formal y bien estructurada.

IDEA A CONVERTIR:
ID: {idea.id}
Título: {idea.title}
Contexto: {idea.context}
Problema: {idea.problem}
Valor: {idea.value}
Prioridad Original: {idea.priority}

FORMATO REQUERIDO:
Genera una historia de usuario siguiendo este formato:

1. **Título**: Breve y descriptivo
2. **Como** [tipo de usuario]: Identifica quién necesita esta funcionalidad
3. **Quiero** [acción/objetivo]: Qué quiere hacer el usuario
4. **Para** [beneficio]: Por qué es valioso

5. **Criterios de Aceptación** (4-6 criterios):
   - Específicos y medibles
   - Orientados al comportamiento esperado
   - Sin detalles técnicos de implementación
   
6. **Estimación**: Story points (1, 2, 3, 5, 8, 13)
   - 1-2: Cambios triviales o muy simples
   - 3: Feature pequeña
   - 5: Feature moderada
   - 8: Feature compleja
   - 13: Feature muy compleja (considerar dividir)

7. **Epic**: Categoriza la historia (ej: Gestión de Pedidos, Procesamiento de Pagos, etc.)

8. **Servicios Afectados**: Lista de microservicios que necesitan cambios

9. **Notas Técnicas** (2-4 notas):
   - Eventos a publicar/consumir
   - Patrones arquitectónicos recomendados
   - Integraciones necesarias
   - Consideraciones de seguridad

Responde SOLO con un JSON válido (sin markdown ni texto adicional):
{{
    "title": "Título descriptivo",
    "as_a": "tipo de usuario",
    "i_want": "acción u objetivo",
    "so_that": "beneficio o razón",
    "acceptance_criteria": [
        "Criterio 1",
        "Criterio 2",
        "Criterio 3",
        "Criterio 4"
    ],
    "estimation": 5,
    "epic": "Nombre del Epic",
    "priority": "Alta 🔴",
    "affected_services": ["Service1 API", "Service2 API"],
    "technical_notes": [
        "Nota técnica 1",
        "Nota técnica 2"
    ]
}}

IMPORTANTE:
- Mantén la prioridad original de la idea: {idea.priority}
- Los criterios de aceptación deben ser claros y verificables
- La estimación debe ser realista basada en la complejidad
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
            
            # Convert to UserStory object
            acceptance_criteria = [
                AcceptanceCriteria(text=ac, completed=False)
                for ac in result.get("acceptance_criteria", [])
            ]
            
            user_story = UserStory(
                id=f"US-{next_us_number:03d}",
                title=result.get("title", idea.title),
                as_a=result.get("as_a", ""),
                i_want=result.get("i_want", ""),
                so_that=result.get("so_that", ""),
                acceptance_criteria=acceptance_criteria,
                estimation=result.get("estimation"),
                epic=result.get("epic"),
                priority=result.get("priority", idea.priority),
                affected_services=result.get("affected_services", []),
                dependencies=[],
                status="To Do",
                technical_notes=result.get("technical_notes", [])
            )
            
            # Build full text for the user story
            user_story.full_text = f"{user_story.title} {user_story.as_a} {user_story.i_want} {user_story.so_that}"
            
            return user_story
            
        except Exception as e:
            print(f"Error generating user story with Gemini: {e}")
            # Return a basic user story if AI generation fails
            return self._create_fallback_user_story(idea, next_us_number)
    
    def _create_fallback_user_story(self, idea: Idea, next_us_number: int) -> UserStory:
        """Create a basic user story if AI generation fails."""
        return UserStory(
            id=f"US-{next_us_number:03d}",
            title=idea.title,
            as_a="usuario del sistema",
            i_want=f"implementar la siguiente idea: {idea.title}",
            so_that=idea.value,
            acceptance_criteria=[
                AcceptanceCriteria(text=f"Resuelve el problema: {idea.problem}", completed=False),
                AcceptanceCriteria(text=f"Proporciona el valor: {idea.value}", completed=False)
            ],
            estimation=5,
            epic="Por Definir",
            priority=idea.priority,
            affected_services=[],
            dependencies=[],
            status="To Do",
            technical_notes=[
                f"Esta historia fue generada automáticamente desde {idea.id}",
                "Requiere refinamiento manual"
            ]
        )
    
    def generate_multiple_user_stories(
        self,
        ideas: List[Idea],
        starting_us_number: int
    ) -> List[UserStory]:
        """
        Generate user stories for multiple ideas.
        
        Args:
            ideas: List of ideas to convert
            starting_us_number: Starting US number
            
        Returns:
            List of generated UserStory objects
        """
        user_stories = []
        
        for i, idea in enumerate(ideas):
            us_number = starting_us_number + i
            user_story = self.generate_user_story(idea, us_number)
            user_stories.append(user_story)
        
        return user_stories
