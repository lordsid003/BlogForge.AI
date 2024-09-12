import os
import re
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.messages.ai import AIMessage
from textblob import TextBlob

load_dotenv()

def format_bullets(content):
    content = re.sub(r'(\d+\. )', r'\n\1', content)  
    content = re.sub(r'(\n- )', r'\n\n- ', content)  
    return content.strip()

class Model:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.8,
            model="llama3-70b-8192",
            api_key=st.secrets["LLAMA_API_KEY"]
        )


    def clean_content(self, content):
        content = re.sub(r'[^\w\s.,!?\'"-\u0900-\u097F\u0600-\u06FF\u4E00-\u9FFF\uAC00-\uD7AF\u3040-\u309F\u30A0-\u30FF]', '', content)
        return content
    

    def generate_outline(self, topic):
        prompt = PromptTemplate(
            input_variables=["topic"],
            template="""
                Create a detailed outline in for a blog post on topic: {topic}. 
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
    

    def generate_content(self, topic, style="formal", words=500, language="English"):
        prompt = PromptTemplate(
            input_variables=["style", "topic", "words", "language"],
            template=
            """
                Write a {style} blog post in {language} language about {topic} in exactly {words} words. 
                The content should include exactly 3-4 key points, with each point in a new line, 
                clearly presented using bullet points or numbered lists.
                Ensure the text is engaging, informative, statistical, and factual.
                Stay within the word count limit.
            """,
            validate_template=True
        )
        chain = prompt | self.llm
        data = {"topic": topic, "style": style, "words": words, "language": language}
        response = chain.invoke(data)

        if isinstance(response, AIMessage):
            content = response.content 
        else:
            raise ValueError(f"Unexpected response type: {type(response)}")
       
        content = content.strip()  
        content = re.sub(r'\n+', '\n', content)
        content = format_bullets(content)

        return content
    
    
    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity 
        return sentiment
    
    
    def expand_section(self, section, words=500, language="English"):
        prompt = PromptTemplate(
            input_variables=["section", "words", "language"],
            template=
            """
                Expand on the following blog section in {language} language with examples in {words} words: {section}.
                The content should include exactly 3-4 key points, with each point in a new line, 
                clearly presented using bullet points or numbered lists.
                Ensure the text is engaging, informative, statistical, and factual.
                Stay within the word count limit.
            """
        )
        chain = prompt | self.llm
        data = {"section": section, "words": words, "language": language}
        response = chain.invoke(data)
        if isinstance(response, AIMessage):
            content = response.content 
        else:
            raise ValueError(f"Unexpected response type: {type(response)}")

        content = content.strip()  
        content = re.sub(r'\n+', '\n', content)
        content = format_bullets(content)

        return content