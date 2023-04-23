import tweepy
import os
import openai

def openAI():
    openai.organization = "org-CLFZ9je7cd5PzOefNeu46i1q"
    openai.api_key = os.getenv("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")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f'find 5 main keyword in this sentences Every vehicle we sell, battery we install & solar panel we add moves the needle in the direction of a sustainable future.Thank you to the Tesla team, customers & supporters for bringing us closer to our goal!Happy Earth Day)'}
        ]
    )

    print(completion.choices[0].message)
def twitter():
    # Your Twitter API credentials
    consumer_key = "nu3QdJDVvDzAl6SFcv3tgKpVW"
    consumer_secret = "3L7SBaEvmCmFGsGIScWAXNrw8MGdBhJhklV1eCKlcSKpP2zA9s"
    access_token = "295548817-7AQJdkNhE6V7bcBPyp6doUxYVkw1WS16mJUeipq8"
    access_token_secret = "dzapd3dIA7DGu93S3B1HZMfQCgtL6AL2HN73OHYx5vKCr"

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Get the top 10 trending topics related to cryptocurrency in the United States
    trends = api.get_place_trends(23424977)
    crypto_trends = [t for t in trends if "cryptocurrency" in t["name"].lower()][:10]

    # Print the top 10 trending topics related to cryptocurrency in the United States
    for i, trend in enumerate(crypto_trends):
        print(f"{i + 1}. {trend['name']}")
def main():
    openAI()

if __name__ == "__main__":
    main()