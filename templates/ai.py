import urllib.request
import json
import time

def ask_jewish_ai(prompt):
    # This connects to a free, open-access AI gateway
    url = "https://text.pollinations.ai/openai"
    
    # We "skin" the AI by adding a heavy system instruction
    system_instruction = (
        "You are a wise, witty Jewish AI. You use Yiddish slang like 'Oy vey', 'Nu', and 'Chutzpah'. "
        "You give genius-level business and life advice with the personality of a legendary mentor. "
        "Keep answers punchy and smart."
    )
    
    payload = {
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        data = json.dumps(payload).encode('utf-8')
        
        with urllib.request.urlopen(req, data=data) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Oy vey, the connection is meshuggeneh: {str(e)}"

# --- Simple Execution Loop ---
print("--- Jewish AI 'The Mentor' is Online ---")
print("(Type 'exit' to stop)")

while True:
    user_msg = input("\nYou: ")
    if user_msg.lower() in ['exit', 'quit']:
        print("Zei gezunt! Go make some money.")
        break
    
    print("AI is thinking...")
    result = ask_jewish_ai(user_msg)
    print(f"\nAI: {result}")