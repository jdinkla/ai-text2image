from flask import Flask, render_template, request
from langchain import PromptTemplate, OpenAI, LLMChain
from openai import Image

app = Flask(__name__, static_folder='static')

template = """
You describe an image for a text2image AI.
It is important to describe the contents with keywords that can be recognised by the AI.
Use adjectives to describe details. 
Limit your answer to at most 75 words.
Do not use the following words: [knob].

Question: {question}
"""

prompt = PromptTemplate(
    input_variables=["question"],
    template=template
)

chain = LLMChain(llm=OpenAI(temperature=0.5), prompt=prompt)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def get_image():
    question = request.form['text']
    print("question: " + question)
    description = chain.predict(question=question)
    print(description)
    response = Image.create(
        prompt=description,
        n=1,
        size="1024x1024"
    )
    print(response)
    image_url = response['data'][0]['url']
    return render_template('index.html', text=question, description=description, image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)
