from flask import Flask, render_template, request
from langchain.prompts import PromptTemplate
from openai import Image
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from openai import OpenAI

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder='static')

template = """
You describe an image for a text2image AI.
It is important to describe the contents with keywords that can be recognised by the AI.
Use adjectives to describe details. 
Limit your answer to at most 75 words.
Do not use the following words: [knob].

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
        model="dall-e-3",
        prompt=description,
        size="1024x1024",
        quality="standard",
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
