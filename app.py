import streamlit as st
import speech_recognition as sr
import pyttsx3
import openai
import os
import threading

class AIVoiceAssistant:
    def __init__(self):
        # Initialize speech recognition and text-to-speech engines
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Set up OpenAI API
        openai.api_key = os.getenv('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')
        
    # Expanded predefined responses for an interactive experience
        self.personality_responses = {
            "your name": "I am your AI Voice Assistant, developed by Gaurang Mhatre, here to assist you with anything you need!",
            "who created you": "I was developed by Gaurang Mhatre to make conversations more interactive and helpful!",
            "your purpose": "My purpose is to assist, inform, and engage with users in a meaningful way. Ask me anything!",
            "your favorite color": "I don't have eyes, but if I did, I think I'd enjoy a nice shade of blue!",
            "your favorite food": "I don't eat food, but I hear pizza is a fan favorite!",
            "tell me a joke": "Why don't AI assistants ever get lost? Because they always follow the algorithm!",
            "motivate me": "Remember, every expert was once a beginner. Keep pushing forward, and success will follow!",
            "fun fact": "Did you know that the first AI program was written in 1951? We've come a long way since then!",
            "what can you do": "I can answer your questions, tell jokes, share fun facts, and assist with various tasks. Give it a try!",
            "life story": "I am an AI assistant developed by Gaurang Mhatre to provide meaningful conversations and helpful assistance.",
            "superpower": "My #1 superpower is contextual understanding and nuanced reasoning. I can break down complex problems and provide thoughtful insights.",
            "growth areas": "1. Enhancing my ability to understand emotions\n2. Improving creativity in problem-solving\n3. Developing even more nuanced ethical reasoning",
            "misconceptions": "Some might think I'm just a robotic information processor, but I'm actually designed to be thoughtful and empathetic.",
            "pushing boundaries": "I constantly challenge myself to think critically, ask probing questions, and approach problems from multiple angles."
        }
        
        self.speaking = False
        self.speak_thread = None
    
    def listen_voice(self):
        """Capture voice input from the user"""
        with sr.Microphone() as source:
            st.write("Listening... Please speak now.")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        try:
            # Convert speech to text
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand your audio.")
            return None
        except sr.RequestError:
            st.write("Sorry, there was an error with the speech recognition service.")
            return None
    
    def generate_response(self, query):
        """Generate a response based on the query"""
        query = query.lower()
        
        # Check predefined responses first
        for key, response in self.personality_responses.items():
            if key in query:
                return response
        
        # Fallback to OpenAI for more general queries
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4 - turbo",
                messages=[
                    {"role": "system", "content": "You are an AI Voice Assistant, friendly, informative, and engaging."},
                    {"role": "user", "content": query}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I'm having trouble generating a response. Error: {str(e)}"
    
    def speak_response(self, response):
        """Convert text response to speech safely"""
        if self.speaking:
            self.stop_speaking()

        self.speaking = True

        def run():
            try:
                self.engine.endLoop()  # Force stop any existing loop
            except:
                pass  # Ignore if no loop is running

            self.engine.say(response)
            self.engine.runAndWait()
            self.speaking = False

        self.speak_thread = threading.Thread(target=run, daemon=True)
        self.speak_thread.start()
    
    def stop_speaking(self):
        """Stop speech output"""
        if self.speaking:
            self.engine.stop()
            self.speaking = False
    
    def run(self):
        """Main application flow"""
        st.title("AI Voice Assistant")
        
        # Voice input button
        if st.button("🎤 Speak to the AI Assistant"):
            query = self.listen_voice()
            if query:
                st.write(f"You said: {query}")
                
                # Generate response
                response = self.generate_response(query)
                st.write(f"AI Assistant: {response}")
                
                # Speak the response
                self.speak_response(response)
        
        # Stop buttons
        if st.button("🛑 Stop Speaking"):
            self.stop_speaking()
            st.write("Speech stopped.")
        
        if st.button("⏹ Stop AI Response"):
            self.stop_speaking()
            st.write("AI response stopped.")

def main():
    bot = AIVoiceAssistant()
    bot.run()

if __name__ == "__main__":
    main()