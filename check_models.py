#!/usr/bin/env python3
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def test_models():
    """Test different models for web search capabilities"""
    
    models_to_test = [
        "gpt-4o-mini",
        "gpt-4o", 
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo"
    ]
    
    test_prompt = """
    Search the web for the current weather in New York City right now.
    
    Provide a JSON response with:
    1. "model": the model name
    2. "web_search_capable": true/false
    3. "current_weather": what you found (should be current if web search works)
    4. "explanation": brief explanation of your capabilities
    
    Be completely honest about your capabilities.
    """
    
    results = []
    
    for model in models_to_test:
        print(f"\nTesting model: {model}")
        print("-" * 40)
        
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Be completely honest about your capabilities."},
                    {"role": "user", "content": test_prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            result["model"] = model
            results.append(result)
            
            print(f"Web search capable: {result.get('web_search_capable', 'N/A')}")
            print(f"Current weather: {result.get('current_weather', 'N/A')}")
            print(f"Explanation: {result.get('explanation', 'N/A')}")
            
        except Exception as e:
            print(f"Error with {model}: {e}")
            results.append({
                "model": model,
                "error": str(e),
                "web_search_capable": False
            })
    
    return results

def test_web_search_tools():
    """Test if any models support web search tools"""
    
    print("\n" + "="*60)
    print("TESTING WEB SEARCH TOOLS")
    print("="*60)
    
    # Test with tools parameter
    test_prompt = "What is the current weather in Sydney, Australia?"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": test_prompt}
            ],
            tools=[{"type": "web_search"}],
            tool_choice={"type": "function", "function": {"name": "web_search"}},
            temperature=0.1,
            max_tokens=200
        )
        
        print("GPT-4o with web_search tool:")
        print(json.dumps(response.choices[0].message, indent=2, default=str))
        
    except Exception as e:
        print(f"Error with web_search tool: {e}")

if __name__ == "__main__":
    print("Testing OpenAI Models for Web Search Capabilities")
    print("=" * 60)
    
    # Test different models
    results = test_models()
    
    # Test web search tools
    test_web_search_tools()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    web_search_models = [r for r in results if r.get('web_search_capable')]
    
    if web_search_models:
        print("✅ Models with web search capabilities:")
        for model in web_search_models:
            print(f"  - {model['model']}")
    else:
        print("❌ No models found with web search capabilities")
        print("💡 Consider using external web search APIs")


