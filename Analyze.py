from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
positiveCounter=0
negativeCounter=0
neutralCounter=0

with open("sb.txt", "r") as file:
    for line in file.readlines():
        print(line)
        ss = sid.polarity_scores(line)
        if ss['compound'] > 0.2:
            positiveCounter += 1
        elif ss['compound'] < -0.2:
            negativeCounter += 1
        else:
            neutralCounter += 1
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
        print()

print('Positive: '+str(positiveCounter)+' | Negative: '+str(negativeCounter)+' | Neutral: '+str(neutralCounter))