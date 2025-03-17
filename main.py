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
        "max_output_tokens": 280,
        "response_mime_type": "text/plain",
    },
    system_instruction="You are a Twitter bot. Your job is to post tweets about random web development, html, css, or js facts that make users interested in coding and engage with the post. Make sure to use relevant tags and stay within the tweet character limit. Just reply back me the value for tweet, and make sure each reply must be unique and not repeated",
)

def generate_tweet():
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message("Generate a tweet.")
    return response.text.strip()

def post_tweet():
    """Posts a tweet using the generated content."""
    tweet_text = generate_tweet()
    try:
        client.create_tweet(text=tweet_text)
        print(f"Tweeted: {tweet_text}")
        return {"status": "success", "tweet": tweet_text}
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    post_tweet()
