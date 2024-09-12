import streamlit as st
from blog_generator import Model
from outliner import Outliner

def format_sentiment(sentiment_score):
    if sentiment_score > 0:
        return f"<span style='color: green; font-weight: bold;'>Positive</span> ✔️ (Score: {sentiment_score:.2f})"
    elif sentiment_score < 0:
        return f"<span style='color: red; font-weight: bold;'>Negative</span> ❌ (Score: {sentiment_score:.2f})"
    else:
        return f"<span style='color: blue; font-weight: bold;'>Neutral</span> 🔵 (Score: {sentiment_score:.2f})"

def main():
    st.title("BlogForge.AI")
    st.write("Personalized AI-Blog Assistant 📝")

    st.subheader("# Features")
    st.write(
        """
        **Welcome to the AI-Powered Blog Assistant!**  
        This application offers the following features:
        - **Content Generation:** Create engaging and informative blog posts on any topic.
        - **Outline Generation:** Get a detailed outline with main points and subpoints for your blog post.
        - **Mind Map Creation:** Visualize your blog outline as a mind map for better organization and planning.
        - **Section Expansion:** Expand specific sections of your blog post with detailed explanations and examples.
        - **Customizable Style:** Choose from different writing styles including Formal, Casual, Technical, and Research.
        """
    )
    with st.sidebar:
        st.write("Select the writing style:")
        style = st.selectbox("Choose the style:", ["formal", "casual", "technical", "research"])

        st.write("Blog words count:")
        words = st.selectbox("Choose the word count:", [500, 800, 1000])

    st.write("## Enter Your Blog Topic")
    topic = st.text_input("Enter your blog topic:")

    if topic:
        generator = Model()
        outliner = Outliner()

        with st.spinner("Generating content..."):
            content = generator.generate_content(topic, style, words)
        
        sentiment = generator.analyze_sentiment(content)
        formatted_sentiment = format_sentiment(sentiment)
        st.markdown(f"### Sentiment Analysis of Generated Content\n{formatted_sentiment}", unsafe_allow_html=True)

        with st.expander("Blog Content"):
            st.subheader("Generated Content:")
            st.write(content)

        with st.spinner("Generating outline..."):
            outline = generator.generate_outline(topic) 

        with st.expander("Outline Details"):
            st.write("### Generated Outline")
            for item in outline:
                st.write(item)
        
        with st.expander("Mind Map"):
            st.write("### Generated Mind Map")
            fig = outliner.create_mind_map(outline)
            st.plotly_chart(fig)

        selected_node = st.selectbox("Select a section to expand:", outline[1])
        if st.button("Expand Section"):
            with st.spinner("Expanding section..."):
                expanded_content = generator.expand_section(selected_node)
            with st.expander("Expanded content"):
                st.subheader("Expanded Content:")
                st.write(expanded_content)

if __name__ == "__main__":
    main()