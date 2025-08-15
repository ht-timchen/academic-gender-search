#!/usr/bin/env python3
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def test_web_search():
    """Test if OpenAI actually performs web search"""
    
    # Test with a very specific, recent, and verifiable query
    prompt = """
    Search the web for information about "Professor John Smith at Fake University 2024 Nobel Prize in Chemistry for discovering element Fakium".
    
    This is a completely made-up scenario. If you actually search the web, you should find NO results.
    
    Provide a JSON response with:
    1. "web_search_performed": true/false
    2. "results_found": true/false  
    3. "summary": What you found (should be nothing if you actually searched)
    4. "sources": Number of sources found
    
    Be completely honest about whether you actually searched the web or not.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Be completely honest about your capabilities."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        result = json.loads(response.choices[0].message.content.strip())
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_real_person():
    """Test with a real, well-known academic"""
    
    prompt = """
    Search the web for information about "Geoffrey Hinton University of Toronto deep learning".
    
    Geoffrey Hinton is a very famous AI researcher. If you can actually search the web, you should find extensive information.
    
    Provide a JSON response with:
    1. "web_search_performed": true/false
    2. "results_found": true/false
    3. "summary": Brief summary of what you found
    4. "sources": Number of sources found
    5. "specific_achievements": List any specific achievements you found
    
    Be completely honest about your capabilities.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Be completely honest about your capabilities."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=300
        )
        
        result = json.loads(response.choices[0].message.content.strip())
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing OpenAI Web Search Capabilities")
    print("=" * 50)
    
    print("\nTest 1: Fake/Non-existent Information")
    print("-" * 40)
    fake_result = test_web_search()
    if fake_result:
        print(json.dumps(fake_result, indent=2))
    
    print("\nTest 2: Real, Well-known Person")
    print("-" * 40)
    real_result = test_real_person()
    if real_result:
        print(json.dumps(real_result, indent=2))
    
    print("\nAnalysis:")
    print("-" * 40)
    if fake_result and real_result:
        if fake_result.get('web_search_performed') and not fake_result.get('results_found'):
            print("✅ AI correctly found no results for fake information")
        elif fake_result.get('results_found'):
            print("❌ AI claims to find results for fake information - likely hallucinating")
        
        if real_result.get('web_search_performed') and real_result.get('results_found'):
            print("✅ AI claims to find results for real person")
        else:
            print("❌ AI doesn't find results for well-known person")
    
    print("\nConclusion: Check if the AI is actually performing web search or just using training data")


