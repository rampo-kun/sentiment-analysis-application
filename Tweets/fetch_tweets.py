import requests
import time

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANSkwwEAAAAAEH8s7Rg1FLyrQRmSPF1ABKlSSoY%3Dj738woqC3sHkCU4rhVXrqCVmrnNuGeEKCL0yTLpZNlE2wEELtc"

API_URL = "https://api.x.com/2/tweets/search/recent"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

params = {
    "query": "education policy India OR education reform India",  # Updated search query
    "max_results": 100,
    "tweet.fields": "created_at,text",
}


def fetch_tweets_and_save():
    all_tweets = []
    next_token = None
    tweet_count = 0

    while tweet_count < 50:  # Stop once we have 50 tweets
        if next_token:
            params["next_token"] = next_token

        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()

            if 'data' in data:
                for tweet in data['data']:
                    tweet_text = tweet['text']
                    all_tweets.append(tweet_text)
                    tweet_count += 1

                    if tweet_count >= 50:
                        break

            next_token = data.get('meta', {}).get('next_token')

            if not next_token or tweet_count >= 50:
                break

        else:
            print(f"Error fetching tweets: {response.status_code}")
            break

        time.sleep(1)

    with open("indian_education_policy_tweets.txt", "w", encoding="utf-8") as file:
        for tweet in all_tweets:
            file.write(tweet + "\n")

    print(
        f"Saved {len(all_tweets)} tweets to 'indian_education_policy_tweets.txt'")


if __name__ == "__main__":
    print("Fetching tweets about Indian education policy...\n")
    fetch_tweets_and_save()
