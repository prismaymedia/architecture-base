"""
Main workflow orchestrator for processing ideas.
"""

import re
from typing import List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from .config import config
from .models import Idea, UserStory, SimilarityResult
from .parser import MarkdownParser, load_file_content, save_file_content
from .similarity import SimilarityChecker
from .generator import UserStoryGenerator


console = Console()


class IdeaProcessor:
    """Main processor for the idea workflow."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run or config.dry_run
        self.parser = MarkdownParser()
        self.similarity_checker = SimilarityChecker()
        self.generator = UserStoryGenerator()
        
        console.print("\n[bold cyan]🚀 Idea Processor Initialized[/bold cyan]\n")
        if self.dry_run:
            console.print("[yellow]⚠️  Running in DRY RUN mode - no files will be modified[/yellow]\n")
    
    def process_ideas(self) -> Tuple[List[Idea], List[UserStory]]:
        """
        Main workflow to process ideas.
        
        Returns:
            Tuple of (ideas_marked_as_duplicate, generated_user_stories)
        """
        console.print("[bold]Step 1:[/bold] Loading files...\n")
        
        # Load files
        ideas_content = load_file_content(config.ideas_file)
        backlog_content = load_file_content(config.backlog_file)
        
        # Parse ideas and user stories
        console.print("[bold]Step 2:[/bold] Parsing ideas and user stories...\n")
        ideas = self.parser.parse_ideas(ideas_content)
        user_stories = self.parser.parse_user_stories(backlog_content)
        
        console.print(f"✓ Found [green]{len(ideas)}[/green] ideas")
        console.print(f"✓ Found [green]{len(user_stories)}[/green] existing user stories\n")
        
        # Filter ideas that need processing (status "Por refinar")
        ideas_to_process = [
            idea for idea in ideas
            if "Por refinar" in idea.status or "💭" in idea.status
        ]
        
        console.print(f"📝 Ideas to process: [cyan]{len(ideas_to_process)}[/cyan]\n")
        
        if not ideas_to_process:
            console.print("[yellow]No ideas to process. All ideas are either converted or discarded.[/yellow]")
            return [], []
        
        # Check for duplicates
        console.print("[bold]Step 3:[/bold] Checking for duplicates...\n")
        duplicate_ideas = []
        unique_ideas = []
        
        for idea in ideas_to_process:
            console.print(f"Checking [cyan]{idea.id}[/cyan]: {idea.title}")
            
            similar_items = self.similarity_checker.find_similar_items(
                idea,
                user_stories,
                other_ideas=ideas
            )
            
            if similar_items and similar_items[0].is_duplicate:
                # Mark as duplicate
                duplicate_ideas.append(idea)
                idea.is_duplicate = True
                idea.similar_to = similar_items[0].similar_item_id
                idea.similarity_score = similar_items[0].similarity_score
                
                console.print(f"  ⚠️  [yellow]Duplicate found[/yellow] - Similar to {similar_items[0].similar_item_id} "
                            f"(score: {similar_items[0].similarity_score:.2f})")
                console.print(f"  └─ Reason: {similar_items[0].reason}\n")
            else:
                unique_ideas.append(idea)
                console.print(f"  ✓ [green]Unique idea[/green]\n")
        
        # Display summary
        self._display_duplicate_summary(duplicate_ideas)
        
        # Generate user stories from unique ideas
        if unique_ideas:
            console.print(f"\n[bold]Step 4:[/bold] Generating user stories from {len(unique_ideas)} unique ideas...\n")
            
            next_us_number = self.parser.get_next_us_number(backlog_content)
            generated_user_stories = []
            
            for idea in unique_ideas:
                console.print(f"Generating user story for [cyan]{idea.id}[/cyan]...")
                user_story = self.generator.generate_user_story(idea, next_us_number)
                generated_user_stories.append(user_story)
                console.print(f"  ✓ Generated [green]{user_story.id}[/green]: {user_story.title}\n")
                next_us_number += 1
            
            # Display generated user stories
            self._display_generated_stories(generated_user_stories)
        else:
            console.print("\n[yellow]No unique ideas to generate user stories from.[/yellow]")
            generated_user_stories = []
        
        # Update files
        if not self.dry_run:
            console.print("\n[bold]Step 5:[/bold] Updating files...\n")
            
            if duplicate_ideas:
                console.print("Marking duplicate ideas in IDEAS.md...")
                updated_ideas_content = self._mark_duplicates_in_ideas(
                    ideas_content,
                    duplicate_ideas
                )
                save_file_content(config.ideas_file, updated_ideas_content)
                console.print("  ✓ IDEAS.md updated\n")
            
            if generated_user_stories:
                console.print("Appending new user stories to BACKLOG.md...")
                updated_backlog_content = self._append_user_stories_to_backlog(
                    backlog_content,
                    generated_user_stories
                )
                save_file_content(config.backlog_file, updated_backlog_content)
                console.print("  ✓ BACKLOG.md updated\n")
            
            if generated_user_stories:
                console.print("Marking ideas as converted in IDEAS.md...")
                updated_ideas_content = self._mark_ideas_as_converted(
                    load_file_content(config.ideas_file),
                    unique_ideas,
                    generated_user_stories
                )
                save_file_content(config.ideas_file, updated_ideas_content)
                console.print("  ✓ IDEAS.md updated with conversion status\n")
        
        # Final summary
        self._display_final_summary(duplicate_ideas, generated_user_stories)
        
        return duplicate_ideas, generated_user_stories
    
    def _mark_duplicates_in_ideas(self, content: str, duplicate_ideas: List[Idea]) -> str:
        """Mark duplicate ideas in IDEAS.md content."""
        for idea in duplicate_ideas:
            # Find the idea section and update its status
            pattern = rf'(###\s+\[{re.escape(idea.id)}\][^\n]+\n.*?)\*\*Estado\*\*:\s+[^\n]+'
            replacement = rf'\1**Estado**: ⚠️ Repetida - Similar a {idea.similar_to} (similitud: {idea.similarity_score:.0%})'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        return content
    
    def _mark_ideas_as_converted(
        self,
        content: str,
        ideas: List[Idea],
        user_stories: List[UserStory]
    ) -> str:
        """Mark ideas as converted to user stories in IDEAS.md."""
        idea_to_us_map = {idea.id: us.id for idea, us in zip(ideas, user_stories)}
        
        for idea_id, us_id in idea_to_us_map.items():
            # Find the idea section and update its status
            pattern = rf'(###\s+\[{re.escape(idea_id)}\][^\n]+\n.*?)\*\*Estado\*\*:\s+[^\n]+'
            replacement = rf'\1**Estado**: ✅ Convertida a {us_id}'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        return content
    
    def _append_user_stories_to_backlog(
        self,
        content: str,
        user_stories: List[UserStory]
    ) -> str:
        """Append new user stories to BACKLOG.md."""
        # Find the appropriate section based on priority
        for us in user_stories:
            us_markdown = us.to_markdown()
            
            # Determine which priority section to add to
            if "Alta 🔴" in us.priority or "🔴" in us.priority:
                section_marker = "### 🔴 Prioridad Alta - Crítico"
            elif "Media 🟡" in us.priority or "🟡" in us.priority:
                section_marker = "### 🟡 Prioridad Media - Importante"
            else:
                section_marker = "### 🟢 Prioridad Baja - Mejoras"
            
            # Find the section and insert after it
            section_pos = content.find(section_marker)
            if section_pos != -1:
                # Find the next line after the section header
                next_line_pos = content.find('\n', section_pos) + 1
                # Insert the user story
                content = content[:next_line_pos] + '\n' + us_markdown + '\n' + content[next_line_pos:]
        
        return content
    
    def _display_duplicate_summary(self, duplicate_ideas: List[Idea]):
        """Display table of duplicate ideas."""
        if not duplicate_ideas:
            return
        
        table = Table(title="⚠️  Duplicate Ideas Found", show_header=True, header_style="bold yellow")
        table.add_column("Idea ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Similar To", style="yellow")
        table.add_column("Similarity", justify="right", style="red")
        
        for idea in duplicate_ideas:
            table.add_row(
                idea.id,
                idea.title[:50] + "..." if len(idea.title) > 50 else idea.title,
                idea.similar_to or "",
                f"{idea.similarity_score:.0%}" if idea.similarity_score else ""
            )
        
        console.print("\n")
        console.print(table)
        console.print("\n")
    
    def _display_generated_stories(self, user_stories: List[UserStory]):
        """Display table of generated user stories."""
        if not user_stories:
            return
        
        table = Table(title="✨ Generated User Stories", show_header=True, header_style="bold green")
        table.add_column("US ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Priority", style="yellow")
        table.add_column("Story Points", justify="center", style="magenta")
        table.add_column("Epic", style="blue")
        
        for us in user_stories:
            table.add_row(
                us.id,
                us.title[:40] + "..." if len(us.title) > 40 else us.title,
                us.priority,
                str(us.estimation) if us.estimation else "-",
                us.epic or "-"
            )
        
        console.print("\n")
        console.print(table)
        console.print("\n")
    
    def _display_final_summary(
        self,
        duplicate_ideas: List[Idea],
        generated_user_stories: List[UserStory]
    ):
        """Display final summary."""
        summary_text = f"""
[bold cyan]📊 Processing Complete![/bold cyan]

[yellow]Duplicate Ideas Found:[/yellow] {len(duplicate_ideas)}
[green]New User Stories Generated:[/green] {len(generated_user_stories)}

[bold]Next Steps:[/bold]
1. Review the generated user stories in BACKLOG.md
2. Check marked duplicate ideas in IDEAS.md
3. Refine user stories as needed
4. Move approved stories to appropriate Kanban state
"""
        
        console.print(Panel(summary_text, title="Summary", border_style="green"))
