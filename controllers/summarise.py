import os
import sys
import json
import asyncio
from gitingest import ingest_async
from google import genai
from groq import Groq
from dotenv import load_dotenv
from utils.prompts import chunk_prompts
from utils.prompts import integration_prompts

print(chunk_prompts)

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
TOKEN_LIMIT = 4000
CHUNK_SIZE = 8000  

def split_into_chunks(content, chunk_size):
    """Split content into chunks of specified token size."""
    tokens = content.split()
    chunks = []
    
    for i in range(0, len(tokens), chunk_size):
        chunk = " ".join(tokens[i:i + chunk_size])
        print(f"Chunk {(i/chunk_size) + 1}: {chunk[:50]}...")
        print("-----------------------------------------------------------------------------------") 
        chunks.append(chunk)
    
    return chunks

def truncate_content(content, limit):
    """Reduces content size to fit within the token limit."""
    tokens = content.split()
    if len(tokens) > limit:
        return " ".join(tokens[:limit])
    return content

def analyze_with_gemini(repo_summary, repo_tree, repo_content):
    """Use Gemini to identify relevant files and extract important code within token limit."""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        content_chunks = split_into_chunks(repo_content, CHUNK_SIZE)
        
        base_prompt = (
            "You are a senior software developer analyzing a GitHub repository. "
            "Provide a thorough, structured analysis that would help someone understand the codebase quickly.\n\n"
            f"Repository Summary: {repo_summary}\n\n"
            f"Repository Files Structure: {repo_tree}\n\n"
            "Your analysis should:\n"
            "1. Identify the main purpose of this repository\n"
            "2. Highlight key components, frameworks, and technologies used\n"
            "3. Outline the architecture and how components interact\n"
            "4. Identify entry points and core functionality\n"
            "5. Note any interesting patterns or potential issues\n"
            "Be precise and technical in your assessment.\n\n"
        )
        
        responses = []

        for i, chunk in enumerate(content_chunks):
            chunk_prompt = (
                f"{base_prompt}"
                f"Files Content (Part {i+1}/{len(content_chunks)}):\n{chunk}\n\n"
                f"{chunk_prompts}"
            )
            
            chunk_response = client.models.generate_content(
                model="gemini-2.0-flash", contents=chunk_prompt
            )
            
            responses.append(chunk_response.text)

        integration_prompt = (
            f"{integration_prompts}"
            f"{' '.join(responses)}"
        )
        
        final_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=integration_prompt
        )

        print("GEMINI FINAL RESPONSE: ", final_response)
        
        return final_response.text
    except Exception as e:
        print(f"Error analyzing with Gemini: {e}", file=sys.stderr)
        return None

# def generate_with_groq(gemini_output):
#     """Use Groq to generate a comprehensive summary based on Gemini's analysis."""
#     try:
#         client = Groq(api_key=GROQ_API_KEY)
        
#         truncated_output = truncate_content(gemini_output, TOKEN_LIMIT)
        
#         prompt = (
#             f"{integration_prompts}"
#             f"{truncated_output}"
#         )
        
#         chat_completion = client.chat.completions.create(
#             messages=[{"role": "user", "content": prompt}],
#             model="llama-3.3-70b-versatile",
#             response_format={"type": "json_object"}
#         )
        
#         return chat_completion.choices[0].message.content
#     except Exception as e:
#         print(f"Error generating response with Groq: {e}", file=sys.stderr)
#         return None
    

async def run_pipeline(github_url):
    try:
        summary, tree, content = await ingest_async(github_url)
        print("----------TREE----------")
        print(tree)
        print("--------------------------")
        if not summary or not tree or not content:
            raise ValueError("Failed to fetch repository details.")
        
        gemini_response = analyze_with_gemini(summary, tree, content)
        if not gemini_response:
            raise ValueError("Failed to analyze repository with Gemini.")
        
        # groq_summary = generate_with_groq(gemini_response)
        # if not groq_summary:
        #     raise ValueError("Failed to generate summary with Groq.")
        
        result = {
            "repoMarkdown": gemini_response,
            "repoSummary": gemini_response, ##groq_summary,
            "success": True
        }
        
        return result
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }
    

async def main(github_repo_url:str = None):
    result = {}
    if github_repo_url == None or github_repo_url == "":
        result = {
            "error": "No GitHub URL provided.",
            "success": False
        }
    else:
        result = await run_pipeline(github_repo_url)
    
    print(json.dumps(result))
    return result

if __name__ == "__main__":
    asyncio.run(main())