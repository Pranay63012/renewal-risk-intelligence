from groq import Groq

client = Groq(api_key="GROQ_API_KEY")  # Replace with your actual API key or set as environment variable

def run_test():
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Say hello in one simple sentence"}
        ]
    )

    print("\nAI Test Output:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    run_test()