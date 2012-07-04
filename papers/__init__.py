'''This application will store and display relevant publications.

Goals for this App
==================

* This might include papers from the lab or interesting papers.  
* I would like to include a comment thread for each paper, probably using Disqus.
* The goal is also to use API's from Altmetric, Mendeley, PMC and PLOS to also display altmetrics for these papers.
* Another idea is to have hidden discussions of papers, or papers which are not publicly displayed.

There are two options for the best way to store these.
1. One way is the make an API call to Mendeley to get a list of all my and favorite papers and their associated metadata
2. Another way is to download and store the papers via the API in the database using a recurring script like cron.
3. A third way would be to have a mendeley database available to the server which can be queried directly.  In this case I would need to figure out how to update that database.

'''