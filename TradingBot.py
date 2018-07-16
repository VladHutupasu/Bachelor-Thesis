import gatheringFeatures
import gatherFeaturesTrade
import SVM_bitcoin
import threading
from tkinter import *
from tkinter import messagebox

enableButton = 0
btnTest = None
btnTrain = None
btnStart = None

def createLabels(labels, window):
    for i in range(len(labels)):
        lbl = Label(window, text=labels[i], font=("Arial Bold", 10))
        lbl.grid(column=0, row=i+2)

def createSpace(col, row, window):
    lbl = Label(window, text="", font=("Arial Bold", 16))
    lbl.grid(column=col, row=row)

def clickedGatherTrainData():
    btnTrain.config(state=DISABLED)
    thread = threading.Thread(target=gatheringFeatures.gatherFeaturesAndMakeSIA, args=['2018-04-03', '2018-06-02', False])
    thread.start()
    print('Finished gathering features for train data!')

def clickedGatherTestData():
    btnTest.config(state=DISABLED)
    thread = threading.Thread(target=gatherFeaturesTrade.gatherFeaturesAndMakeSIA, args=['2018-06-03', '2018-07-14', False])
    thread.start()
    print('Finished gathering features for test data!')

def clickedTrade():
    messagebox.showinfo('Info', 'Good luck!')
    thread = threading.Thread(target=SVM_bitcoin.trainAndtest, args=[int(txtInvestment.get()), int(txtDistributionDays.get()),
                                                                     float(txtShortPercentage.get()), float(txtLongPercentage.get())])
    thread.start()

def checkButtons():

    while not (btnTrain['state']=='disabled'):
        pass
    btnTest.config(state="normal")
    while not (btnTest['state']=='disabled'):
        pass
    btnStart.config(state="normal")


def main():
    window = Tk()

    window.title("Trading Bot")
    window.geometry('600x500')


    lbl = Label(window, text="Settings", font=("Arial Bold", 16))
    lbl.grid(column=0, row=0)

    createSpace(0, 1, window)

    # CREATE LABELS
    labels = ['Enter investment value ($):', 'Create distribution for each day for its (n) previous days :',
              'Go short when movement percentage smaller than (%):',
              'Go long when movement percentage higher than (%):']
    createLabels(labels, window)

    # TEXT BOXES
    global txtInvestment
    txtInvestment = Entry(window, width=10, state="normal")
    txtInvestment.grid(column=1, row=2)
    txtInvestment.focus()

    global txtDistributionDays
    txtDistributionDays = Entry(window, width=10, state="normal")
    txtDistributionDays.grid(column=1, row=3)

    global txtShortPercentage
    txtShortPercentage = Entry(window, width=10, state="normal")
    txtShortPercentage.grid(column=1, row=4)

    global txtLongPercentage
    txtLongPercentage = Entry(window, width=10, state="normal")
    txtLongPercentage.grid(column=1, row=5)

    # BUTTONS
    createSpace(0, 6, window)
    global btnTrain
    btnTrain = Button(window, text="Create csv file for training", bg="green", fg="white", command=clickedGatherTrainData)
    btnTrain.grid(column=0, row=7)

    global btnTest
    btnTest = Button(window, text="Create csv file for testing", state=DISABLED, bg="green", fg="white", command=clickedGatherTestData)
    btnTest.grid(column=0, row=8)

    global btnStart
    createSpace(0, 9, window)
    btnStart = Button(window, text="Start trading", state=DISABLED, bg="red", fg="white", command=clickedTrade)
    btnStart.grid(column=0, row=10)

    thread = threading.Thread(target=checkButtons)
    thread.start()


    window.mainloop()


if __name__ == "__main__":
    main()