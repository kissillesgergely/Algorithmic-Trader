# Algorithmic Trader

This application currently implements the logic of mean reversion trading integrated with the Alpaca API.

❗ Disclaimer: This software serves only practice purposes. It is not an approved trading bot.

This application and the author don't qualify mean reversion trading as a good
or bad strategy, it is just implemented in frames of this program.
## How the application works

The core of the application is a scheduler which is responsible to collect 
market data in pre-defined time intervals from the Alpaca API. The data is
fetched on weekdays and during market hours
(it doesn't keep track of bank holidays, which can cause unwanted order placements on those weekdays).

The data request happens according to a predefined list of stock symbols.

Step 1.\
Once the information is available the application calculates the moving averages
for the symbols. If the current price is above the moving average by a pre-determined
percentage then it places a sell order for the given stock. If it is below the moving
average a buy order is initiated.

Step 2.\
If there is an open position then the algorithm checks if the current value has
moved close enough (determined by another percentage) to the moving average. In case it has,
the position gets closed. This only for works with fulfilled positions
(if an order has been placed but not fulfilled the algorithm will still according to Step 1)



## How to run the application

Set up an Alpaca account and generate API credentials for your **paper** account
(it means it will operate with not real money with but "paper" money).

Add your base url and credentials as environment variables as:

`APCA_API_BASE_URL`\
`APCA_API_KEY_ID`\
`APCA_API_SECRET_KEY`

You will also need a running database MySQL database. To be able to connect to it
change the default credentials in `logs/settings.py`.

Once you have access to the database run the database migrations:\
`python manage.py makemigrations`\
`python manage.py migrate`

Run the application using the command `python manage.py runserver --noreload`.
The option `--noreload` is important in order not to start the scheduler
multiple times.

You can see the trading logs under `logs/info.log`. You can also check out your
Alpaca dashboard at your Alpaca account.