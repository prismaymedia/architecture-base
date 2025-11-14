#!/usr/bin/env python3
"""
Command-line interface for the Idea Processor.

Usage:
    python -m scripts.idea_processor.cli [options]

Options:
    --dry-run: Run without modifying files (preview mode)
    --help: Show this help message
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.idea_processor.processor import IdeaProcessor
from scripts.idea_processor.config import config
from rich.console import Console


console = Console()


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Process ideas from IDEAS.md and generate user stories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process ideas and update files
  python -m scripts.idea_processor.cli

  # Preview what would happen without modifying files
  python -m scripts.idea_processor.cli --dry-run

  # Use custom threshold for similarity
  python -m scripts.idea_processor.cli --threshold 0.85

Environment Variables:
  OPENAI_API_KEY: Required - Your OpenAI API key for similarity checking
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.80,
        help='Similarity threshold for duplicates (0.0-1.0, default: 0.80)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Update config
    config.dry_run = args.dry_run
    config.similarity_threshold = args.threshold
    config.verbose = args.verbose
    
    # Validate OpenAI API key
    if not config.openai_api_key:
        console.print("\n[bold red]Error:[/bold red] OPENAI_API_KEY environment variable is not set.\n")
        console.print("Please set it with your OpenAI API key:")
        console.print("  export OPENAI_API_KEY='your-api-key-here'\n")
        sys.exit(1)
    
    # Validate files exist
    if not config.ideas_file.exists():
        console.print(f"\n[bold red]Error:[/bold red] IDEAS.md not found at {config.ideas_file}\n")
        sys.exit(1)
    
    if not config.backlog_file.exists():
        console.print(f"\n[bold red]Error:[/bold red] BACKLOG.md not found at {config.backlog_file}\n")
        sys.exit(1)
    
    try:
        # Run the processor
        processor = IdeaProcessor(dry_run=args.dry_run)
        duplicate_ideas, generated_stories = processor.process_ideas()
        
        console.print("\n[bold green]✅ Process completed successfully![/bold green]\n")
        
        if args.dry_run:
            console.print("[yellow]Note: This was a dry run. No files were modified.[/yellow]")
            console.print("[yellow]Run without --dry-run to apply changes.[/yellow]\n")
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Process interrupted by user.[/yellow]\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}\n")
        if args.verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
