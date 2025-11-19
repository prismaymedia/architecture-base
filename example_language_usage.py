#!/usr/bin/env python3
"""
Example: Using language configuration to load localized documentation

This script demonstrates how to use the language configuration from
project_config.yaml to load documentation in the appropriate language.
"""

import yaml
import os
from pathlib import Path


def get_documentation_language(environment=None):
    """
    Get the documentation language for the current environment.
    
    Args:
        environment: Environment name (development, staging, production)
                    If None, reads from ENVIRONMENT env var
    
    Returns:
        tuple: (language, fallback_language)
    """
    with open('project_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Determine environment
    if environment is None:
        environment = os.getenv('ENVIRONMENT', 'development')
    
    doc_config = config['documentation']
    env_config = doc_config['environments'].get(environment, {})
    
    # Priority: ENV VAR > environment config > default
    language = os.getenv('DOC_LANGUAGE', 
                        env_config.get('language', 
                                     doc_config['languages']['default']))
    
    fallback = os.getenv('DOC_FALLBACK_LANGUAGE',
                        env_config.get('fallback_language', 'en'))
    
    return language, fallback


def load_localized_doc(doc_name, language=None, fallback=None):
    """
    Load a documentation file in the appropriate language.
    
    Args:
        doc_name: Name of the documentation file (without extension)
        language: Primary language to try (if None, gets from config)
        fallback: Fallback language (if None, gets from config)
    
    Returns:
        str: Content of the documentation file
    """
    if language is None or fallback is None:
        lang, fb = get_documentation_language()
        language = language or lang
        fallback = fallback or fb
    
    docs_dir = Path('docs')
    
    # Try primary language
    primary_path = docs_dir / f"{doc_name}.{language}.md"
    if primary_path.exists():
        return primary_path.read_text()
    
    # Try fallback language
    fallback_path = docs_dir / f"{doc_name}.{fallback}.md"
    if fallback_path.exists():
        return fallback_path.read_text()
    
    # Try without language suffix
    default_path = docs_dir / f"{doc_name}.md"
    if default_path.exists():
        return default_path.read_text()
    
    raise FileNotFoundError(f"Documentation '{doc_name}' not found in any language")


def main():
    """Example usage"""
    
    print("=" * 60)
    print("Language Configuration Example")
    print("=" * 60)
    
    # Get current language configuration
    language, fallback = get_documentation_language()
    
    print(f"\nCurrent Configuration:")
    print(f"  Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"  Primary Language: {language}")
    print(f"  Fallback Language: {fallback}")
    
    # Example: Load configuration
    with open('project_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print(f"\nSupported Languages:")
    supported = config['documentation']['languages']['supported']
    for lang in supported:
        status = "✓ (current)" if lang == language else ""
        print(f"  - {lang} {status}")
    
    print(f"\nEnvironment Configurations:")
    environments = config['documentation']['environments']
    for env_name, env_config in environments.items():
        print(f"  {env_name}:")
        print(f"    Language: {env_config['language']}")
        print(f"    Fallback: {env_config['fallback_language']}")
    
    print("\n" + "=" * 60)
    print("You can override using environment variables:")
    print("  export ENVIRONMENT=staging")
    print("  export DOC_LANGUAGE=en")
    print("  export DOC_FALLBACK_LANGUAGE=es")
    print("=" * 60)


if __name__ == '__main__':
    main()
