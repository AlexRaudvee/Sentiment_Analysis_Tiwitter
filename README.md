# DBL Data chalenge Group-24

This project revolves around the question of how to compare the performance of airlines when they use Twitter as a communication channel. The dataset we are analyzing consists of a large number of tweets from several airlines, and we asked, in a role-playing game, to analyze the data for one of our clients. Our client is one out of several possible airlines, the assigned airline is interested in assessing their performance when using Twitter as a communication channel. They are interested in comparing their performance to other airlines in general and an assigned competitor airline in particular. Our airline will be represented by an airline marketeer. The marketeer wonders whether their Twitter team is doing a good job and whether this is useful for the company, particularly in comparison to the competitor airline.

Our Client: EasyJet
Our Competitor: British Airways

## About The Data

All the data can be found [here](https://surfdrive.surf.nl/files/index.php/s/Dz082kih8yMGB5P), given dataset is represented as multiple json files containing the information about posted tweets, during the project this raw data were loaded and saved in the database usin SQLite

## Files Discription
      
  create_database.ipynb - file where we create the database and loading the data in the database
  
  retriving_data.ipynb - in this file we exploring the data that we have
  
  sentiment_analysis.ipynb - in this file we provide sentiment analisis on Tweets
    
  sentiment_analysis_vis.ipynb - code for visualizations about sentiment analysis
  
  main_visualisations.ipynb - Jupiter Noutbook with the main code for first and main visualisations
  
  accuracy_of_the_model.ipynb - file with code for measusring the accuracy of the model that we use
  
  get_conversations.ipynb - file with code for getting conversations and storing them in csv file 
  
  sentiment_on_conversations_pre.ipynb - file with code for preprocessing the data for future sentiment analysis on conversations (not used)
  
  sentiment_on_conversations_vis.ipynb - file with the code for visualisations about sentiment analysis on conversations (not used)
 
  poster_vis.ipynb - the file that we use for the demo, it generates the plots that we use in the poster for specific time period 
  
  get_reply_percentage.ipynb - the code used for further analysis, later on this code was used in one of the previous files
  
  get_geo.ipynb - file used for analysis and exploring the data about geolocations that are avaliable and how can we use them, later on was used in one of the previous files 
  
  difference_sen_resp_vis.ipynb - file used for additional visualisation to confirm our thoughts and used in one of the previous files 
  
  change_of_sentiment_in_convs.ipynb - file used to discover how sentiment changes during the conversation, later on used in one of the previous files


## How To Run


  
  ONNX_SENTIMENT.ipynb - code that have been used for providing the sentiment analysis on the whole set of tweets, then scrip have been used to store the data from the csvs to the database
  
  
  
