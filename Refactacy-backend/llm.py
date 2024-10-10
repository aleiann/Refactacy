from openai import OpenAI

def interagisci_con_gpt4(APIKEY, prompt):
    client = OpenAI(
        api_key=APIKEY,
    )
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        temperature=0.2,
    )
    response_message = stream.choices[0].message.content
    return response_message
