import streamlit as st
from outliner import Outliner
from blog_generator import Model

generator = Model()
mind_map = Outliner()

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
        """
    )

    with st.sidebar:
        st.write("Select the writing style:")
        style = st.selectbox("Choose the style:", ["formal", "casual", "technical", "research"], key='style')

        st.write("Blog words count:")
        words = st.selectbox("Choose the word count:", [500, 800, 1000], key='words')

    st.write("## Enter Your Blog Topic")
    topic = st.text_input("Enter your blog topic:", key='topic')

    st.header("Preferred Language: ")
    lang = st.radio(
        "Choose an option:",
        ["English", "Hindi", "French", "German"],
        horizontal=True,
        key='language'
    )

    generate_blog = st.button("Generate Blog", key='generate_blog')

    if generate_blog:
        if 'content' not in st.session_state or st.session_state.lang != lang:
            with st.spinner("Generating content and outline..."):
                content = generator.generate_content(topic, style, words, lang)
                st.session_state.content = content
                st.session_state.lang = lang
                
                outline = generator.generate_outline(topic)
                st.session_state.outline = outline

            sentiment = generator.analyze_sentiment(st.session_state.content)
            formatted_sentiment = format_sentiment(sentiment)
            st.markdown(f"### Sentiment Analysis of Generated Content\n{formatted_sentiment}", unsafe_allow_html=True)

    if 'content' in st.session_state:
        with st.expander("Blog Content", expanded=True):
            st.subheader("Generated Content:")
            st.write(st.session_state.content)

    if 'outline' in st.session_state:
        with st.expander("Outline Details", expanded=False):
            st.write("### Generated Outline")
            for item in st.session_state.outline:
                st.write(item)

        with st.expander("Mind Map", expanded=False):
            st.write("### Generated Mind Map")
            fig = mind_map.create_mind_map(st.session_state.outline)
            st.plotly_chart(fig)

        selected_node = st.selectbox("Select a section to expand:", st.session_state.outline)

        if 'expanded_content' not in st.session_state:
            st.session_state.expanded_content = {}

        expand_section = st.button("Expand Section", key='expand_section')

        if expand_section and selected_node:
            if selected_node not in st.session_state.expanded_content or st.session_state.lang != lang:
                with st.spinner("Expanding section..."):
                    expanded_content = generator.expand_section(selected_node, words, lang)
                    st.session_state.expanded_content[selected_node] = expanded_content

        if selected_node in st.session_state.expanded_content:
            with st.expander("Expanded Content", expanded=True):
                st.subheader(f"Expanded Content: {selected_node}")
                st.write(st.session_state.expanded_content[selected_node])

if __name__ == "__main__":
    main()