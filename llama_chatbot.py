# -*- coding: utf-8 -*-
"""llama_chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P9gWiGGWRXP4nBUJN3Yn45ZHk-14SxUh

# Install Dependencies
"""

# Commented out IPython magic to ensure Python compatibility.
# Install dependencies and initialize
# %pip install -qU \
    replicate \
    langchain \
    sentence_transformers \
    pdf2image \
    pdfminer \
    pdfminer.six \
    unstructured \
    pillow-heif \
    unstructured-inference \
    pikepdf \
    pypdf \
    faiss-gpu --quiet

"""# Presentation Layer Code

Defines different functions and widgets that can be used to generate and display various diagrams and architectures
"""

# Presentation layer code

import base64
from IPython.display import Image, display
import matplotlib.pyplot as plt

def mm(graph):
  graphbytes = graph.encode("ascii")
  base64_bytes = base64.b64encode(graphbytes)
  base64_string = base64_bytes.decode("ascii")
  display(Image(url="https://mermaid.ink/img/" + base64_string))

def genai_app_arch():
  mm("""
  flowchart TD
    A[Users] --> B(Applications e.g. mobile, web)
    B --> |Hosted API|C(Platforms e.g. Custom, HuggingFace, Replicate)
    B -- optional --> E(Frameworks e.g. LangChain)
    C-->|User Input|D[Llama 2]
    D-->|Model Output|C
    E --> C
    classDef default fill:#CCE6FF,stroke:#84BCF5,textColor:#1C2B33,fontFamily:trebuchet ms;
  """)

def rag_arch():
  mm("""
  flowchart TD
    A[User Prompts] --> B(Frameworks e.g. LangChain)
    B <--> |Database, Docs, XLS|C[fa:fa-database External Data]
    B -->|API|D[Llama 2]
    classDef default fill:#CCE6FF,stroke:#84BCF5,textColor:#1C2B33,fontFamily:trebuchet ms;
  """)

def llama2_family():
  mm("""
  graph LR;
      llama-2 --> llama-2-7b
      llama-2 --> llama-2-13b
      llama-2 --> llama-2-70b
      llama-2-7b --> llama-2-7b-chat
      llama-2-13b --> llama-2-13b-chat
      llama-2-70b --> llama-2-70b-chat
      classDef default fill:#CCE6FF,stroke:#84BCF5,textColor:#1C2B33,fontFamily:trebuchet ms;
  """)

def apps_and_llms():
  mm("""
  graph LR;
    users --> apps
    apps --> frameworks
    frameworks --> platforms
    platforms --> Llama 2
    classDef default fill:#CCE6FF,stroke:#84BCF5,textColor:#1C2B33,fontFamily:trebuchet ms;
  """)

import ipywidgets as widgets
from IPython.display import display, Markdown

API_KEY = widgets.Password(
    value='',
    placeholder='',
    description='API_KEY:',
    disabled=False
)

def md(t):
  display(Markdown(t))

def bot_arch():
  mm("""
  graph LR;
  user --> prompt
  prompt --> i_safety
  i_safety --> context
  context --> Llama_2
  Llama_2 --> output
  output --> o_safety
  i_safety --> memory
  o_safety --> memory
  memory --> context
  o_safety --> user
  classDef default fill:#CCE6FF,stroke:#84BCF5,textColor:#1C2B33,fontFamily:trebuchet ms;
  """)

def fine_tuned_arch():
  mm("""
  graph LR;
      Custom_Dataset --> Pre-trained_Llama
      Pre-trained_Llama --> Fine-tuned_Llama
      Fine-tuned_Llama --> RLHF
      RLHF --> |Loss:Cross-Entropy|Fine-tuned_Llama
      classDef default fill:#CCE6FF,stroke:#84BCF5,textColor:#1C2B33,fontFamily:trebuchet ms;
  """)

def load_data_faiss_arch():
  mm("""
  graph LR;
      documents --> textsplitter
      textsplitter --> embeddings
      embeddings --> vectorstore
      classDef default fill:#CCE6FF,stroke:#84BCF5,textColor:#1C2B33,fontFamily:trebuchet ms;
  """)

def mem_context():
  mm("""
      graph LR
      context(text)
      user_prompt --> context
      instruction --> context
      examples --> context
      memory --> context
      context --> tokenizer
      tokenizer --> embeddings
      embeddings --> LLM
      classDef default fill:#CCE6FF,stroke:#84BCF5,textColor:#1C2B33,fontFamily:trebuchet ms;
  """)

