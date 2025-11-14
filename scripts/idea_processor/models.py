"""
Data models for ideas and user stories.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date


class Idea(BaseModel):
    """Represents an idea from IDEAS.md"""
    
    id: str  # e.g., "ID-001"
    title: str
    context: str
    problem: str
    value: str
    date_created: str
    status: str
    priority: str  # 🔴 Alta, 🟡 Media, 🟢 Baja, 💭 Por Definir
    
    # Additional fields for processing
    full_text: str = ""  # Complete text for similarity comparison
    is_duplicate: bool = False
    similar_to: Optional[str] = None  # Reference to similar US-XXX or ID-XXX
    similarity_score: Optional[float] = None
    
    def __str__(self) -> str:
        return f"{self.id}: {self.title}"


class AcceptanceCriteria(BaseModel):
    """Represents an acceptance criterion."""
    text: str
    completed: bool = False


class UserStory(BaseModel):
    """Represents a user story from BACKLOG.md"""
    
    id: str  # e.g., "US-001"
    title: str
    as_a: str  # "Como [role]"
    i_want: str  # "Quiero [action]"
    so_that: str  # "Para [benefit]"
    
    acceptance_criteria: List[AcceptanceCriteria] = Field(default_factory=list)
    estimation: Optional[int] = None  # Story points
    epic: Optional[str] = None
    priority: str = "Media 🟡"
    affected_services: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    status: str = "To Do"
    technical_notes: List[str] = Field(default_factory=list)
    
    # For similarity comparison
    full_text: str = ""
    
    def __str__(self) -> str:
        return f"{self.id}: {self.title}"
    
    def to_markdown(self) -> str:
        """Convert user story to markdown format."""
        lines = []
        lines.append(f"#### {self.id}: {self.title}")
        lines.append(f"**Como** {self.as_a}")
        lines.append(f"**Quiero** {self.i_want}")
        lines.append(f"**Para** {self.so_that}")
        lines.append("")
        lines.append("**Criterios de Aceptación:**")
        for ac in self.acceptance_criteria:
            checkbox = "[x]" if ac.completed else "[ ]"
            lines.append(f"- {checkbox} {ac.text}")
        lines.append("")
        
        if self.estimation:
            lines.append(f"**Estimación**: {self.estimation} Story Points")
        if self.epic:
            lines.append(f"**Epic**: {self.epic}")
        lines.append(f"**Prioridad**: {self.priority}")
        if self.affected_services:
            lines.append(f"**Servicios Afectados**: {', '.join(self.affected_services)}")
        if self.dependencies:
            deps = ', '.join(self.dependencies) if self.dependencies else "Ninguna"
            lines.append(f"**Dependencias**: {deps}")
        lines.append(f"**Estado**: {self.status}")
        
        if self.technical_notes:
            lines.append("")
            lines.append("**Notas Técnicas:**")
            for note in self.technical_notes:
                lines.append(f"- {note}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        return "\n".join(lines)


class SimilarityResult(BaseModel):
    """Result of similarity comparison."""
    
    idea_id: str
    similar_item_id: str  # US-XXX or ID-XXX
    similarity_score: float
    is_duplicate: bool
    reason: str  # Explanation of why it's similar
