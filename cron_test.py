from datetime import datetime

f = open("test.txt", "a")
f.write('\n' + str(datetime.now()))
f.close()

# /Documents/PersonalProjects/Natural-Strength-Building/cron_test.py


# Works
#   * * * * * python /Users/jasonzhang/Documents/PersonalProjects/Natural-Strength-Building/cron_test.py


# Works
# * * * * * cd Desktop && python test.py >> output.txt

# * * * * * /Users/jasonzhang/opt/anaconda3/bin/python

# * * * * * cd Documents/PersonalProjects/Natural-Strength-Building && /Users/jasonzhang/opt/anaconda3/bin/python records_scraping.py

# * * * * * cd Documents/PersonalProjects/Natural-Strength-Building && /Users/jasonzhang/opt/anaconda3/bin/python  records_scraping.py
