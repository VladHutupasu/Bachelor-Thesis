import pandas as pd
import numpy as np
from sklearn import svm
import sklearn.decomposition as pca
from tkinter import messagebox
import Distribution
from datetime import timedelta, datetime



def predict_movement(day_diff, volatility, sia, model):
    if(model.predict([[day_diff, volatility, sia]])) == 0:
        return 'Down'
    else:
        return 'Up'

def trainAndtest(money, prevDays, short, long):

    initialMoney = money

    train_data = pd.read_csv('train.csv')
    test_data = pd.read_csv('trade.csv')

    train_data['Volume'] = train_data['Volume']/1000000
    test_data['Volume'] = test_data['Volume']/1000000

    print('Length train data: '+str(len(train_data)))
    print('Length test data: '+str(len(test_data)))


    # Specify inputs for the model
    imp_features = train_data[['Day Diff', 'SIA', 'Volatility']].as_matrix()
    movement_label = np.where(train_data['Movement']=='Up', 1, 0)





    # Fit the SVM model
    model = svm.SVC(kernel='linear')
    print('Fitting model..')
    model.fit(imp_features, movement_label)

    i=0
    accuracy=0

    while i < len(test_data):
        print("*********************************************")
        result = predict_movement(test_data['Day Diff'][i], test_data['SIA'][i], test_data['Volatility'][i], model)
        bet = False
        movement = None

        dateNow = datetime.strptime(test_data['Date'][i], "%Y-%m-%d %H:%M:%S")
        dateBack = dateNow - timedelta(days=prevDays)

        dateNow = datetime.strftime(dateNow, "%Y-%m-%d")
        dateBack = datetime.strftime(dateBack, "%Y-%m-%d")

        print("Create distribution for " + dateBack + " - " + dateNow)
        resultDistr = Distribution.showDist(dateBack, dateNow, 5)
        print(resultDistr)
        up = max(resultDistr)
        down = min(resultDistr)

        if result=='Up' and up[0]>=long:
            print("Going long because Up is ->"+str(up[0]))
            movement = up[0]
            bet = True
        elif result=='Down' and down[0]<=short:
            print("Going short because Down is ->" + str(down[0]))
            movement = down[0]
            bet = True


        if (result == test_data['Movement'][i]):

            if i < (len(test_data) - 1):

                print("TRUE prediction for date: " + test_data['Date'][i])

                if bet:
                    print("NICE! I bet for that")
                    moneyMade = abs(test_data['Close**'][i] - test_data['Close**'][i + 1])
                    print('Money made :' + str(moneyMade) + ' for day ' + str(test_data['Date'][i]))
                    money = money + moneyMade

            accuracy = accuracy + 1

        else:

            if i < (len(test_data) - 1):

                print("FALSE prediction for date: " + test_data['Date'][i])

                if bet:
                    print("oops.. I bet for that")
                    moneyLost = abs(test_data['Close**'][i] - test_data['Close**'][i + 1])
                    print('Money lost :' + str(moneyLost) + ' for day ' + str(test_data['Date'][i]))
                    money = money - moneyLost


        if result == test_data['Movement'][i] and bet:
            messagebox.showinfo("Result", "Date: " + dateNow + "\n\nI predicted a " + result + " movement, with a possibility of a " + str(movement) + "% price movement."
                                +"\n\nNice! It seems I was correct.\nYou won "+str(round(moneyMade,2))+"$")

        elif not result == test_data['Movement'][i] and bet:
            messagebox.showinfo("Result", "Date: " + dateNow + "\n\nI predicted a " + result + " movement, with a possibility of a " + str(movement) + "% price movement."
                                + "\n\nOops, it seems I was wrong..\nYou lost " + str(round(moneyLost,2)) + "$")

        elif result == test_data['Movement'][i] and not bet:
            messagebox.showinfo("Result", "Date: " + dateNow + "\n\nI predicted a " + result + " movement, with a possibility of a " + str(movement) + "% price movement."
                                + "\n\nOops, it seems you did not bet because of the price movement probability")

        elif not result == test_data['Movement'][i] and not bet:
            messagebox.showinfo("Result", "Date: " + dateNow + "\n\nI predicted a " + result + " movement, with a possibility of a " + str(movement) + "% price movement."
                   + "\n\nGood decision! You did not bet, because the of the price movement probability")
        i+=1



    final_accuracy = accuracy/len(test_data) *100
    print('ACCURACY IS:'+str(final_accuracy)+'%')
    print('Wallet balance is at: '+str(money))

    finalProffitLoss = money-initialMoney

    if finalProffitLoss>0:
        messagebox.showinfo('Conclusion', 'Accuracy: '+str(round(final_accuracy,2))+'%\n\nFinal wallet balance: '+str(round(money,2))+"$"+
                            "\n\nProffit: "+str(money-initialMoney))
    else:
        messagebox.showinfo('Conclusion',
                            'Accuracy: ' + str(round(final_accuracy, 2)) + '%\n\nFinal wallet balance: ' + str(
                                round(money, 2)) + "$" +
                            "\n\nLoss: " + str(round(finalProffitLoss,2))+"$")


# trainAndtest(10000, 2, -0.2, 0.2)
