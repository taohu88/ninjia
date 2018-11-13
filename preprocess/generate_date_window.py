import sys
import datetime

def date_to_file(dt, file_name):
    with open(file_name, mode='w', encoding='utf-8') as f:
        f.write("%s\n" % dt.strftime("%Y-%m-%d"))


dateStr = sys.argv[1]
if dateStr == "":
    dt = datetime.date.today()
else:
    dt = datetime.datetime.strptime(dateStr, "%Y-%m-%d")

print('Date is %s' % dt)

step = sys.argv[2]

if step == "":
    step = "-7"
step = int(step)

days = datetime.timedelta(days=step)

if step > 0:
    startDate = dt
    endDate = dt + days
else:
    endDate = dt
    startDate = dt + days
print('Start date is %s and end date is %s' % (startDate, endDate))

startFile = sys.argv[3]
endFile = sys.argv[4]

print('Writing %s to file %s' % (startDate, startFile))
date_to_file(startDate, startFile)

print('Writing %s to file %s' % (endDate, endFile))
date_to_file(endDate, endFile)
