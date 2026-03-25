import json
import time
import random
import curl_cffi
import urllib.parse as up

username = ""
token = ""
ct0 = ""

def main():
    try:
        api = API(token, ct0)
        print(f"Fetching {username} tweets in batches")
        batch_number = 1
        cursor = None
        eol = False
        while not eol:
            tweets, cursor, eol = api.get_tweets(username, cursor)
            print(f"Got {len(tweets)} tweets to delete in batch {batch_number}")
            for tweet in tweets:
                api.delete_tweet(tweet)
                time.sleep(random.uniform(5, 10))
            time.sleep(random.uniform(15, 20))
            batch_number += 1
        print(f"Completed deleting {username} tweets")
        print("\n\n--------------------------------\n\n")
        print(f"Fetching {username} retweets in batches")
        batch_number = 1
        cursor = None
        eol = False
        user_id = api.get_id(username)
        if not user_id:
            print(f"Failed to get {username} user id")
            return
        while not eol:
            retweets, cursor, eol = api.get_retweets(user_id, cursor)
            print(f"Got {len(tweets)} retweets to unretweet in batch {batch_number}")
            for retweet in retweets:
                api.unretweet(retweet)
                time.sleep(random.uniform(5, 10))
            time.sleep(random.uniform(15, 20))
            batch_number += 1
        print(f"Completed unretweeting {username} retweets")
    except Exception as e:
        print(f"Error on {e}")
    finally:
        input("Press Enter to exit...")

