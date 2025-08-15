#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print("Testing Assistants API for web search...")
    
    # Check what's available in beta.assistants
    print("Beta assistants attributes:", [attr for attr in dir(client.beta.assistants) if not attr.startswith('_')])
    
    # Try to create an assistant with web search
    try:
        assistant = client.beta.assistants.create(
            name="Web Search Test",
            instructions="You are a helpful assistant that can search the web.",
            model="gpt-4o-mini",
            tools=[{"type": "web_search"}]
        )
        print("✅ Assistant created with web search!")
        print(f"Assistant ID: {assistant.id}")
        
        # Clean up
        client.beta.assistants.delete(assistant.id)
        print("Assistant cleaned up")
        
    except Exception as e:
        print(f"❌ Error creating assistant with web search: {e}")
        
        # Try without web search
        try:
            assistant = client.beta.assistants.create(
                name="Basic Test",
                instructions="You are a helpful assistant.",
                model="gpt-4o-mini"
            )
            print("✅ Basic assistant created successfully")
            print(f"Assistant ID: {assistant.id}")
            
            # Clean up
            client.beta.assistants.delete(assistant.id)
            print("Basic assistant cleaned up")
            
        except Exception as e2:
            print(f"❌ Error creating basic assistant: {e2}")
    
    # Check available models
    print("\nChecking available models...")
    models = client.models.list()
    search_models = [model.id for model in models.data if 'search' in model.id.lower()]
    if search_models:
        print("✅ Found search-enabled models:", search_models)
    else:
        print("❌ No search-enabled models found")
        
except Exception as e:
    print(f"Error: {e}")


