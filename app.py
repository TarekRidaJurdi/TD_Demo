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
    st.title("💬 TD Virtual Assistant Chatbot")
    
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
    ### Empowering Business Growth: Ghassan's Method and Life Journey

**Passionate Business Advocate**  
Ghassan Alrifai is dedicated to helping businesses grow and innovate. With 15 years of diverse experience, he supports aspiring entrepreneurs, believing in strategies that benefit everyone. His mantra, "together we all win," reflects his commitment to collaborative and mutually beneficial partnerships.

**Early Education and Business Beginnings**  
Ghassan’s journey began with a Diploma in English from Ramsgate Kent’s Regency School of English in 1997. Initially pursuing law at Beirut Arabia University, he transitioned to IT, eventually earning a diploma in Networking and Systems Engineering in 2003. At 19, while studying in Syria, he opened his first internet café in Homs, launching his entrepreneurial career. He also managed a coffee shop and participated in his family’s automobile business.

**Family: The Cornerstone of His Life**  
Family holds a special place in Ghassan’s life, shaping his values and priorities. Since his marriage in 2007, he has been a devoted husband and father of two children. Family moments, especially with his mother, who joined his household after his father's passing in 2012, are deeply cherished. His Syrian heritage, rich in business and politics, profoundly influences his perspectives and endeavors.

**Professional Career: A Diverse Path Across Industries**  
Ghassan's career began in 2004 in Qatar, where he gained experience across various industries. He managed servers for prestigious clients at HP, excelled in automotive sales at Al-Mannai, and served as a Business Development Officer at IBQ. His achievements include boosting business revenue by $400 million in 2008 and securing dealership deals with renowned German companies.

**A New Phase of Business Cooperation**  
Ghassan excelled in the automotive industry, particularly at Automobile Al-Mannai, focusing on General Motors (GMC). Despite his success, he moved on to leverage his expertise in securing substantial deals for a new engineering firm, navigating challenges along the way.

**Establishing Successful Businesses**  
Driven by entrepreneurial spirit, Ghassan embarked on establishing and managing businesses. Notably, he founded VGC, a testament to his determination and success in business.

**Revolutionizing Investment with Treasure Deal Invest INC**  
One of Ghassan's major ventures is Treasure Deal Invest INC, an investment company poised to revolutionize the industry through innovative technology and a unique business model. Founded in the USA and expanding to the UAE and Qatar, the company aims to empower startups with a $120 million capital dedicated to supporting innovation and growth. Future plans include establishing a legal presence in the UK.

**Commitment to Excellence**  
Ghassan’s professional journey is marked by a commitment to excellence, innovation, and a customer-centric approach. His success across various industries showcases his expertise and forward-thinking mindset.

**Current and Upcoming Ventures**  
As a Venture Partner, Ghassan plays a crucial role in identifying and evaluating new investment opportunities, offering strategic support, and managing relationships with a vast network of startups and investors. His upcoming ventures include Treasure Deal Group, a business conglomerate specializing in cutting-edge solutions across 18 industries, and Veteran General Contracting (VGC), where he serves as CEO, providing top-tier facilities management services in Qatar.

**Ghasan Al-Refai's Successful Ventures**  
Ghassan has been instrumental in transforming numerous startups into market giants. Through his guidance and expertise, these companies have overcome challenges, achieved significant growth, and expanded into new markets.

**Coming Soon: Treasure Deal Invest**  
Ghassan's upcoming project, Treasure Deal Invest, is focused on nurturing 36 startups over the next three years, with a strategic vision extending to the GCC and Europe. This dynamic investment firm aims to streamline the investment journey, providing easier access to capital and empowering the next generation of pioneering businesses.

---

*Note: The content could be further enriched with suitable images or photographs of Ghassan Alrifai and his family, and milestones could be highlighted using blocks or cards for a visually appealing presentation.*
    
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
                        
