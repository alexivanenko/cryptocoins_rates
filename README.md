# CryptoCoins Rates Telegram Bot

## Subscribe to 3 times per day your favourite crypto coins USD rates or check it yourself in the bot 

### Requirements

CryptoCoins Rates Bot version 0.1 requires Python >= 3.0 and MongoDB >=3.2.x

##### Installation

```sh
$ git checkout https://github.com/alexivanenko/cryptocoins_rates.git 
$ pip install -r requirements.txt
```

Run mongo console and then:
```sh
> use admin
> db.createUser({user: "crypto_coin", pwd: "your_password_here", roles: [ { role: "userAdmin", db: "crypto_coins" }, {role : "readWrite", db : "crypto_coins"} ]})
> db.updateUser("crypto_coin", {roles : [{ role : "readWrite", db : "crypto_coins"  }, { role: "userAdmin", db: "crypto_coins" }, { role: "dbAdmin", db: "crypto_coins" }]})
> use crypto_coins
```
Don't forget to change password. 
Add Mongo authentication credentials to the config.json file.

Run the bot in the background:
```sh
$ nohup ./python cryptocoins_bot.py & 
```

If you want to send crypto coins rates to users 3 times per day please add the cryptocoins_rates_manager.py to the crontab - setup every minute cron job.  
