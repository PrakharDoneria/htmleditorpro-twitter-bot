import os
import tweepy
import google.generativeai as genai

# Twitter API Authentication
client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

# Gemini API Configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
    system_instruction="You are a Twitter bot that generates unique, interesting coding tips or website tricks. Do not repeat any previous tweet. Keep the tweet within 280 characters. No markdown."
)

# In-memory tweet history (lasts only during runtime)
tweet_history = set()
chat_history = []

def generate_unique_tweet(max_retries=5):
    """Generates a tweet that hasn't been tweeted before in this session."""
    for _ in range(max_retries):
        chat_session = model.start_chat(history=chat_history)
        response = chat_session.send_message("Generate a tweet.")
        tweet = response.text.strip()

        # Add to history to continue the context
        chat_history.append({"role": "user", "parts": ["Generate a tweet."]})
        chat_history.append({"role": "model", "parts": [tweet]})

        if tweet not in tweet_history:
            tweet_history.add(tweet)
            return tweet
    raise ValueError("Failed to generate a unique tweet after several attempts.")

def post_tweet():
    try:
        tweet_text = generate_unique_tweet()
        client.create_tweet(text=tweet_text)
        print(f"Tweeted: {tweet_text}")
        return {"status": "success", "tweet": tweet_text}
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")
        return {"status": "error", "message": str(e)}
    except ValueError as e:
        print(str(e))
        return {"status": "error", "message": "Could not generate a unique tweet."}

if __name__ == "__main__":
    post_tweet()
