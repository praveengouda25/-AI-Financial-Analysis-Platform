"""
Helper script to create .streamlit/secrets.toml with proper UTF-8 encoding
Run this instead of using PowerShell echo command
"""

import os
from pathlib import Path

# Create .streamlit directory if it doesn't exist
streamlit_dir = Path('.streamlit')
streamlit_dir.mkdir(exist_ok=True)

# Create secrets.toml with UTF-8 encoding
secrets_file = streamlit_dir / 'secrets.toml'

secrets_content = '''# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
# Replace "sk-your-key-here" with your actual OpenAI API key

OPENAI_API_KEY = "sk-your-key-here"

# Optional: Specify model (default is gpt-3.5-turbo)
# OPENAI_MODEL = "gpt-4"
'''

# Write with UTF-8 encoding (no BOM)
with open(secrets_file, 'w', encoding='utf-8') as f:
    f.write(secrets_content)

print("✅ Created .streamlit/secrets.toml successfully!")
print(f"📁 Location: {secrets_file.absolute()}")
print("\n⚠️  IMPORTANT: Edit this file and replace 'sk-your-key-here' with your actual OpenAI API key")
print("\n📝 To edit:")
print(f"   notepad {secrets_file}")
print("\n🔒 This file is already in .gitignore - your API key is safe!")
