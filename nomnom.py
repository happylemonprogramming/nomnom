from openai import OpenAI
import os

# Let's use voice activation for the user and transcribe their content
# DVM? or is that too much?
# Use Pablo's ecash to npub combo to have user login and permit users to tip the response/bot
# Set up API keys
client = OpenAI(
  api_key=os.environ.get("openaiapikey"),
)

# FUNCTIONS
def get_recipe_suggestion(ingredients):
    """
    Use OpenAI's GPT model to generate a recipe suggestion based on ingredients.
    """
    prompt = f"Create a recipe using these ingredients: {', '.join(ingredients)}. Provide the recipe name and instructions."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful chef assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    print(response)
    return response.choices[0].message.content

def generate_image(recipe_name):
    response = client.images.generate(
    model="dall-e-3",
    prompt=recipe_name,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    return image_url

# WEBPAGE
import streamlit as st
from micstream import *

st.set_page_config(
    page_title='NOM NOM!',
    page_icon=':cooking:'
)

st.title("NOM NOM! :cooking:")

ingredients_input = st.text_input("Enter ingredients (separated by commas):")
# col1, col2 = st.columns(2)
# start_button = col1.button(":studio_microphone:")
# stop_button = col2.button(":large_red_square:")
# if start_button:
#     transcriber.connect()

#     microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
#     transcriber.stream(microphone_stream)
# if stop_button:
#     transcriber.close()
#     ingredients_input = transcript.text
ingredients = [ingredient.strip() for ingredient in ingredients_input.strip().split(',')]

if ingredients_input:
    with st.spinner('Generating recipe...'):
        recipe = get_recipe_suggestion(ingredients)
        recipe_name = recipe.split('\n')[0]  # Assuming the first line is the recipe name
        try:
            image = generate_image(recipe_name)
        except Exception as e:
            print(f"An error occurred while generating the image: {str(e)}")

    st.image(image)
    st.info(recipe)