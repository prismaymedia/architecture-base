#!/usr/bin/env python3
"""
Validation script to test the idea processor without requiring OpenAI API key.
Tests basic functionality like parsing, data models, etc.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from scripts.idea_processor import config
        from scripts.idea_processor import models
        from scripts.idea_processor import parser
        print("✅ All core modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r scripts/idea_processor/requirements.txt")
        return False


def test_parser():
    """Test the markdown parser with sample data."""
    print("\nTesting parser...")
    try:
        from scripts.idea_processor.parser import MarkdownParser
        
        # Test idea parsing
        sample_ideas = """
### [ID-001] Test Idea

- **Contexto**: Test context
- **Problema**: Test problem
- **Valor**: Test value
- **Fecha**: 2025-11-14
- **Estado**: 💭 Por refinar
"""
        ideas = MarkdownParser.parse_ideas(sample_ideas)
        assert len(ideas) == 1, "Should parse 1 idea"
        assert ideas[0].id == "ID-001", "ID should be ID-001"
        
        # Test user story parsing
        sample_us = """
#### US-001: Test Story
**Como** test user
**Quiero** test action
**Para** test benefit

**Criterios de Aceptación:**
- [ ] Test criterion 1
- [ ] Test criterion 2

**Estimación**: 5 Story Points
**Epic**: Test Epic
**Estado**: To Do
"""
        user_stories = MarkdownParser.parse_user_stories(sample_us)
        assert len(user_stories) == 1, "Should parse 1 user story"
        assert user_stories[0].id == "US-001", "ID should be US-001"
        assert len(user_stories[0].acceptance_criteria) == 2, "Should have 2 criteria"
        
        print("✅ Parser tests passed")
        return True
    except Exception as e:
        print(f"❌ Parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_models():
    """Test data models."""
    print("\nTesting models...")
    try:
        from scripts.idea_processor.models import Idea, UserStory, AcceptanceCriteria
        
        # Test Idea model
        idea = Idea(
            id="ID-001",
            title="Test Idea",
            context="Test context",
            problem="Test problem",
            value="Test value",
            date_created="2025-11-14",
            status="💭 Por refinar",
            priority="Alta 🔴"
        )
        assert idea.id == "ID-001"
        
        # Test UserStory model
        us = UserStory(
            id="US-001",
            title="Test Story",
            as_a="test user",
            i_want="test action",
            so_that="test benefit",
            acceptance_criteria=[
                AcceptanceCriteria(text="Test criterion")
            ]
        )
        assert us.id == "US-001"
        assert len(us.acceptance_criteria) == 1
        
        # Test to_markdown
        markdown = us.to_markdown()
        assert "US-001" in markdown
        assert "test user" in markdown
        
        print("✅ Model tests passed")
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_structure():
    """Test that expected files exist."""
    print("\nTesting file structure...")
    try:
        repo_root = Path(__file__).parent.parent.parent
        
        required_files = [
            repo_root / "IDEAS.md",
            repo_root / "BACKLOG.md",
            repo_root / "scripts" / "idea_processor" / "cli.py",
            repo_root / "scripts" / "idea_processor" / "config.py",
            repo_root / "scripts" / "idea_processor" / "models.py",
            repo_root / "scripts" / "idea_processor" / "parser.py",
            repo_root / "scripts" / "idea_processor" / "similarity.py",
            repo_root / "scripts" / "idea_processor" / "generator.py",
            repo_root / "scripts" / "idea_processor" / "processor.py",
            repo_root / "scripts" / "idea_processor" / "README.md",
            repo_root / "scripts" / "idea_processor" / "requirements.txt",
        ]
        
        for file_path in required_files:
            assert file_path.exists(), f"Missing file: {file_path}"
        
        print(f"✅ All {len(required_files)} required files exist")
        return True
    except Exception as e:
        print(f"❌ File structure test failed: {e}")
        return False


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Idea Processor Validation Suite")
    print("=" * 60)
    
    results = []
    
    # Test file structure first (doesn't require dependencies)
    results.append(("File Structure", test_file_structure()))
    
    # Test imports (requires dependencies)
    imports_ok = test_imports()
    results.append(("Imports", imports_ok))
    
    if imports_ok:
        # Only run these if imports worked
        results.append(("Models", test_models()))
        results.append(("Parser", test_parser()))
    else:
        print("\nSkipping remaining tests due to missing dependencies.")
    
    # Summary
    print("\n" + "=" * 60)
    print("Validation Results")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20s}: {status}")
    
    all_passed = all(passed for _, passed in results)
    
    print("=" * 60)
    if all_passed:
        print("\n✅ All validation tests passed!")
        return 0
    else:
        print("\n❌ Some validation tests failed.")
        print("\nIf dependencies are missing, install them with:")
        print("  pip install -r scripts/idea_processor/requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
