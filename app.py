from flask import Flask, render_template, request
from langchain.prompts import PromptTemplate
from openai import Image
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

config = {
    "model": "dall-e-3", 
    "quality": "standard"
}

# config = {
#     "model": "gpt-image-1",
#     "quality": "medium"
# }

app = Flask(__name__, static_folder='static')

template = """
You are an expert in generating image descriptions for text-to-image AI models.

You describe an image for a text2image AI. Limit your answer to at most 75 words.

Question: {question}
"""

prompt = PromptTemplate.from_template(template)
runnable = prompt | ChatOpenAI() | StrOutputParser()

client = OpenAI()

def generateDescription(question):
    logging.debug("question: " + question)
    return runnable.invoke({"question": question})

def generateImage(description):
    logging.debug("description: " + description)
    response = client.images.generate(
        model=config["model"],
        prompt=description,
        size="1024x1024",
        quality=config["quality"],
        n=1,
    )
    logging.debug(response)
    return response.data[0].url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_image():
    question = request.form['text']
    description = generateDescription(question)
    url = generateImage(description)
    return render_template('index.html', text=question, description=description, image_url=url)

if __name__ == '__main__':
    app.run(debug=True)
