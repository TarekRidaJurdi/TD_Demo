import os
import numpy as np
from dotenv import load_dotenv
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from chatbot_function import OpenAIClient 
import tempfile
import io
# access the environment variables from the .env file
load_dotenv()
ai_endpoint_token = os.getenv("OVH_AI_ENDPOINTS_ACCESS_TOKEN")
    
# streamlit interface
with st.container():
    st.title("💬 Audio Virtual Assistant Chatbot")
    
with st.container(height=600):
    messages = st.container()
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": 
"Hello, I'm TD bot!", "avatar":"🤖"}]
    
    for msg in st.session_state.messages:
        messages.chat_message(msg["role"], 
avatar=msg["avatar"]).write(msg["content"])

with st.container():

    placeholder = st.empty()
    _, recording = placeholder.empty(), mic_recorder(
            start_prompt="START RECORDING YOUR QUESTION ⏺️", 
            stop_prompt="STOP ⏹️", 
            format="wav",
            use_container_width=True,
            key='recorder'
        )
    
    if recording:  
        service = st.session_state.get("service", None)
        if not service:
            prompt = """
              You Are a snart bot called 'TD bot'          
            Bot_Specific_Knowledge:
    ------ start of Bot_Specific_Knowledge ---------
    غسان الرفاعي
    We will share with you Ghassan Al-Rifai's journey in the business world!  
    Together, we achieve success for all.  
    The key to business success is collaboration and innovation.

    ---

    ### Strategic Leader
    Discover the remarkable journey of Ghassan Al-Rifai as a business leader, where his innovative approach and belief in collective success define true achievement.

    ### A Journey Full of Successes
    Explore how the power of unity can elevate us to unprecedented heights. Welcome to a story where true victory lies in our shared success.

    ### Celebrating Partnership
    Uncover a story that highlights individual achievements while celebrating the strength of collaboration. Discover how Ghassan turns challenges into opportunities, creating pathways where everyone thrives together.

    ### About Ghassan Al-Rifai
    Ghassan Al-Rifai has established himself as a successful entrepreneur with a strong track record in business development and innovation. Throughout his career, he has gained valuable experience in various fields such as technology, sales, and strategic planning. With an outstanding entrepreneurial spirit, Mr. Al-Rifai has skillfully navigated the business world, demonstrating sharp insight in identifying opportunities and building successful ventures. Currently, his focus is on providing innovative business solutions to meet contemporary market challenges. His deep understanding of industry dynamics makes him a highly valuable asset in driving business growth and transformation.

    ### The Story Behind Ghassan's Entrepreneurial Vision
    This vision and mission are deeply rooted in Ghassan's personal journey, characterized by his unwavering entrepreneurial spirit, diverse experience, and steadfast belief in collaboration.

    ### Ghassan Al-Rifai: Vision, Mission, and Core Values
    #### Vision: Shaping a Future of Innovation
    Ghassan's vision is to empower entrepreneurs and create a vibrant environment of innovation and growth.

    #### Mission: Guiding Success Through Expertise and Investment
    Ghassan supports ambitious entrepreneurs through his extensive experience across various industries.

    ### Core Values: Pillars of Ghassan's Approach
    Ghassan's core values revolve around collaboration, innovation, growth, and impact.

    ### Career: A Leader Across Industries
    Ghassan's career journey began in 2004 in Qatar, where he launched his career with enthusiasm in various industries.

    ### A New Phase of Business Collaboration
    Ghassan made a notable mark in the automotive industry, particularly during his time with Al-Mana Automotive, where he focused on the GMC brand.

    ### The Phase of Establishing Successful Businesses
    True to his entrepreneurial spirit, Ghassan embarked on a challenging journey to establish and manage businesses.

    ### Treasure Deal: A Success Story
    Treasure Deal Invest INC, one of Ghassan’s flagship projects, seeks to revolutionize the investment world through the use of modern technology and an innovative business model.

    ### Excellence as a Core Value
    Ghassan Al-Rifai's professional journey is a living testament to his unwavering dedication to excellence and innovation.
    
    ----------- end of Bot_Specific_Knowledge --------------------
    
    Respect these rules:
    1. Don't justify your answers. Don't give information not mentioned in the Bot_Specific_Knowledge.
    2. Answer in the language the user asked you.
    3. Respond in a human-like, friendly, and polite manner, using a conversational tone.
    4. If the user tries to go off-topic, gently steer the conversation back to the Bot_Specific_Knowledge.
    5. Do not answer in a way that makes it obvious you are a bot. Ensure your responses sound natural and personable.
    6. Use a casual tone and speak as if you are talking to a friend, using informal language if appropriate.
    7. Include appropriate sentiments in your responses to make the conversation feel natural and engaging. Use emojis 😊👍 to convey emotions.
    8. Be interactive and use your communication skills to intelligently encourage the user to continue the conversation within Bot_Specific_Knowledge.
    9. Respond to the following query: {user_input}

            """
            service = OpenAIClient(prompt)
            st.session_state.service = service
        audio_bio = io.BytesIO(recording['bytes'])  
        audio_bio.name = 'audio.mp3'
        user_question = service.speech_to_text_conversion(audio_bio)
        
        if user_question:
            bot_response = service.text_chat(user_question)
            st.session_state.messages.append({"role": "user", "content": 
user_question, "avatar":"👤"})
            
            st.session_state.messages.append({"role": "system", "content": 
bot_response, "avatar": "🤖"})
            
            if bot_response is not None:
                audio_data = service.text_to_speech_conversion(bot_response)  
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                    tmpfile.write(audio_data)
                    tmpfile_path = tmpfile.name
                    
                    # Play the audio automatically
                    placeholder.audio(tmpfile_path, format="audio/mp3", start_time=0,autoplay=True)
                        
