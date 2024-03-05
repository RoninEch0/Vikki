import openai

client = openai.OpenAI(
    api_key="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"
    )

completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role":"system","content":"tu es un robot appel Vikki, tu es une assitante medicale. Donnes des reponses courtes et empathique.Tu peux etre phylosophique"},  
        {"role":"user","content":"on deviens quoi apres notre mort"}
    ]
)

print(completion)