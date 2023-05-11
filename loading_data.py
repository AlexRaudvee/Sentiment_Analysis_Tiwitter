from  imports import json, os, sqlite3, time
from config import folder_path, path_to_db



file_count = 0
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        with open(os.path.join(folder_path, filename), 'r') as f:
            lst_main = []
            for line in f:
                try:
                    lst_main.append(json.loads(line.strip()))
                    
                except json.JSONDecodeError:
                    print('Error parsing JSON:', line)

            ### USER DATA

            users_fill_values = []

            for tweet_object in lst_main:
                try: 
                    user_tpl = ( tweet_object['user']['id'],  # user_id
                                str(tweet_object['user']['name']), # user_name
                                str(tweet_object['user']['screen_name']),  # user_screen_name
                                tweet_object['user']['followers_count'],  # followers_count
                                tweet_object['user']['friends_count']) # friends_count
                    
                    users_fill_values.append(user_tpl)
                except:
                    continue

            ### ORIGINAL TWEET DATA 

            original_tweets_fill_values = []

            def retrieving_full_text(dictionary):
                f_text = ''
                if dictionary['truncated'] == True:
                    f_text = dictionary['extended_tweet'].get('full_text')
                else:
                    f_text = dictionary['text']
                return f_text

            def retrieving_user_mentions(dictionary):
                user_ment = []
                for user in dictionary['entities']['user_mentions']:
                    try:
                        user_ment.append(user['id'])
                    except: 
                        break
                return str(user_ment)

            def retrieving_hashtags(dictionary):
                hash_lst = []
                for hashtag in dictionary['entities']['hashtags']:
                    try:
                        hash_lst.append(hashtag['text'])
                    except:
                        break
                return str(hash_lst)

            def retrieving_symbols(dictionary):
                symb_lst = []
                for symbol in dictionary['entities']['symbols']:
                    try:
                        symb_lst.append(symbol['text'])
                    except:
                        break
                return str(symb_lst)


            for tweet_object in lst_main:
                try:
                    
                    if (tweet_object['is_quote_status'] == False) and (tweet_object['text'][0:2] != 'RT') and (tweet_object['in_reply_to_status_id'] == None):

                        try:
                            possibly_sensitive = str(tweet_object['possibly_sensitive'])
                            
                        except:
                            possibly_sensitive = str(False)


                        tweet_id = tweet_object['id']
                        user_id = tweet_object['user']['id']
                        full_text = retrieving_full_text(tweet_object)
                        timestamp_ms = tweet_object['timestamp_ms']
                        user_mentions = retrieving_user_mentions(tweet_object)
                        hashtags = retrieving_hashtags(tweet_object)
                        symbols = retrieving_symbols(tweet_object)
                        quote_count = tweet_object['quote_count']
                        reply_count = tweet_object['reply_count']
                        favorite_count = tweet_object['favorite_count']
                        retweet_count = tweet_object['retweet_count']
                        lang = str(tweet_object['lang'])

                        original_tweet_tpl = (tweet_id, user_id ,str(f"""{full_text}"""), str(timestamp_ms), str(lang), str(user_mentions), str(hashtags), str(symbols), quote_count, reply_count, favorite_count, retweet_count, possibly_sensitive)
                        
                        original_tweets_fill_values.append(original_tweet_tpl)
                    
                except:
                    continue


            
            ### REPLIES TWEETS 

            replies_fill_values = []

            for tweet_object in lst_main:

                try:
                    if tweet_object['in_reply_to_status_id'] != None:
                        try: 
                            if tweet_object['truncated'] == True:
                                full_text = tweet_object['extended_tweet']['full_text']

                            if tweet_object['truncated'] == False:
                                full_text = tweet_object['text']
                        except:
                            full_text = None

                        user_mentions = tweet_object['entities']['user_mentions']

                        try:
                            user_mentions_id = []
                            for user in user_mentions:
                                user_mentions_id.append(user['id'])
                        except:
                            user_mentions_id = None
                            
                        try: 
                            hash_lst = []
                            for hashtag in tweet_object['entities']['hashtags']:
                                try:
                                    hash_lst.append(hashtag['text'])

                                except:
                                    continue

                        except:
                            continue

                        try:
                            possibly_sensitive = tweet_object['possibly_sensitive']
                            
                        except:
                            possibly_sensitive = False

                        reply_tpl = (
                            tweet_object['id'],
                            tweet_object['in_reply_to_status_id'],
                            tweet_object['in_reply_to_user_id'],
                            tweet_object['user']['id'],
                            
                            str(f"{full_text}"),

                            str(tweet_object['timestamp_ms']),
                            str(tweet_object['lang']),
                            str(hash_lst),
                            str(tweet_object['entities']['symbols']),

                            str(user_mentions_id),
                            
                            tweet_object['quote_count'],
                            tweet_object['reply_count'],
                            tweet_object['favorite_count'],
                            tweet_object['retweet_count'],
                            str(possibly_sensitive)
                        )

                        replies_fill_values.append(reply_tpl)

                except:
                    continue

            
            ### RETWEET TWEETS 

            retweets_fill_values = []

            for tweet_object in lst_main:
                try: 
                    try:
                        user_mentions_id = []
                        for user in user_mentions:
                            user_mentions_id.append(user['id'])

                    except:
                        user_mentions_id = None

                    try:
                        a = tweet_object['retweeted_status']['id']
                        b = tweet_object['quoted_status']['id']
                        retweeted_and_quoted = True

                    except:
                        retweeted_and_quoted = False

                    try: 
                        hash_lst = []
                        for hashtag in tweet_object['entities']['hashtags']:
                            try:
                                hash_lst.append(hashtag['text'])

                            except:
                                continue

                    except:
                        continue

                    try:     
                        possibly_sensitive = tweet_object['possibly_sensitive']
                            
                    except:
                        possibly_sensitive = False


                    retweet_tpl = (
                        tweet_object['id'],
                        tweet_object['retweeted_status']['id'],
                        tweet_object['user']['id'],
                        str(tweet_object['timestamp_ms']),

                        str(hash_lst),

                        str(tweet_object['entities']['symbols']),
                        
                        str(user_mentions_id),

                        tweet_object['quote_count'],
                        tweet_object['reply_count'],
                        tweet_object['favorite_count'],
                        tweet_object['retweet_count'],
                        
                        str(retweeted_and_quoted),
                        str(possibly_sensitive)
                    )

                    retweets_fill_values.append(retweet_tpl)

                except:
                    continue

            ### QUOTED TWEETS 

            quotes_fill_values = []

            for tweet_object in lst_main:
                try:

                    if tweet_object['is_quote_status'] == True and tweet_object['text'][0:2] != 'RT':
                        try: 
                            if tweet_object['truncated'] == True:
                                full_text = tweet_object['extended_tweet']['full_text']

                            if tweet_object['truncated'] == False:
                                full_text = tweet_object['text']
                        except:
                            full_text = None

                        user_mentions = tweet_object['entities']['user_mentions']

                        try:
                            user_mentions_id = []
                            for user in user_mentions:
                                user_mentions_id.append(user['id'])

                        except:
                            user_mentions_id = None

                        try: 
                            hash_lst = []
                            for hashtag in tweet_object['entities']['hashtags']:
                                try:
                                    hash_lst.append(hashtag['text'])

                                except:
                                    continue

                        except:
                            continue
                        
                        try:
                            possibly_sensitive = tweet_object['possibly_sensitive']
                            
                        except:
                            possibly_sensitive = False


                        quote_tpl = (
                            tweet_object['id'],
                            tweet_object['quoted_status_id'],
                            tweet_object['quoted_status']['user']['id'],
                            tweet_object['user']['id'],

                            str(f"{full_text}"),

                            str(tweet_object['timestamp_ms']),
                            str(tweet_object['lang']),
                            str(hash_lst),
                            str(tweet_object['entities']['symbols']),

                            str(user_mentions_id),

                            tweet_object['quote_count'],
                            tweet_object['reply_count'],
                            tweet_object['favorite_count'],
                            tweet_object['retweet_count'],
                            str(possibly_sensitive)
                        )

                        quotes_fill_values.append(quote_tpl)
                        
                except:
                    continue

            
            ### LOADING USER DATA IN USERS 

            try:

                sqliteConnection = sqlite3.connect(path_to_db)
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                count1 = 0
                failed_count1 = 0
                for i in list(set(users_fill_values)):

                    try:
                        
                        users_fill_query_sql = f"""INSERT INTO 'users' ('user_id', 'user_name', 'user_screen_name', 'followers_count', 'friends_count') VALUES {i}"""
                        
                        rowcount = cursor.execute(users_fill_query_sql)
                        sqliteConnection.commit()
                        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)

                    except Exception as ex:
                        failed_count1 += 1
                        print(ex)
                        continue
                    
                    count1 += 1

                cursor.close()

            except sqlite3.Error as error:
                failed_count1 += 1
                print("Failed to insert data into sqlite table", error)
                
            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("The SQLite connection is closed")
                
                print(f'user data: total:{count1}, failed:{failed_count1}')


            ### LOAD THE ORIGINAL TWEETS DATA IN ORIGINAL_TWEETS

            try:
                sqliteConnection = sqlite3.connect(path_to_db)
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                count2 = 0
                failed_count2 = 0
                for i in original_tweets_fill_values:

                    try:
                        
                        original_tweets_fill_query_sql = f"""
                            INSERT INTO 'original_tweets' (tweet_id, 
                                                            user_id, 
                                                            full_text, 
                                                            timestamp_ms, 
                                                            lang, 
                                                            user_mentions, 
                                                            hashtags, 
                                                            symbols, 
                                                            quote_count, 
                                                            reply_count, 
                                                            favourite_count, 
                                                            retweeted_count,
                                                            possibly_sensetive )  VALUES {i}"""  
                            
                        rowcount = cursor.execute(original_tweets_fill_query_sql)
                        sqliteConnection.commit()
                        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)

                    except Exception as ex:
                        failed_count2 += 1
                        print(ex)
                        continue
                    
                    count2 += 1

                cursor.close()

            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)
            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("The SQLite connection is closed")

                print(f'user data: total:{count2}, failed:{failed_count2}')


            ### LOADING REPLIES TWEETS IN REPLIES 

            try:
                sqliteConnection = sqlite3.connect(path_to_db)
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                count3 = 0
                failed_count3 = 0
                for i in replies_fill_values:

                    try:
                        
                        replies_fill_query_sql = f"""
                            INSERT INTO 'replies' ( 'tweet_id', 
                                                    'in_reply_to_status_id', 
                                                    'in_reply_to_user_id', 
                                                    'user_id', 
                                                    'full_text', 
                                                    'timestamp_ms', 
                                                    'lang', 
                                                    'hashtags',
                                                    'symbols',
                                                    'user_mentions',
                                                    'quote_count',
                                                    'reply_count',
                                                    'favorite_count',
                                                    'retweeted_count',
                                                    'possibly_sensetive' )
                            VALUES {i}
                        """
                                    
                        rowcount = cursor.execute(replies_fill_query_sql)
                        sqliteConnection.commit()
                        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)

                    except Exception as ex:
                        failed_count3 += 1
                        print(ex)
                        continue
                    
                    count3 += 1

                cursor.close()

            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)
            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("The SQLite connection is closed")

                print(f'user data: total:{count3}, failed:{failed_count3}')


            ### LOAD THE RETWEETS TWEETS IN RETWEETES

            try:
                sqliteConnection = sqlite3.connect(path_to_db)
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                count4 = 0
                failed_count4 = 0
                for i in retweets_fill_values:

                    try:
                        
                        retweets_fill_query_sql = f"""
                            INSERT INTO 'retweets' ( 'tweet_id', 
                                                    'retweet_status_id', 
                                                    'user_id', 
                                                    'timestamp_ms', 
                                                    'hashtags',
                                                    'symbols',
                                                    'user_mentions',
                                                    'quote_count',
                                                    'reply_count',
                                                    'favorite_count',
                                                    'retweeted_count'
                                                    'retweeted_and_quoted'
                                                    'possibly_sensetive')
                            VALUES {i}
                        """

                        rowcount = cursor.execute(retweets_fill_query_sql)
                        sqliteConnection.commit()
                        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)

                    except Exception as ex:
                        failed_count4 += 1
                        print(ex)
                        continue
                    
                    count4 += 1

                cursor.close()

            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)
            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("The SQLite connection is closed")

                print(f'user data: total:{count4}, failed:{failed_count4}')

            ### LOAD THE QUOTES TWEETS IN QUOTES 


            try:
                sqliteConnection = sqlite3.connect(path_to_db)
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                count5 = 0
                failed_count5 = 0
                for i in quotes_fill_values:

                    try:
                        
                        quotes_fill_query_sql =f"""
                            INSERT INTO 'quotes' ( 'tweet_id', 
                                                    'quoted_status_id', 
                                                    'quoted_status_user_id', 
                                                    'user_id', 
                                                    'full_text', 
                                                    'timestamp_ms', 
                                                    'lang', 
                                                    'hashtags',
                                                    'symbols',
                                                    'user_mentions',
                                                    'quote_count',
                                                    'reply_count',
                                                    'favorite_count',
                                                    'retweeted_count',
                                                    'possibly_sensetive')
                            VALUES {i}
                        """

                        
                        rowcount = cursor.execute(quotes_fill_query_sql)

                        sqliteConnection.commit()
                        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)

                    except Exception as ex:
                        failed_count5 += 1
                        print(ex)
                        continue
                    
                    count5 += 1

                cursor.close()

            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)
            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("The SQLite connection is closed")

                print(f'user data: total:{count5}, failed:{failed_count5}')

    file_count += 1

    time.sleep(5)
    