from datetime import datetime

f = open("test.txt","a")
f.write(str(datetime.now()))
f.close()

# /Documents/PersonalProjects/Natural-Strength-Building/cron_test.py



#   * * * * * python /Users/jasonzhang/Documents/PersonalProjects/Natural-Strength-Building/cron_test.py

# * * * * * cd Desktop && python test.py >> output.txt