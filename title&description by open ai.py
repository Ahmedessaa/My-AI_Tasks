import openai
openai.api_key = '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'

def generate_website_title(prompt):
    model = "gpt-3.5-turbo-instruct"

    response = openai.Completion.create(
        engine=model,
        prompt=f"Create a catchy title for a website about {prompt}.",
        max_tokens=15, 
        temperature=0.5,
        n=1,
        stop=None
    )

    return response.choices[0].text.strip()

def generate_description(title):
    model = "gpt-3.5-turbo-instruct"

    description_prompt = f"Generate a brief description for a website with the title: '{title}'."
    
    response = openai.Completion.create(
        engine=model,
        prompt=description_prompt,
        max_tokens=150,  
        temperature=0.5,
        n=1,
        stop=None
    )

    return response.choices[0].text.strip()

user_input = input("Enter a topic for your website: ")

website_title = generate_website_title(user_input)
print("Generated Title:", website_title)

description = generate_description(website_title)
print("Generated Description:", description)
