from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
positiveCounter=0
negativeCounter=0
neutralCounter=0
fileCounter=0

while fileCounter < 32:
    fileCounter+=1
    positiveCounter = 0
    negativeCounter = 0
    neutralCounter = 0
    with open('redditCommentsBitcoinMarkets/' + str(fileCounter), "r") as file:
        print(file.readline(60))
        for line in file.readlines():
            ss = sid.polarity_scores(line)
            if ss['compound'] > 0.2:
                positiveCounter += 1
            elif ss['compound'] < -0.2:
                negativeCounter += 1
            else:
                neutralCounter += 1
            # for k in sorted(ss):
            #     print('{0}: {1}, '.format(k, ss[k]), end='')
            # print()

    # print('Positive: '+str(positiveCounter)+' | Negative: '+str(negativeCounter)+' | Neutral: '+str(neutralCounter)+' | FOR number->'+str(fileCounter))
    print(str(((positiveCounter-negativeCounter)/(positiveCounter+negativeCounter))*1000)+' | FOR number->'+str(fileCounter))