

Nebula Backend is a FastAPI-based backend application designed to analyze GitHub repositories and provide structured summaries. It leverages AI models like Gemini to process repository content and generate meaningful insights. The application includes endpoints for repository ingestion and summarization, making it a powerful tool for developers to understand codebases quickly.

---

## Features

- **GitHub Repository Analysis**: Analyze GitHub repositories to extract meaningful insights.
- **AI-Powered Summarization**: Uses AI models like Gemini and Groq for content analysis and summarization.
- **FastAPI Framework**: Built with FastAPI for high performance and scalability.
- **CORS Support**: Configured to allow cross-origin requests from specific frontend applications.
- **JSON Responses**: Provides structured JSON responses for easy integration with frontend applications.

---

## Project Structure

```
.gitignore
main.py
requirements.txt
controllers/
    summarise.py
routes/
    summarise_route.py
utils/
    prompts.py
```

### File Descriptions

- **main.py**: The entry point of the application. Configures the FastAPI app, sets up CORS middleware, and includes routes.
- **requirements.txt**: Lists all the dependencies required for the project.
- **summarise.py**: Contains the core logic for analyzing GitHub repositories using AI models.
- **summarise_route.py**: Defines the API route for summarizing GitHub repositories.
- **prompts.py**: Contains prompt templates used for AI model interactions.
- **.gitignore**: Specifies files and directories to be ignored by Git.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/nebula-backend.git
   cd nebula-backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add the following environment variables:

   ```
   GOOGLE_API_KEY=your_google_api_key
   ```

---

## Usage

1. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

2. Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

3. Use the following endpoints:

   - **`GET /`**: Returns a welcome message.
   - **`GET /greet/{name}`**: Greets the user with the provided name.
   - **`GET /api/gitingest`**: Ingests a GitHub repository and returns its summary.
   - **`POST /api/summarise`**: Accepts a GitHub repository URL and returns a detailed analysis.

---

## API Example

### Request: `POST /api/summarise`

```json
{
  "github_repo_url": "https://github.com/example/repo"
}
```

### Response:

```json
{
  "repoMarkdown": "Detailed Markdown Summary",
  "repoSummary": "Detailed JSON Summary",
  "success": true
}
```

---

## Development

### Adding New Features

1. Add new routes in the routes directory.
2. Implement the corresponding logic in the controllers directory.
3. Update the main.py file to include the new route.

### Running Tests

To run tests, use the following command:

```bash
pytest
```

---

## Dependencies

The project uses the following Python libraries:

- `gitingest`: For GitHub repository ingestion.
- `google-genai`: For interacting with Google's AI models.
- `groq`: For generating summaries using Groq.
- `dotenv`: For managing environment variables.
- `fastapi`: For building the backend API.
- `uvicorn`: For running the FastAPI server.
- `pydantic`: For data validation and parsing.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- **FastAPI**: For providing an excellent framework for building APIs.
- **Google GenAI**: For enabling AI-powered content analysis.

---
