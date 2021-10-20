import math
import datetime
import requests

Today = datetime.datetime.utcnow() #datetime.datetime(2020, 12, 31, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
Month = {
  "Jan": 1,
  "Feb": 2,
  "Mar": 3,
  "Apr": 4,
  "May": 5,
  "Jun": 6,
  "Jul": 7,
  "Aug": 8,
  "Sep": 9,
  "Oct": 10,
  "Nov": 11,
  "Dec": 12
}
ColHeader = ["Date","Open","High","Low","Close","AdjClose","Volume"]
TotalDay = [0,0,0,0,0] #Mon=0 > Fri =4
TotalDayPositive = [0,0,0,0,0] 

def process_table(_html: str) -> str:
	result = ""
	cacheDayData = ""
	weekday = 0
	counter = 0
	tmrCloseValue = 0
	tmrPL = 0
	openCloseDiff = 0
	resultByDay = _html.split("</tr>")

	for dayData in resultByDay:
		if cacheDayData:
			result= f"{result}{cacheDayData}"
			cacheDayData = ""
							
		counter = 0;
		shareData = dayData.split("</span>")
		for sData in shareData:
			data = sData.split(">")
			if((data[-1]).strip()):
				if(counter ==0):
					date = (data[-1]).strip().replace(",","")
					cacheDayData= f"{cacheDayData}\n\"{date}\":"+'{'
					dateInfo = date.split(" ")
					weekday = datetime.datetime(int(dateInfo[2]), Month[dateInfo[0]], int(dateInfo[1]), 8, 0, 0, 173504).weekday()
				else:
					cacheDayData= f"{cacheDayData}\"{ColHeader[counter]}\": " + (data[-1]).strip().replace(",","") +","
					if(counter ==1):
						openCloseDiff = float((data[-1]).strip().replace(",",""))
					elif(counter ==4):
						tempInt = round(float((data[-1]).strip().replace(",","")),2)
						openCloseDiff = round(tempInt - openCloseDiff ,2)
						tmrPL = round(tmrCloseValue - tempInt,2)
						tmrCloseValue = tempInt
				counter+=1
		if (result) and (counter >0):
			result= f"{result}\"OpenCloseDiff\": {openCloseDiff},\"DailyP&L\": {tmrPL}" +'},' +f"{cacheDayData}"
			cacheDayData = ""
			TotalDay[weekday]+=1
			if(openCloseDiff>0):
				TotalDayPositive[weekday]+=1

	#Clear last cache
	result= f"{result}\"OpenCloseDiff\": 0.01,\"DailyP&L\": 0.01" +'}'

	result = '[{\"DLM\": \"'+f"{Today}"+'\",\"SPX\":{' +f"{result}" + '},\n"Statistics": {	}'
	return (f"{result}" + '}]')


def get_spx_data() -> str:
	url = "https://finance.yahoo.com/quote/%5EGSPC/history"
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
	}
	resultStartStr = "Volume</span></th></tr></thead>"
	resultEndStr = "</tbody>"
	startPeriod = math.trunc(datetime.datetime(Today.year, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp())
	endPeriod = math.trunc(datetime.datetime(Today.year, Today.month, Today.day, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp())
	#endPeriod = endPeriod - 86400 #As UTC time earlier than New York time
	Config = {'period1': startPeriod, 'period2': endPeriod, 'interval': '1d', 'filter': 'history', 'frequency': '1d', 'includeAdjustedClose': 'true'}
	print(Config)
	resp = requests.get(url, headers=headers, params=Config)
	resp.raise_for_status()
	resultStr = ((resp.text.split(resultStartStr))[1]).split(resultEndStr)
	
	return process_table(resultStr[0])


def main():
	filename = f"model/{Today.year}.json"

	sourceFile = open(filename, 'w')
	print( get_spx_data(), file = sourceFile)
	sourceFile.close()
	print("Done writing data.")


if __name__ == "__main__":
    main()