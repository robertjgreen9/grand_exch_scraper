# grand_exch_scraper
Scrapes the prices and timestamps for various items from RuneScape's Grand Exchange API and writes them to a MySQL database.

Makes calls to the Grand Exchange API and writes their name, price and timestamp (YYYY-MM-DDTHH:MM:SS.000Z) to a linked MySQL database.

The MySQL database credentials are logged in the .env file.

MySQL table headers:
	`id` int,
	`price` int,
	`timestamp` varchar(255)

Current version is known to work on Python 3.9.2 on Raspberry Pi OS 2023-05-03.


