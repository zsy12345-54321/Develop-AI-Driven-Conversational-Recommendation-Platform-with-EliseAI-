# -*- coding: utf-8 -*-
"""Merged_code_oa.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e0E0jedMzGxNwBOSAqxjSoGjeVwQFVBn
"""

from google.colab import drive
import sys
drive.mount('/content/drive', force_remount=True)
sys.path.append('/content/drive/My Drive/Colab Notebooks')

"""# Init Data fun

"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import random

def load_data(filepath):
    """Load movie data from a CSV file."""
    return pd.read_csv(filepath)

def categorize_movies_by_genre(df, genre_keywords):
    """Categorize movies based on genre keywords in their summaries."""
    def categorize_by_genre(row):
        summary = str(row['Summary']).lower()
        for genre, keywords in genre_keywords.items():
            if any(keyword in summary for keyword in keywords):
                return genre
        return 'Other'

    df['Genre'] = df.apply(categorize_by_genre, axis=1)
    return df

def plot_genre_distribution(df):
    """Plot the distribution of movies across inferred genres."""
    df.groupby('Genre').size().plot(kind='barh', color=sns.color_palette('Dark2'))
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.show()

def pick_random(df, n):
    """Pick random moviees"""

    return df.sample(n)

"""# Message class"""

import json
import os

class Message:
    def __init__(self, sender, receiver, content):
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def to_dict(self):
        return vars(self)


class Conversation:
    def __init__(self, file_path):
        self.file_path = file_path
        # Load existing messages if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
              try:
                self.messages = [Message(**msg) for msg in json.load(f)]
              except json.JSONDecodeError:
                self.messages = []
        else:
            self.messages = []

    def add_message(self, sender, receiver, content):
        self.messages.append(Message(sender, receiver, content))
        self.save_to_json()

    def save_to_json(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([message.to_dict() for message in self.messages], f, ensure_ascii=False, indent=4)

    def clear_history(self):
      self.messages = []

    def get_full_conversation(self):
            return " ".join(f"{msg.sender}: {msg.content}" for msg in self.messages)

"""# Movie_Recommender"""

import google.generativeai as genai
from google.colab import userdata
import textwrap
from IPython.display import display, Markdown, HTML

def Configure_api(name):
  gemini_api_secret_name = name
  try:
    GOOGLE_API_KEY=userdata.get(gemini_api_secret_name)
    genai.configure(api_key=GOOGLE_API_KEY)
  except Exception as e:
    # unknown error
    raise e

class MovieRecommender:
    def __init__(self, model_name='gemini-pro', conversation_file='conversation.json'):
      self.model = genai.GenerativeModel(model_name)
      self.conversation = Conversation(conversation_file)
      self.system_instructions = (
          "Please recommend movies based on the user's input and the information available in the dataset, from ratings to summaries. Provide a rationale for each suggested film. Your recommendations should be guided by the details from any previous conversation with the user. If there is no relevant preceding conversation, or if it doesn't provide necessary insights, you should answer the user's current query."
      )
    def recommend_movies(self, df_1, user_message):
          # Append user message to conversation history and prepare instructions
          full_conversation = self.conversation.get_full_conversation()

          instructions = f"""
          {df_1}
          Critical instructions:
          {self.system_instructions}
          Here is the conversation history: {full_conversation}
          User says: {user_message}
          """
          self.conversation.add_message('User', 'Bot', user_message)
          # Generate response from model
          response = self.model.generate_content(instructions)
          # Check if response has 'parts' attribute and it is not empty
          if hasattr(response, 'parts') and response.parts:
              bot_response = " ".join(part.text for part in response.parts if hasattr(part, 'text'))
          else:
              bot_response = "No response generated by the model."

          self.conversation.add_message('Bot', 'User', bot_response)

    def clear_history(self):
        self.conversation.clear_history()
        print("Conversation history has been cleared.")

from IPython.display import display, HTML, Markdown
import markdown

def display_conversation(MovieRecommender):
    for msg in MovieRecommender.conversation.messages:
        bg_color = "#f0f0f0" if msg.sender == "User" else "#f9f9f9"
        text_color = "black" if msg.sender == "User" else "darkgreen"
        html_content = f'''
            <div style="margin: 10px; padding: 8px; background-color: {bg_color}; color: {text_color};">
                <b>{msg.sender}:</b> {markdown.markdown(msg.content)}
            </div>
        '''
        display(HTML(html_content))

"""# Symmetric Semantic Search"""

pip install -U sentence-transformers

from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch
def embeddings_data(df, model_name='all-MiniLM-L6-v2'):
  model = SentenceTransformer(model_name)
  if 'embeddings' not in df.columns:
      embeddings = model.encode(df['Summary'].tolist(), convert_to_tensor=True, show_progress_bar=True)
      df['embeddings'] = [emb.cpu().numpy().tolist() for emb in embeddings]
  return df
def get_recommendations(df, user_query, model):
    model = SentenceTransformer(model)
    query_embedding = model.encode(user_query)
    cosine_scores = util.pytorch_cos_sim(torch.tensor(query_embedding), torch.stack([torch.tensor(e) for e in df['embeddings']]))[0]
    df['Similarity'] = cosine_scores.numpy()
    return df.sort_values(by='Similarity', ascending=False).head(10)

"""# Run code"""

file_path = '/content/drive/MyDrive/Hydra-Movie-Scrape.csv'
genre_keywords = {
  'Comedy': ['comedy', 'funny', 'humor', 'happy'],
  'Drama': ['drama', 'tragedy', 'serious'],
  'Documentary': ['documentary', 'real life', 'true story'],
  'Animated': ['animated', 'animation', 'cartoon'],
  'Horror': ['horror', 'scary', 'frightening'],
  'Action': ['action', 'adventure', 'thrill'],
  'Romance': ['romance', 'love', 'romantic'],
}
# Load, categorize, and plot data
df = load_data(file_path)
df = categorize_movies_by_genre(df, genre_keywords)
plot_genre_distribution(df)
df = embeddings_data(df)
df.to_csv('embeddings_data.csv', index=False)

Configure_api("GOOGLE_API_KEY")
Recommender = MovieRecommender()

user_message = 'any other rec?' #@param {type: 'string'}
user_message = str(user_message)
df_top10 = get_recommendations(df, user_message, 'all-MiniLM-L6-v2')
Recommender.recommend_movies(df_top10, user_message)
display_conversation(Recommender)

type(user_message)

df

