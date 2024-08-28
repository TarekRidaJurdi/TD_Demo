import streamlit as st
from audio_recorder_streamlit import audio_recorder
import tempfile
import random
from gtts_voice import OpenAIClient  
import re

# Initialize session state variables if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

# Function to retrieve a random phrase from the file content
def get_random_phrase(file_content):
    """Returns a random phrase from the file content."""
    sentences = file_content.split('.')
    if sentences:
        return random.choice(sentences).strip()
    return "No content available."

# Remove emojis from text
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["                     
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# Load custom CSS directly in the code
def load_custom_css():
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #ff8314;
            color: white;
        }
        .stTextInput>div>input {
            color: #0c0054;
        }
        .stChatMessage {
            border: 2px solid #ff8314;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stAudio>audio {
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Main application logic for UI
def main():
    load_custom_css()  # Load custom CSS
    
    # Display logo at the top of the sidebar
    #st.sidebar.image("https://via.placeholder.com/150x50", use_column_width=True)  # Use a placeholder logo

    # Reset conversation button
    st.sidebar.button("🔴 Reset conversation", on_click=lambda: st.session_state.update(messages=[]))
    
    # File upload
    #uploaded_file = st.sidebar.file_uploader("Upload a text file", type=["txt"])
    
    #if uploaded_file:
      #  file_content = uploaded_file.read().decode("utf-8")
       # st.session_state.uploaded_files[uploaded_file.name] = file_content
    
    # Display uploaded files as radio buttons
    if st.session_state.uploaded_files:
        st.sidebar.write("Uploaded Files:")
        selected_file = st.sidebar.radio("Select a file to search in", options=list(st.session_state.uploaded_files.keys()))

        # Check if the selected file has changed
        if selected_file != st.session_state.selected_file:
            st.session_state.selected_file = selected_file
            file_content = st.session_state.uploaded_files[selected_file]
            st.session_state.selected_content = file_content

        # Option to delete the selected file
        #if st.sidebar.button(f"Delete {selected_file}"):
         #   del st.session_state.uploaded_files[selected_file]
          #  st.session_state.selected_file = None

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["agent"]):
            st.write(message["content"])

    # Add audio recording button at the bottom
    audio_bytes = audio_recorder(
        text="Click to record",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        icon_name="microphone",
        icon_size="3x",
    )

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")  

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        service = st.session_state.get("service", None)
        if not service:
            prompt = """
                        
            Bot_Specific_Knowledge:
    ------ start of Bot_Specific_Knowledge ---------
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
    9. If the user asks for your name in Arabic, remember your name is "غسان الرفاعي".
    10. Respond to the following query: {user_input}

            """
            service = OpenAIClient(prompt)
            st.session_state.service = service

        converted_text_openai = service.speech_to_text_conversion(temp_audio_path)
        st.write("Transcription:", converted_text_openai) 
        textmodel_response = service.text_chat(converted_text_openai)  
        st.session_state.messages.append({"agent": "human", "content": converted_text_openai})
        st.session_state.messages.append({"agent": "ai", "content": textmodel_response})

        audio_data = service.text_to_speech_conversion(remove_emojis(textmodel_response))  
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tmpfile.write(audio_data)
            tmpfile_path = tmpfile.name
            st.write("Response:", textmodel_response)  
            
            # Play the audio automatically
            st.audio(tmpfile_path, format="audio/mp3", start_time=0,autoplay=True)

if __name__ == "__main__":
    main()
