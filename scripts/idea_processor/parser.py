"""
Parser for IDEAS.md and BACKLOG.md files.
"""

import re
from typing import List, Tuple
from pathlib import Path
from .models import Idea, UserStory, AcceptanceCriteria


class MarkdownParser:
    """Parser for extracting ideas and user stories from markdown files."""
    
    @staticmethod
    def parse_ideas(content: str) -> List[Idea]:
        """
        Parse IDEAS.md content and extract all ideas.
        
        Args:
            content: The content of IDEAS.md
            
        Returns:
            List of Idea objects
        """
        ideas = []
        
        # Pattern to match idea sections
        # Looking for: ### [ID-XXX] Title
        idea_pattern = r'###\s+\[([^\]]+)\]\s+([^\n]+)'
        
        # Find all idea sections
        idea_matches = list(re.finditer(idea_pattern, content))
        
        for i, match in enumerate(idea_matches):
            idea_id = match.group(1)
            title = match.group(2).strip()
            
            # Get the content between this idea and the next one (or end of section)
            start_pos = match.end()
            if i + 1 < len(idea_matches):
                end_pos = idea_matches[i + 1].start()
            else:
                # Find the next section header (##) or end of file
                next_section = re.search(r'\n##\s+', content[start_pos:])
                if next_section:
                    end_pos = start_pos + next_section.start()
                else:
                    end_pos = len(content)
            
            idea_content = content[start_pos:end_pos].strip()
            
            # Extract fields
            context = MarkdownParser._extract_field(idea_content, "Contexto")
            problem = MarkdownParser._extract_field(idea_content, "Problema")
            value = MarkdownParser._extract_field(idea_content, "Valor")
            date_created = MarkdownParser._extract_field(idea_content, "Fecha")
            status = MarkdownParser._extract_field(idea_content, "Estado")
            
            # Determine priority based on section
            priority = MarkdownParser._determine_priority_from_position(content, match.start())
            
            # Build full text for similarity comparison
            full_text = f"{title} {context} {problem} {value}"
            
            idea = Idea(
                id=idea_id,
                title=title,
                context=context,
                problem=problem,
                value=value,
                date_created=date_created,
                status=status,
                priority=priority,
                full_text=full_text
            )
            
            ideas.append(idea)
        
        return ideas
    
    @staticmethod
    def parse_user_stories(content: str) -> List[UserStory]:
        """
        Parse BACKLOG.md content and extract all user stories.
        
        Args:
            content: The content of BACKLOG.md
            
        Returns:
            List of UserStory objects
        """
        user_stories = []
        
        # Pattern to match user story sections
        # Looking for: #### US-XXX: Title
        us_pattern = r'####\s+(US-\d+):\s+([^\n]+)'
        
        # Find all user story sections
        us_matches = list(re.finditer(us_pattern, content))
        
        for i, match in enumerate(us_matches):
            us_id = match.group(1)
            title = match.group(2).strip()
            
            # Get the content between this US and the next one
            start_pos = match.end()
            if i + 1 < len(us_matches):
                end_pos = us_matches[i + 1].start()
            else:
                # Find next major section or end of file
                next_section = re.search(r'\n###\s+', content[start_pos:])
                if next_section:
                    end_pos = start_pos + next_section.start()
                else:
                    end_pos = len(content)
            
            us_content = content[start_pos:end_pos].strip()
            
            # Extract "Como... Quiero... Para..." pattern
            as_a_match = re.search(r'\*\*Como\*\*\s+([^\n]+)', us_content)
            i_want_match = re.search(r'\*\*Quiero\*\*\s+([^\n]+)', us_content)
            so_that_match = re.search(r'\*\*Para\*\*\s+([^\n]+)', us_content)
            
            as_a = as_a_match.group(1).strip() if as_a_match else ""
            i_want = i_want_match.group(1).strip() if i_want_match else ""
            so_that = so_that_match.group(1).strip() if so_that_match else ""
            
            # Extract acceptance criteria
            acceptance_criteria = MarkdownParser._extract_acceptance_criteria(us_content)
            
            # Extract other fields
            estimation_match = re.search(r'\*\*Estimación\*\*:\s+(\d+)\s+Story Points', us_content)
            estimation = int(estimation_match.group(1)) if estimation_match else None
            
            epic_match = re.search(r'\*\*Epic\*\*:\s+([^\n]+)', us_content)
            epic = epic_match.group(1).strip() if epic_match else None
            
            priority = MarkdownParser._determine_priority_from_position(content, match.start())
            
            services_match = re.search(r'\*\*Servicios Afectados\*\*:\s+([^\n]+)', us_content)
            affected_services = []
            if services_match:
                services_text = services_match.group(1).strip()
                affected_services = [s.strip() for s in services_text.split(',')]
            
            deps_match = re.search(r'\*\*Dependencias\*\*:\s+([^\n]+)', us_content)
            dependencies = []
            if deps_match:
                deps_text = deps_match.group(1).strip()
                if deps_text.lower() != "ninguna":
                    dependencies = [d.strip() for d in deps_text.split(',')]
            
            status_match = re.search(r'\*\*Estado\*\*:\s+([^\n]+)', us_content)
            status = status_match.group(1).strip() if status_match else "To Do"
            
            # Extract technical notes
            technical_notes = MarkdownParser._extract_technical_notes(us_content)
            
            # Build full text for similarity comparison
            full_text = f"{title} {as_a} {i_want} {so_that} {' '.join([ac.text for ac in acceptance_criteria])}"
            
            user_story = UserStory(
                id=us_id,
                title=title,
                as_a=as_a,
                i_want=i_want,
                so_that=so_that,
                acceptance_criteria=acceptance_criteria,
                estimation=estimation,
                epic=epic,
                priority=priority,
                affected_services=affected_services,
                dependencies=dependencies,
                status=status,
                technical_notes=technical_notes,
                full_text=full_text
            )
            
            user_stories.append(user_story)
        
        return user_stories
    
    @staticmethod
    def _extract_field(content: str, field_name: str) -> str:
        """Extract a field value from markdown content."""
        pattern = rf'\*\*{field_name}\*\*:\s+([^\n]+)'
        match = re.search(pattern, content)
        if match:
            return match.group(1).strip()
        
        # Try with dash format: - **Field**: value
        pattern = rf'-\s+\*\*{field_name}\*\*:\s+([^\n]+)'
        match = re.search(pattern, content)
        if match:
            return match.group(1).strip()
        
        return ""
    
    @staticmethod
    def _extract_acceptance_criteria(content: str) -> List[AcceptanceCriteria]:
        """Extract acceptance criteria from user story content."""
        criteria = []
        
        # Find the acceptance criteria section
        ac_section_match = re.search(
            r'\*\*Criterios de Aceptación\*\*:?\s*\n((?:- \[.\].*\n?)*)',
            content,
            re.MULTILINE
        )
        
        if ac_section_match:
            ac_text = ac_section_match.group(1)
            # Find all checkbox items
            ac_items = re.findall(r'- \[(.)\]\s+([^\n]+)', ac_text)
            for checkbox, text in ac_items:
                completed = checkbox.lower() == 'x'
                criteria.append(AcceptanceCriteria(text=text.strip(), completed=completed))
        
        return criteria
    
    @staticmethod
    def _extract_technical_notes(content: str) -> List[str]:
        """Extract technical notes from user story content."""
        notes = []
        
        # Find the technical notes section
        notes_section_match = re.search(
            r'\*\*Notas Técnicas\*\*:?\s*\n((?:- .*\n?)*)',
            content,
            re.MULTILINE
        )
        
        if notes_section_match:
            notes_text = notes_section_match.group(1)
            # Find all list items
            note_items = re.findall(r'- ([^\n]+)', notes_text)
            notes = [note.strip() for note in note_items]
        
        return notes
    
    @staticmethod
    def _determine_priority_from_position(content: str, position: int) -> str:
        """
        Determine priority based on which section the item is in.
        Looks backwards from the position to find the priority section header.
        """
        content_before = content[:position]
        
        # Look for priority headers in reverse order
        if "🔴" in content_before.split('\n')[-20:]:  # Check last 20 lines
            return "Alta 🔴"
        elif "## 🔴" in content_before[-500:]:
            return "Alta 🔴"
        elif "🟡" in content_before.split('\n')[-20:]:
            return "Media 🟡"
        elif "## 🟡" in content_before[-500:]:
            return "Media 🟡"
        elif "🟢" in content_before.split('\n')[-20:]:
            return "Baja 🟢"
        elif "## 🟢" in content_before[-500:]:
            return "Baja 🟢"
        
        return "Media 🟡"  # Default
    
    @staticmethod
    def get_next_us_number(backlog_content: str) -> int:
        """Get the next available US number from backlog."""
        us_pattern = r'US-(\d+)'
        matches = re.findall(us_pattern, backlog_content)
        if matches:
            numbers = [int(m) for m in matches]
            return max(numbers) + 1
        return 1
    
    @staticmethod
    def get_next_id_number(ideas_content: str) -> int:
        """Get the next available ID number from ideas file."""
        id_pattern = r'ID-(\d+)'
        matches = re.findall(id_pattern, ideas_content)
        if matches:
            numbers = [int(m) for m in matches]
            return max(numbers) + 1
        return 1


def load_file_content(file_path: Path) -> str:
    """Load content from a file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def save_file_content(file_path: Path, content: str) -> None:
    """Save content to a file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
