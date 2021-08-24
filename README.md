# CoviBot Documentation

# Introduction:
CoviBot is an all-in-one centre for covid needs. Made with a framework library called dicord.py using the immensely popular and growing coding language Python 3.9. This bot can give stats, tell the status of nearest hospitals and most importantly predict future Covid 19 active cases values of India!
Let's see about things it contains in detail:

# Discord.py:
Discord is an extremely popular chatting and connecting site for building communities and overall having a good time with your friends. The audience is mostly young so the bot had to have easy commands and results in layman language. While in a group in Discord called a guild or server you can chat with anyone on it. Discord.py help make automatic response bots for it. Typing a special prefix and then a command activates the bot which is online 24/7. The script is written with repl.it to collaborate and uptime robot to keep it running. Let’s see some commands we provide:
1) c!info:
This command gets all covid values across India
and displays them with a powerful tool provided by
discord called embeds. It gives information of:
i.	Active Cases in the world
ii.	Total Confirmed Cases in the world
iii.	Cumulative Recovered Cases in the world
iv.	Total Deaths in the world
2) c!hospital <Name Of City In India>:
The command gives all information of hospitals 
in your city, like Total Hospitals and Total Open
Beds. This uses the library INDICovid19.
3) c!issafe <Name Of City In India>:
The command evaluates and gives information
about the city, you type and tells if it is safe or not.
4) c!test <symptoms>:
This command does a little test through
thresholding Covid factors in their severity and tells
if you should consider getting tested or not.
5)c!predict:
The main highlight is the predict command, which
uses updating .csv files from GitHub and uses them
to train an ARIMA(p, d, q) machine learning model.
This uses the order 2, 1, 5 and has very low error
coefficients (Average 0.03). This can tell the cases of the day after
and plots a graph using Plotly to plot these in a
visually appealing manner and sends that chart in
the chat.
6)c!help:
	This function is there for giving new users a gist of what is inside the bot and how to use the functions.



# The Website
CoviBot has its own place on the web! We have made a website, made fully with python dash html components which will display our bot features in a website view. It has the Covid snapshots of the world, five day forecast predictions and a map with all the vaccination centres in India. The website has the link to add the discord bot to the server you like.
The Website
All source codes are uploaded on a git on GitHub which has the link:
# Questions:
1)  Why did we decide to do this project?
We both have always been tech geeks in our school since our parents got us a computer and we are well known in our school as the techies.We both know five programing languages and have experience in a lot of different software. So when the point arose about the Covid AI competition, even in Python, so we had to join!
2) Why did we choose the No-Code or with Code option?
We both have plenty of experience with Python with Sidhharth having made games for a lot of time, and Neev being into discord.py and machine learning, then again this was totally our playground to play in!
3) What was the most fun part for the team?
The most fun part was probably trying to figure out the millions of errors we got, with the help of our mentor Swapnil Sangal who is a Btech Computer Science, he used to work as a data scientist in Mercedes Benz and now works as a Product Manager at a growing online coding class platform Tekie it was mostly a bit faster!
4) What was the easiest part?
The easiest part was probably setting up the through discord.py and connecting to the discord API through a token.
5) What challenges did we face?
As well known the hardest part was the machine learning part, trying to find a suitable training dataset which updated daily. After finding that researching for the right machine learning model which we ended up using ARIMA by statsmodels. Then trying to clean the data, get it ready to fit in the model also gave us little hiccups but ultimately after 2 weeks of analysing we ended up prepared!
6) What did we learn?
We learnt a barrelful of machine learning and data analysis by doing this project and would help us contribute to our country further in the future, also learning to troubleshooting and look and looking at errors taught us patience.

This was very fun for each one of us and we would like to say thanks for giving us this opportunity to help out motherland and a platform to display our skills, Such initiatives and competitions do stir child’s interest and build entrepreneurial skills as well, wishing you a good day!

Regards
The CoviBot Team


