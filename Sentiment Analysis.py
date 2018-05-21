from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import csv


# Sentiment analysis using SIA

sia = SIA()
pos_list = []
neg_list = []
neutralCounter = 0
positiveCounter = 0
negativeCounter = 0

fileCounter = 1
i = 2 #=---from 18 May ->January 2
sentimentList=[]
j=0


while fileCounter < 148:

    with open(str(fileCounter), "r", encoding='utf-8', errors='ignore') as file:
        fileCounter += 1
        firstLine = file.readlines(1)

        if 'Daily Discussion,' not in firstLine[0]:
            continue

        for line in file:
            res = sia.polarity_scores(line)
            if res['compound'] > 0.2:
                positiveCounter+=1
            elif res['compound'] < -0.2:
                negativeCounter+=1
            else:
                neutralCounter+=1

    totalSentiment = positiveCounter+negativeCounter+neutralCounter;
    sentimentList.append((positiveCounter-negativeCounter)/totalSentiment)


print('Length is'+str(len(sentimentList)))

# with open('SIA_test.csv', 'w') as csvfile:
#     fieldnames = ['SIA']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#
#     while j<10:
#         writer.writerow({'SIA': sentimentList[j]})
#         j+=1

