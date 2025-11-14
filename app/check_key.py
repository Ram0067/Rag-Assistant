import os
from openai import OpenAI

def check_openai_key():
    """Verify that your OpenAI API key is valid and active."""
    print("🔍 Checking OpenAI API key validity...\n")

    api_key = os.getenv("OPENAI_API_KEY")
    

    if not api_key:
        print("❌ No API key found in environment variables.")
        print("➡️  Please set it with:")
        print("   setx OPENAI_API_KEY \"sk-your-key-here\"   (Windows)")
        print("   export OPENAI_API_KEY=\"sk-your-key-here\"  (Linux/macOS)")
        return

    try:
        client = OpenAI(api_key=api_key)
        response = client.models.list()
        models = client.models.list()
        print("✅ Models available for this API key:")
        for m in models.data:
            print("-", m.id)
        print("✅ Your OpenAI API key is valid!")
        print(f"📦 You have access to {len(response.data)} models.")
        print("Example model:", response.data[0].id)
    except Exception as e:
        print("❌ API Key validation failed.")
        print(f"Error: {e}")
        print("\n🧭 Tips:")
        print(" - Make sure your key starts with `sk-` or `sk-proj-`.")
        print(" - If it's a project key, also set `OPENAI_PROJECT_ID`.")
        print(" - Visit https://platform.openai.com/api-keys to create a new one.")

if __name__ == "__main__":
    check_openai_key()
