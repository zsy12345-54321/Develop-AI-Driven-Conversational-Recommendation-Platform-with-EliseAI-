# Develop-AI-Driven-Conversational-Recommendation-Platform-with-EliseAI

This project utilizes Python, Large Language Models, and the Hugging Face library to develop a chat-based application that provides real-time movie recommendations. The system analyzes movie data, categorizes movies by genre, and uses conversational AI powered by the Gemini API for dynamic and personalized movie suggestions. It is designed to run in a Google Colab environment and leverages various Google functionalities.

## Features

- **Data Loading and Visualization**: Load movie data from a CSV file, categorize it by genre based on summaries, and visualize the distribution of these genres.
- **Conversational Recommendations**: Utilize the Gemini API through a model-based conversational framework to interact with users and generate personalized movie recommendations.
- **Semantic Search**: Implement semantic search using the Hugging Face’s `sentence-transformers` to find movies that closely match a user's queries.

## Requirements

To run this script, you will need:
- Access to Google Colab
- A Google Drive with the necessary CSV file stored in 'My Drive/Colab Notebooks'
- Python packages including `pandas`, `numpy`, `matplotlib`, `seaborn`, `random`, `json`, `os`, `google`, `IPython`, `markdown`, `sentence-transformers`, `torch`

## Setup Instructions

1. **Google Colab Setup**:
   - Mount your Google Drive and ensure the path to your 'Colab Notebooks' folder is appended to `sys.path`.
   - Place the CSV file with movie data, named `Hydra-Movie-Scrape.csv`, in the 'My Drive/Colab Notebooks' folder.

2. **Dependency Installation**:
   - Install the necessary Python packages using the following command:
     ```python
     !pip install -U sentence-transformers
     ```

3. **API Configuration**:
   - Set up the Gemini API key to enable generative AI functionalities. Substitute `'GOOGLE_API_KEY'` with your actual API secret key.

## Usage

- **Data Processing**:
  - Run the `load_data`, `categorize_movies_by_genre`, and `plot_genre_distribution` functions to load and process the data.

- **Recommendation System**:
  - Initialize the `MovieRecommender` class, which employs the Gemini API for conversational movie recommendations. Input user messages to receive tailored suggestions based on the conversation context.

- **Semantic Search**:
  - Leverage `embeddings_data` and `get_recommendations` functions to conduct semantic searches and identify the top-10 movie recommendations in response to user queries.

## Example

Here’s how to interact with the MovieRecommender system:

```python
# Configure API
Configure_api("YOUR_API_SECRET_NAME")

# Initialize Recommender
Recommender = MovieRecommender()

# User input
user_message = "suggest a comedy movie"
df_top10 = get_recommendations(df, user_message, 'all-MiniLM-L6-v2')

# Get recommendations
Recommender.recommend_movies(df_top10, user_message)

# Display conversation
display_conversation(Recommender)
```

![Example Output](https://github.com/zsy12345-54321/Develop-AI-Driven-Conversational-Recommendation-Platform-with-EliseAI-/blob/main/output_example.png)

*Figure: A sample interaction in the Movie Recommender chat app showing the system's response to a user asking for a comedy movie recommendation.*

