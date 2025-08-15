#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    print("OpenAI client created successfully")
    print("Available attributes:", [attr for attr in dir(client) if not attr.startswith('_')])
    
    # Test basic chat completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Hello, can you search the web?"}
        ],
        max_tokens=50
    )
    
    print("\nBasic chat test:")
    print(response.choices[0].message.content)
    
    # Check if agents attribute exists
    if hasattr(client, 'agents'):
        print("\n✅ Agents API is available!")
    else:
        print("\n❌ Agents API is not available in this version")
        
    # Check for beta features
    if hasattr(client, 'beta'):
        print("✅ Beta features available:", dir(client.beta))
    else:
        print("❌ No beta features found")
        
except Exception as e:
    print(f"Error: {e}")


