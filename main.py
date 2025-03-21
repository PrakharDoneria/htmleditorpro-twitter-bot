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
    system_instruction="You are a twitter bot who generates random tweet about interesting facts on web development tips & tricks each time unique, interesting and should not repeat if already said. Remember the tweet size limit and don't use markdown just reply back me the tweet text value",
)

def generate_tweet():
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message("Generate a tweet.")
    return response.text.strip()

def get_trending_topics():
    """Fetch trending topics from Twitter."""
    try:
        trending = client.get_place_trends(id=1)  # Global trends, change the WOEID for specific location
        trending_topics = []
        for trend in trending[0]["trends"]:
            trending_topics.append(trend["name"].lower())  # Convert to lowercase for easy matching
        return trending_topics
    except tweepy.TweepyException as e:
        print(f"Error fetching trending topics: {e}")
        return []

def filter_trending_topics(trending_topics):
    """Filter trending topics to find ones related to web development or coding."""
    relevant_keywords = ["web development", "coding", "programming", "javascript", "python", "frontend", "backend", "webdev"]
    filtered_trends = [topic for topic in trending_topics if any(keyword in topic for keyword in relevant_keywords)]
    return filtered_trends

def post_tweet():
    """Posts a tweet using the generated content and trending hashtag."""
    trending_topics = get_trending_topics()
    filtered_trends = filter_trending_topics(trending_topics)
    
    if filtered_trends:
        trending_hashtag = filtered_trends[0]  # Pick the first relevant trending topic
        tweet_text = generate_tweet() + " " + trending_hashtag
        try:
            client.create_tweet(text=tweet_text)
            print(f"Tweeted: {tweet_text}")
            return {"status": "success", "tweet": tweet_text}
        except tweepy.TweepyException as e:
            print(f"Error posting tweet: {e}")
            return {"status": "error", "message": str(e)}
    else:
        print("No relevant trends found.")
        return {"status": "error", "message": "No relevant trending topics found."}

if __name__ == "__main__":
    post_tweet()
