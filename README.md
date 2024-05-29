
# FETCH DATA PIPELINE

This project uses Python (pandas) for extracting and parsing nested json files to a more structured database. The files are then transformed and saved as SQL files, in case one wants to create a SQL database with them. A more easier approach is to convert the pandas dataframes to csv for basic EDA as well.

Here's a very basic data model.

## ER Diagram
![ER Diagram](/assets/erdiagram.png)


## Star Schema
![Modeling](/assets/datamodel.png)

# SQL Queries

#### What are the top 5 brands by receipts scanned for most recent month?

![Query 1](/assets/query1.png)

In this query, the most recent month comes out to be March 2021. However, the data (brandname '.') is clearly incorrect. If we consider brandnames with certain conditions, we can see the results of top 5 brands - Huggies, Pepsi, Knorr, Kleenex and Klondike.

#### When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

As we can see in this query that 'rewardsReceiptStatus' has no definition of 'Accepted'. In this case, a good question to ask to stakeholders is to ask for more accurate data or clarify the definition of an 'Accepted' status for receipts.

But to answer the asked question, we can clearly see that 'Rejected' as average spending around 23.3 whereas 'Finished' has average spending of 80.85, which makes the second category greater.

![Query 2](/assets/query2.png)

#### When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

Same ambiguity in definition applies in this query as well. To answer the question in hand, if we assume 'Finished' as 'Accepted'; then 'Finished' has 8184 purchased items whereas just 173 purchased items were 'Rejected'.

![Query 3](/assets/query3.png)

#### Which brand has the most spend among users who were created within the past 6 months?

![Query 4](/assets/query4.png)

I've queried top 3 brands with most spend amongst users created '6 months prior to latest date in the data'. Which makes Pepsi as our answer.
A data quality issue while answering the query was that the data is stale because it returns no rows when queried for users created in 6 months from today's date (May 2024).


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