class API:
    def __init__(self, token, ct0):
        self.session = curl_cffi.Session(impersonate="chrome123")
        headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'origin': 'https://x.com',
            'referer': 'https://x.com/',
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en',
            'x-csrf-token': ct0
        }
        cookies = {
            'auth_token': token,
            'ct0': ct0
        }
        self.session.headers.update(headers)
        self.session.cookies.update(cookies)

    def get_tweets(self, username, cursor=None):
        tweets = []
        eol = False
        features = {
            "rweb_video_screen_enabled": False,
            "payments_enabled": False,
            "profile_label_improvements_pcf_label_in_post_enabled": True,
            "responsive_web_profile_redirect_enabled": False,
            "rweb_tipjar_consumption_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "premium_content_api_read_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
            "articles_preview_enabled": True,
            "responsive_web_grok_analyze_post_followups_enabled": True,
            "responsive_web_jetfuel_frame": True,
            "responsive_web_grok_share_attachment_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_grok_show_grok_translated_post": True,
            "responsive_web_grok_analysis_button_from_backend": True,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "responsive_web_grok_imagine_annotation_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_media_download_video_enabled": False,
            "responsive_web_enhance_cards_enabled": False,
            "rweb_video_timestamps_enabled": False,
            "responsive_web_grok_community_note_auto_translation_is_enabled": False,
            "responsive_web_grok_image_annotation_enabled": True,
        }
        variables = {
            "rawQuery": f"(from:{username})",
            "count": 20,
            "querySource": "typed_query",
            "product": "Latest",
            "withGrokTranslatedBio": False
        }
        if cursor:
            variables["cursor"] = cursor
        try:
            url = f"https://x.com/i/api/graphql/UN1i3zUiCWa-6r-Uaho4fw/SearchTimeline?variables={up.quote(json.dumps(variables))}&features={up.quote(json.dumps(features))}"
            tweet = self.session.get(url)
            assert tweet.status_code == 200, f'Failed to get tweet details. Status code: {tweet.status_code}. Username: {username}'
            j = tweet.json()
            for u in j["data"]["search_by_raw_query"]["search_timeline"]["timeline"]["instructions"]:
                if u["type"] == "TimelineAddEntries":
                    for k in u["entries"]:
                        if "tweet-" in k["entryId"]:
                            try:
                                tweets.append(k["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["id_str"])
                            except:
                                pass
                        if "cursor-bottom-" in k["entryId"]:
                            cursor = k["content"]["value"]
                    if len(u["entries"]) <= 2:
                        eol = True
                        break
                if u["type"] == "TimelineReplaceEntry":
                    try:
                        if "cursor-bottom-" in u["entry"]["entryId"]:
                            if u["entry"]["content"]["cursorType"] == "Bottom":
                                cursor = u["entry"]["content"]["value"]
                    except:
                        pass
        except Exception as e:
            print(e)
        return tweets, cursor, eol
    
    def get_id(self, username):
        features = {
            "hidden_profile_likes_enabled": True,
            "hidden_profile_subscriptions_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "subscriptions_verification_info_is_identity_verified_enabled": True,
            "subscriptions_verification_info_verified_since_enabled": True,
            "highlights_tweets_tab_ui_enabled": True,
            "responsive_web_twitter_article_notes_tab_enabled": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "payments_enabled": False,
            "profile_label_improvements_pcf_label_in_post_enabled": True,
            "responsive_web_profile_redirect_enabled": False,
            "subscriptions_feature_can_gift_premium": True
        }
        variables = {
            "screen_name": username,
            "withSafetyModeUserFields": True,
        }
        fieldToggles = {
            "withAuxiliaryUserLabels": False
        }
        try:
            response = self.session.get(f"https://x.com/i/api/graphql/ZHSN3WlvahPKVvUxVQbg1A/UserByScreenName?variables={up.quote(json.dumps(variables))}&features={up.quote(json.dumps(features))}&fieldToggles={up.quote(json.dumps(fieldToggles))}")
            return response.json()["data"]["user"]["result"]["rest_id"]
        except:
            return False
        
    def get_retweets(self, userId, cursor=None):
        retweets = []
        eol = False
        variables = {
            "userId": userId,
            "count": 20,
            "includePromotedContent": False,
            "withCommunity": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
            "withV2Timeline": True,
            "referrer": "tweet"
        }
        fieldToggles = {
            "withArticlePlainText": False
        }
        if cursor:
            variables["cursor"] = cursor
        try:
            tweet = self.session.get(f"https://x.com/i/api/graphql/E3opETHurmVJflFsUBVuUQ/UserTweets?variables={up.quote(json.dumps(variables))}&features={up.quote(json.dumps(self.features))}&fieldToggles={up.quote(json.dumps(fieldToggles))}")
            assert tweet.status_code == 200, f'Failed to get tweet details. Status code: {tweet.status_code}.'
            j = tweet.json()
            us = j["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
            for u in us:
                if u["type"] == "TimelineAddEntries":
                    for k in u["entries"]:
                        if "tweet-" in k["entryId"]:
                            try:
                                if k["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["retweeted"]:
                                    retweets.append(k["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["retweeted_status_result"]["result"]["rest_id"])
                            except:
                                pass
                        if "cursor-bottom-" in k["entryId"]:
                            cursor = k["content"]["value"]
                    if len(u["entries"]) <= 2:
                        eol = True
                        break
                if u["type"] == "TimelineReplaceEntry":
                    try:
                        if "cursor-bottom-" in u["entry"]["entryId"]:
                            if u["entry"]["content"]["cursorType"] == "Bottom":
                                cursor = u["entry"]["content"]["value"]
                    except:
                        pass
        except Exception as e:
            print(e)
        return retweets, cursor, eol

    def unretweet(self, tweetid):
        data = {"variables": {"source_tweet_id": tweetid, "dark_request": False}, "queryId": "G4MoqBiE6aqyo4QWAgCy4w"}
        response = self.session.post("https://x.com/i/api/graphql/G4MoqBiE6aqyo4QWAgCy4w/DeleteRetweet", json=data)
        if response.status_code == 200:
            print(f"successfully unretweet {tweetid}")
            return True
        else:
            print(f"failed to unretweet {tweetid}")
            return False
        
    def delete_tweet(self, tweetid):
        data = {"variables": {"tweet_id": tweetid, "dark_request": False}, "queryId": "VaenaVgh5q5ih7kvyVjgtg"}
        response = self.session.post("https://x.com/i/api/graphql/VaenaVgh5q5ih7kvyVjgtg/DeleteTweet", json=data)
        if response.status_code == 200:
            print(f"successfully deleted {tweetid}")
            return True
        else:
            print(f"failed to delete {tweetid}")
            return False

if __name__ == '__main__':
    main()
