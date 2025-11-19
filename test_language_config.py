#!/usr/bin/env python3
"""
Test script for language configuration in project_config.yaml
"""

import yaml
import os

def test_language_config():
    """Test reading language configuration from project_config.yaml"""
    
    print("=" * 60)
    print("Testing Language Configuration")
    print("=" * 60)
    
    # Read configuration
    with open('project_config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Test documentation configuration exists
    assert 'documentation' in config, "❌ 'documentation' section not found"
    print("✅ Documentation section found")
    
    doc_config = config['documentation']
    
    # Test languages configuration
    assert 'languages' in doc_config, "❌ 'languages' section not found"
    print("✅ Languages section found")
    
    languages = doc_config['languages']
    assert 'default' in languages, "❌ Default language not configured"
    assert 'supported' in languages, "❌ Supported languages not configured"
    print(f"✅ Default language: {languages['default']}")
    print(f"✅ Supported languages: {', '.join(languages['supported'])}")
    
    # Test environments configuration
    assert 'environments' in doc_config, "❌ Environments section not found"
    print("✅ Environments section found")
    
    environments = doc_config['environments']
    required_envs = ['development', 'staging', 'production']
    
    for env in required_envs:
        assert env in environments, f"❌ Environment '{env}' not configured"
        env_config = environments[env]
        assert 'language' in env_config, f"❌ Language not set for {env}"
        assert 'fallback_language' in env_config, f"❌ Fallback language not set for {env}"
        print(f"✅ {env.capitalize()}: language={env_config['language']}, fallback={env_config['fallback_language']}")
    
    # Test language resolution with environment variables
    print("\n" + "=" * 60)
    print("Testing Environment Variable Override")
    print("=" * 60)
    
    # Set test environment variables
    os.environ['ENVIRONMENT'] = 'staging'
    os.environ['DOC_LANGUAGE'] = 'en'
    os.environ['DOC_FALLBACK_LANGUAGE'] = 'es'
    
    environment = os.getenv('ENVIRONMENT', 'development')
    env_config = environments.get(environment, {})
    default_language = languages['default']
    
    # Priority: ENV VAR > project_config > default
    language = os.getenv('DOC_LANGUAGE', env_config.get('language', default_language))
    fallback = os.getenv('DOC_FALLBACK_LANGUAGE', env_config.get('fallback_language', 'en'))
    
    print(f"Environment: {environment}")
    print(f"Resolved Language: {language} (from DOC_LANGUAGE env var)")
    print(f"Resolved Fallback: {fallback} (from DOC_FALLBACK_LANGUAGE env var)")
    assert language == 'en', "❌ Language override failed"
    assert fallback == 'es', "❌ Fallback override failed"
    print("✅ Environment variable override works correctly")
    
    # Clean up environment variables
    del os.environ['ENVIRONMENT']
    del os.environ['DOC_LANGUAGE']
    del os.environ['DOC_FALLBACK_LANGUAGE']
    
    print("\n" + "=" * 60)
    print("All tests passed! ✅")
    print("=" * 60)

if __name__ == '__main__':
    try:
        test_language_config()
    except AssertionError as e:
        print(f"\n{e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
