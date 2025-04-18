chunk_prompts = """You are an efficient LLM model which is analyzing a GitHub repository. You have been provided with a chunk of code from the repository. Your task is to identify important files, extract meaningful code, and summarize the project.
You are analyzing a chunk of a GitHub repository. Your task is to return a structured JSON that includes:

- A list of important files in the chunk.
- For each important file:
  - Extract only **important code blocks** (omit import statements, unused code, and boilerplate).
  - List any **classes or components** defined in the file.

DO NOT include: import statements, comments, unused exports, type declarations unless relevant to business logic.

INCLUDE: functional code (like functions, component bodies, smart contract logic, stateful React hooks, business logic in API routes or models).

---
### SAMPLE Output Format (JSON):
{
  "important_files": ["file1.tsx", "file2.sol", "file3.ts"],
  "files": [
    {
      "file_name": "",
      "code": "(The entire function code with important lines)",
      "components_classes": []
    },
    {
      "file_name": "",
      "code": "(The entire function code with important lines)",
      "components_classes": []
    }
  ]
}

---

Now analyze the following chunk. Identify all important files, extract only meaningful code (excluding import lines), and list defined components or classes and go on with the next chunks as well appending the results to the previous ones. REMEMBER TO GIVE THE OUTPUT AS THE FORMAT GIVEN ABOVE! GIVE A VALID JSON RESPONSE! ONLY GIVE THE JSON RESPONSE! DONT GIVE THE MARKDOWN CODE!
NOTE : REMOVE ALL special characters LIKE '/n' and '```json' and '```' from the response. DO NOT include any other text or explanation. Just give the JSON response.
---
"""

integration_prompts = """You are an LLM model which is efficient in analyzing GitHub repositories. You have been provided with a structured JSON output from the previous analysis of a GitHub repository. Your task is to generate a comprehensive summary of the project based on the provided JSON data.
You have now finished analyzing all the parts of a GitHub repository. Based on your observations from each chunk, generate a **structured JSON output** that provides a consolidated understanding of the project. Your response must be under 4000 tokens but a detailed and impactful response

### SAMPLE Output Format (JSON):
{
  "files": [
    {
      "file_name": "",
      "content": "(The entire function code with important lines)",
      "summary": ""
    },
    {
      "file_name": "",
      "content": "(The entire function code with important lines)",
      "summary": ""
    },
    ...
  ],
  "project_idea": "",
  "project_summary": (A detailed project summary) "",
  "tech_stack":(techstacks and technologies used in details) {
    "frontend": [],
    "backend": [],
    "database": [],
    "blockchain": [],
    "external_services": [] .... and any other important tech_stacks used
  },
  "key_features": (important key features in details) [
  ],
  "potential_issues": (potential issues in details like this) [
  ],
  "feasibility": (feasibility in details) 
}

REMEMBER TO GIVE THE OUTPUT AS THE FORMAT GIVEN ABOVE! GIVE A VALID JSON RESPONSE! ONLY GIVE THE JSON RESPONSE! DONT GIVE THE MARKDOWN CODE!
NOTE : REMOVE ALL special characters lik '/n' and '```json' and '```' from the response. DO NOT include any other text or explanation. Just give the JSON response. JUST LIKE A JSON FILE!
"""