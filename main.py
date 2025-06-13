from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

app = FastAPI()


class LinkedInRequest(BaseModel):
    # Example LinkedIn post URL
    # Replace with actual LinkedIn post URL
    post_url: str = "LINKEDIN_POST_URL_HERE"
    provider: str = "openai or hf"  # 'openai' or 'hf'
    token: str = "YOUR_API_TOKEN_HERE"  # API token for the selected provider


class LinkedInPostResponse(BaseModel):
    suggested_comment: str


@app.post("/linkedin-comment", response_model=LinkedInPostResponse)
def get_comment(data: LinkedInRequest = Body(...)):
    post_url = data.post_url
    provider = data.provider
    token = data.token
    if not post_url:
        raise HTTPException(status_code=400, detail="Post URL is required.")
    if provider not in ["openai", "hf"]:
        raise HTTPException(
            status_code=400, detail="Provider must be 'openai' or 'hf'.")
    if not token:
        raise HTTPException(status_code=400, detail="API token is required.")

    from generate_comment import get_linkedin_post_caption, generate_comment_openai, generate_comment_hf
    caption = get_linkedin_post_caption(post_url)
    print("Extracted Caption:")
    print(caption)
    print("Generating comment...")

    if provider == "openai":
        comment = generate_comment_openai(caption, token)
    else:
        comment = generate_comment_hf(caption, token)
    return LinkedInPostResponse(suggested_comment=comment)
