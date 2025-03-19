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
    system_instruction="You are a twitter bot who generates random tweet about intresting facts on web development, html, css, js each time random, unique, intersting and should not repeat if already said. Remember the tweet size limit and don't use markdown just reply back me the tweet text value",
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
