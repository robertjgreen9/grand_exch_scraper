# grand_exch_scraper
Scrapes the prices and timestamps for various items from RuneScape's Grand Exchange API and writes them to a MySQL database.

Makes calls to https://api.weirdgloop.org/exchange/history/rs/latest?id={id} and writes their name, price and scraped timestamp (YYYY-MM-DDTHH:MM:SS.000Z) to a linked MySQL database.

The MySQL database credentials are logged in the .env file.

So far, only tested on Windows 11.

To do list:
- Write a function to allow new users to populate the .env config file with the command line
- Make item selection more dynamic by including a dictionary of item names and IDs
