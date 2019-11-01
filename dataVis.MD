# OBJECTIVE
## TOPIC
Visualising social networks is a challenging area of work where connected graph provides a visual abstraction of the social network. In this project we will use tools to visualize social networks and study their evolution over time. Adding weights to the edges to indicate the strength of a relationship along with positive or negative bonding can be explored using different colour scheme. Visual representation is helpful in identifying influential nodes, strong subgroups or cliques, groups with negative association (who can be potential threats), etc.

## WORK
Finding:
 * Nodes: The individuals whose network we are building
 * Edges: The connection between the nodes. It represents a relationship between the nodes of the network.

`Finding the edges/relation between nodes is important now.`

## MY PLANS
### Plan 1:
1. Clean the dataset(only tweet, user, date and time)
2. For each unique user:
    1. Find their last 50 tweets
    2. Classify them into 3 sentiments
    3. Get the overall sentiment of user:
	  4. `Define the user as a node, size as the sentiment`
3. For each tweet:
	`find the tweet's sentiment`
4. For all db:
  `find count of each unique users`

### Plan 2:
1. Get the trending hashtag of any given day
2. Same as [Plan 1](#plan-1)

### Plan 3:
`Word cloud of a user, interactive as time-series, allowing user to view the changes in the posts made over a given time period.`

### Plan 4:
1. Take 1000 random users from twitter.
2. Make a dataset of all hashtags they have used, with the rt, fav and the sentiment of that tweet.
3. Each user is a node.
4. Edge is any two nodes having same hastag.
5. Edge weight, node size, node color, etc can be set after that.

### Plan 5:
1. Take a random user.
2. Get a list of followers the user has.
3. Find all hashtags the user has used, with datetime.
4. Find if his followers have also used the same hashtag.
5. Same as [Plan 4](#plan-4) 's step 4.
6. Datetime will help to create a timeline based approach, allowing us to see how the user used a hashtag, and how his followers increased/decreased the trendings.
7. Over a course of time, it can be seen how some hashtags become more used, and how others wane over time.
8. Find influential nodes, use sentiment analysis of the main user.