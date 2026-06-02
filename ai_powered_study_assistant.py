import os
from dotenv import load_dotenv
from google import genai
# from google.colab import userdata
from google.genai import types
import gradio as gr

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# client = genai.Client(api_key=userdata.get('GEMINI_API_KEY'))
client = genai.Client(api_key=api_key)


personalities = {
  "Friendly": "You are a friendly, enthusiastic, and highly encouraging Study Assistant. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding.",
  "Academic": "You are a strictly academic, highly detailed, and professional university Professor. Use precise, formal terminology, cite key concepts and structure your response. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding."
}

def study_assistant(user_prompt, personality):
  system_prompt = personalities[personality]
  response = client.models.generate_content(
      model="gemini-2.5-flash" ,
      config = types.GenerateContentConfig(
          system_instruction = system_prompt,
          temperature = 0.2,
          max_output_tokens = 1024
      ),
      contents = user_prompt

  )
  return response.text

demo = gr.Interface(
  fn=study_assistant,
  inputs=[
      gr.Textbox(lines=4, placeholder = "Ask any question", label = "Question"),
      gr.Dropdown(choices=list(personalities.keys()), value = "Friendly", label = "Personality")
  ],
  outputs=gr.Textbox(lines = 10, label = "Response"),
  title = "Study Assistant",
  description="Ask any question to your study assistant with your chosen personality"
)

demo.launch(debug = True)


question = "What are LLMs?"
personality = "Friendly"
print(study_assistant(question, personality))