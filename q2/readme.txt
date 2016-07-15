This question is a little difficult for me as
    1. I am not familiar with DataFrame operations;
    2. Some missing addresses in the excel file;
    3. The details location of company in Bermuda is hard to get;
    4. Google have a very strict constraint on free accounts for query geocode information

To solve the above problems, I use the following methods.
    1. Use a package "geocoder" to do the test and use "googlemaps" package in the formal solution.
    2. For those company lacks address, I collect address data from "U.S. Securities and Exchange Commission"
    3. For companies in Bermuda, just get a rough geocode.
