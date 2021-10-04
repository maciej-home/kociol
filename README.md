# Important info
Everything in this repo and organization is what I'm using in my `"smart" home` system. It's mostly heavily tailored for my usage, but I will be happy if you find it useful  
If you have some suggestions, please open a github issue. Thank you :)  
Please note that I don't give any guarantees nor I take responsibility for using anything in this repo :)  
Some parts of code (e.g. comments) may be in Polish. Sorry for that

I'm also using this repo for learning git, so please report git-related issues too :) 

# What this program does?
It's small script I wrote in order to process data read from iNode Energy Meter by official bash script  
I'm using this energy meter to count how many fuel my stove has used
I'm sending this data to domoticz

# TODOs (in order of priority)
- [x] send data to domoticz
- [ ] coal left in fuel container
- [ ] days left to coal refill
- [ ] hours left to coal refill
- [x] previous month coal usage
- [ ] send data to homeassistant

# Installation
### Installation instructions below are very low quality! Do not blindly copy-paste them, it will not work!
```bash
pip install -r requirements.txt
su - postgres
createuser --pwprompt kociol_user
createdb --encoding=UTF8 --owner=kociol_user kociol
```
psql
```
CREATE TABLE test_table (
	measurement_id SERIAL PRIMARY KEY,
	measurement_time timestamp,
	measurement integer
);
```
