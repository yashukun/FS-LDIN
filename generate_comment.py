import argparse
from get_post_caption import get_linkedin_post_caption
import requests
from openai import OpenAI

# For OpenAI (free-tier, e.g., gpt-3.5-turbo)
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
# Replace with your key
OPENAI_HEADERS = {"Authorization": "Bearer YOUR_OPENAI_API_KEY"}


def generate_comment_openai(caption: str, token: str) -> str:
    try:
        client = OpenAI(
            api_key=token
        )

        # Prompt template
        prompt = (
            f"Caption: {caption}\n"
            "Generate a positive, professional comment for this post in 10–20 words:"
        )

        # Call GPT-4o-mini model
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API exception: {e}"


def generate_comment_hf(caption: str, token: str, model_name: str = "mistralai/Mixtral-8x7B-Instruct-v0.1", strip_comment: bool = True) -> str:
    """
    Generate a positive LinkedIn comment using a HuggingFace Inference API model (Mixtral-8x7B-Instruct-v0.1).
    If strip_comment is True, only return the comment part after 'Comment:'.
    """
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {token}"}
    prompt = f"You are a professional LinkedIn user. Write a thoughtful, positive, and relevant consize upto 15 to 20 words comment for this post:\n\n{caption}\n\nComment:"
    data = {"inputs": prompt, "parameters": {
        "max_new_tokens": 200, "temperature": 0.7}}
    try:
        response = requests.post(
            api_url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            if not strip_comment:
                return str(result)
            # Extract only the comment part after the last 'Comment:'
            comment_text = None
            if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                generated = result[0]['generated_text']
                if 'Comment:' in generated:
                    comment_text = generated.split('Comment:')[-1].strip()
                else:
                    comment_text = generated.strip()
                return comment_text
            elif isinstance(result, dict) and 'generated_text' in result:
                generated = result['generated_text']
                if 'Comment:' in generated:
                    comment_text = generated.split('Comment:')[-1].strip()
                else:
                    comment_text = generated.strip()
                return comment_text
            else:
                return str(result)
        else:
            return f"HuggingFace API error: {response.text}"
    except Exception as e:
        return f"HuggingFace API exception: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate LinkedIn comment from post caption using OpenAI or HuggingFace model.")
    parser.add_argument("--post_url", required=True, help="LinkedIn post URL")
    parser.add_argument("--provider", choices=["openai", "hf"], required=True,
                        help="Choose comment generator: openai or hf (HuggingFace)")
    parser.add_argument("--token", required=True,
                        help="API token for OpenAI or HuggingFace")
    parser.add_argument("--model_name", default="mistralai/Mistral-7B-Instruct-v0.1",
                        help="Model name for HuggingFace provider")
    args = parser.parse_args()

    caption = get_linkedin_post_caption(args.post_url)
    print(f"Extracted Caption: {caption}\n")

    if args.provider == "openai":
        comment = generate_comment_openai(caption, args.token)
    elif args.provider == "hf":
        comment = generate_comment_hf(
            caption, args.token, args.model_name)
    else:
        print("Invalid provider.")
        return
    print(f"Suggested Comment:\n{comment}")


if __name__ == "__main__":
    main()