"""# Chat Completion

This basic chat completion generates accurate and informative information based on the provided user input.

Utilizes Replicate's hosted version of Llama 13-b for chat completion tasks.

For reference: [Link to Replicate API key](https://replicate.com/account/api-tokens)
"""

import os
import replicate
from getpass import getpass


# Utilize Replicate's llama-2-13b
llama2_13b = "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d"

REPLICATE_API_TOKEN = getpass()
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Text completion with input prompt and system prompt
# to promote respectful, safe, and factual responses that propose
# a holistic approach to knowledge acquisition (ie not just trusting one source blindly)
def chatCompletion(prompt):
  output = replicate.run(
      llama2_13b,
      input={"prompt": prompt,
             "temperature": 1.0,
             "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. Always let the user know they can ask you more questions or follow up about the previous response given.",
             "max_new_tokens":1000}
  )
  return "".join(output)

"""# Chat Completion - Sample Financial Questions

**What is a Ticker Symbol?**
"""

output = chatCompletion(prompt="Can you explain to me what a ticker symbol is?")

# Display output using markdown
md(output)

"""**What is a Security vs Stock vs ETF vs Mutual Fund?**"""

output = chatCompletion(prompt="What is the difference between a security vs a stock vs an ETF vs a mutual fund?")
md(output)

"""**How do you know when to buy a security?**"""

output = chatCompletion(prompt="How can you tell when to buy a stock? I'm new to investing.")
md(output)

"""# Chat Completion with Conversation Memory

LLMs are stateless by default, meaning they don't necessarily have access to previous conversation content or context.

Understandably, this can lead to a frustrating user experience when engaging with this financial chatbot. Thus, the following code example demonstrates how to have a multi-turn conversation that captures the context of a user conversation with the chatbot.
"""

user_prompt_chat = """
User: How can you tell when to buy a stock? I'm new to investing.
Assistant: Hello! I'd be happy to help you with your question. However, before we dive into specifics, I want to point out that it's important to consult with a financial advisor or professional before making any investment decisions. They can provide personalized advice based on your individual circumstances and risk tolerance.
That being said, here are some general tips that may be helpful in determining when to buy a stock:
Research the company: Before investing in a particular stock, research the company to understand its financials, business model, and growth prospects. Look for companies with strong fundamentals, such as a history of profitability, a competitive advantage, and a solid balance sheet.
Evaluate market trends: Keep an eye on overall market trends and economic conditions. A strong economy with low inflation and stable interest rates can support stock prices. On the other hand, a recession or market downturn can lead to lower stock values.
Consider valuation: Compare the stock's price to its earnings, revenue, and other fundamental metrics. Avoid overpaying for stocks by looking for value opportunities.
Diversify your portfolio: Spread your investments across different asset classes, sectors, and geographic regions to minimize risk. This can help you ride out market volatility and capture growth opportunities in various areas.
Have a long-term perspective: Investing in stocks should be a long-term game plan. Aim to hold onto your investments for at least five years or more, as this allows for the natural ebbs and flows of the market.
Monitor news and events: Stay informed about news and events that may impact the stocks you own. Company announcements, industry developments, and macroeconomic factors can all influence stock performance.
Be cautious of hype: Be wary of overhyped stocks or industries that promise unusually high returns. These situations can be risky and may not align with your investment goals.
Consult multiple sources: Gather information from reliable sources, such as financial news outlets, research firms, and analyst reports. Avoid relying solely on one source or opinion.
Be prepared to adapt: Your investment strategy may need to evolve over time based on changes in the market or your personal circumstances. Remain flexible and open to adjusting your approach as needed.
Seek professional guidance: If you're new to investing or feel unsure about any aspect of the process, consider consulting a financial advisor or registered investment advisor. They can provide tailored advice and help you create a customized investment plan.
Remember, there is no foolproof way to predict when to buy a specific stock. The best approach is to educate yourself on sound investing principles, remain patient, and be prepared to adapt to changing market conditions.
User: Can you tell me more about what you said about seeking professional advice? What are some things I should look for in a financial or investment advisor? What would you say makes a good investment plan?
"""
output = chatCompletion(prompt=user_prompt_chat)
md(output)