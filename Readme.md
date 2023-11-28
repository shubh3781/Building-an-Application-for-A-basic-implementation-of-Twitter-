Flask==2.0.3
google-cloud-datastore==2.4.0
google-auth==1.30.0
requests==2.27.1
google-cloud-storage


Building an Application for A basic implementation of Twitter 

Common features: 
Sign In page 
Page: index.html 
Function used: signin() 
Description: Firebase UI for login. 
The user also can log in to the program. After successful authentication, the 
application determines whether the user is a new user. A new user is led to a 
another page where he can fill out various information. 
Timeline Page 
Page: timeline.html 
Function: timeline() 
Description: 
This the landing page for users when they are logged in, if a new user logs in 
he/she must enter their username and full name to proceed further. Appropriate 
checks in timeline() function have been applied to ensure this. 
This page displays 50 tweets consisting of tweets of current user and all other users 
he is following. To achieve this a function, get_following_tweets() is used which 
takes in email of current user as a parameter. 
This function loops through tweets of current user and his following, and return 
them in a sorted list in reverse chronological order. Which are then displayed on 
the timeline page. 
Profile Page 
Page: profile.html 
Function: profile() 
Description: 
This page displays profile of a user, it includes full name, user name, email, bio, 
number of followers and following and user’s 50 recent tweets in reverse 
chronological order. 
The function profile() fetches all this data from datastore and renders the profile 
page. 
On this page, a user can edit his short profile and name. This is done through a 
function editprofile() which accepts the edited data posted from the page and 
update it in datastore. 
A user can also edit or delete his tweets that are displayed on this page. This is 
done through the functions updatetweet() and deletetweet() respectively. 
A user can follow or unfollow another user if he visit their profile. 
This is achieved by addfollower() and removefollower() functions which fetches 
the following and followers list of both the users and append or remove the 
usernames from them. 
Search Page 
Page: search.html 
Function: search() 
Description: 
This page shows the result of your search, that is either a username or a tweet 
depending on your keyword and search query. 
The search() function is responsible for handling this task, it fetches matching 
usernames from datastore if you have searched a username or it fetches tweets 
consisting of the content you have searched for. 
Functions used for CRUD operations: 
 fetch_user_by_username(username): 
Parameter(s): username of a user 
Functionality: fetches user entity for given username. 
 fetch_user_by_email(email): 
Parameter(s): email of a user 
Functionality: fetches user entity for given email. 
 fetch_all_user(): 
Parameter(s): None 
Functionality: fetches all user entities. 
 create_user(claims, username, fullname): 
Parameter(s): claims, username, fullname 
Functionality: creating a new user by inserting email, username and 
fullname. 
 update_profile_name(email, full_name, profile): 
Parameter(s): email, full_name, profile 
Functionality: updates an existing user’s full name and profile. 
 get_profile(email): 
Parameter(s): email 
Functionality: fetches tweets of logged in user sort them in reverse 
chronological order. 
 add_follower_following(email, username): 
Parameter(s): email, username 
Functionality: fetches both the current user and the user he is following. 
and appends respective usernames to following and follower list. 
 remove_follower_following(email, username): 
Parameter(s): email, username 
Functionality: fetches both the current user and the user he is following. 
and removes respective usernames from following and follower list. 
 add_tweet(tweet, user): 
Parameter(s): tweet, user 
Functionality: add a new tweet to a user entity. 
 delete_tweet(email, id): 
Parameter(s): email, id 
Functionality: deletes a particular tweet of a user. 
 update_tweet(email, tweet): 
Parameter(s): email, tweet 
Functionality: updates tweets of a user by appending given tweet. 
 get_following_tweets(email): 
Parameter(s): email 
Functionality: fetches tweets from all users and current user and sort them in 
reverse chornological order. This is done to make the timeline. 
 fetch_tweet(value): 
Parameter(s): value 
Functionality: fetches tweets based on the given value in their content. Used 
in searching particular content in tweets.