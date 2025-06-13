# LinkedIn Comment Generator

This project provides an automated system to generate thoughtful, professional comments for LinkedIn posts using AI models (OpenAI or HuggingFace). It includes a FastAPI backend, LinkedIn post caption extraction via Selenium, and multiple comment generation strategies.

## Features

- **Extract LinkedIn Post Captions:** Uses Selenium (with stealth options) to fetch post content.
- **AI-Powered Comment Generation:** Supports both OpenAI (e.g., GPT-4o) and HuggingFace (e.g., Mixtral-8x7B) models.
- **REST API:** FastAPI endpoint for easy integration.
- **Customizable Prompts:** Generates comments with different tones and perspectives.
- **Command-Line & Script Usage:** Includes scripts for direct use and testing.

## Requirements

- Python 3.8+
- Google Chrome (for Selenium)
- The following Python packages (see `requirements.txt`):
  - fastapi
  - uvicorn
  - pydantic
  - requests
  - openai
  - torch
  - transformers
  - selenium
  - selenium-stealth
  - undetected-chromedriver

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up ChromeDriver:**  
   Ensure ChromeDriver is installed and matches your Chrome version.

3. **API Keys:**
   - For OpenAI: Get your API key from [OpenAI](https://platform.openai.com/).
   - For HuggingFace: Get your token from [HuggingFace](https://huggingface.co/settings/tokens).

## Usage

### 1. Run the FastAPI Server

```bash
uvicorn main:app --reload
```

- **Endpoint:** `POST /linkedin-comment`
- **Request Body:**
  ```json
  {
    "post_url": "LINKEDIN_POST_URL_HERE",
    "provider": "openai" or "hf",
    "token": "YOUR_API_TOKEN"
  }
  ```

### 2. Command-Line Script

Generate a comment directly:

```bash
python generate_comment.py --post_url "LINKEDIN_POST_URL" --provider openai --token YOUR_API_TOKEN
```

## File Overview

- `main.py` - FastAPI backend for comment generation.
- `generate_comment.py` - Functions for generating comments using OpenAI or HuggingFace.
- `get_post_caption.py` - Extracts post captions from LinkedIn using Selenium.

## Notes

- LinkedIn’s HTML structure may change; update selectors in `get_post_caption.py` as needed.
- For best results, use valid API tokens and ensure your environment supports Selenium.

## License

MIT License
