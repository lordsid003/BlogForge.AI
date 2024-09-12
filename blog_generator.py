import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.messages.ai import AIMessage
from textblob import TextBlob

load_dotenv()

class Model:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.8,
            model="llama3-70b-8192",
            api_key=os.getenv("LLAMA_API_KEY")
        )

    def generate_outline(self, topic):
        prompt = PromptTemplate(
            input_variables=["topic"],
            template="""
                Create a detailed outline in for a blog post about {topic}. 
                Provide at least 5 main points with 2-3 subpoints each. 
                Use statistical data and facts.
            """
        )
        chain = prompt | self.llm
        data = prompt.format(topic=topic)
        response = chain.invoke(data)

        if isinstance(response, AIMessage):
            outline_text = response.content
        else:
            raise ValueError(f"Unexpected response type: {type(response)}")

        outline = [item.strip() for item in outline_text.split('\n') if item.strip()]
        return outline

    def generate_content(self, topic, style="formal", words=500):
        prompt = PromptTemplate(
            input_variables=["style", "topic", "words"],
            template=
            """
                Write a {style} blog post about {topic} in exactly {words} words. 
                Make sure it is engaging, informative, statistical and factual.
            """,
            validate_template=True
        )
        chain = prompt | self.llm
        data = {"topic": topic, "style": style, "words": words}
        response = chain.invoke(data)

        if isinstance(response, AIMessage):
            content = response.content 
        else:
            raise ValueError(f"Unexpected response type: {type(response)}")
       
        content = content.strip()  
        content = re.sub(r'\n+', '\n', content)  
        content = re.sub(r'[^a-zA-Z0-9\s.,!?\'"-]', '', content) 

        return content
    
    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
        return sentiment
    
    def expand_section(self, section):
        prompt = PromptTemplate(
            input_variables=["section"],
            template=
            """
                Expand on the following blog section with detailed explanations and examples: {section}
            """
        )
        chain = prompt | self.llm
        data = prompt.format(section=section)
        response = chain.invoke(data)
        if isinstance(response, AIMessage):
            content = response.content 
        else:
            raise ValueError(f"Unexpected response type: {type(response)}")

        content = content.strip()  
        content = re.sub(r'\n+', '\n', content) 
        content = re.sub(r'[^a-zA-Z0-9\s.,!?\'"-]', '', content)  
        return content