import cv2
import mediapipe as mp
import random 

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.8, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

if __name__ == "__main__":
    cap = cv2.VideoCapture(0) # capturing video from our webcam
    detector = handDetector(False,2,0.65,0.65) #creating an object of our Hand Detector class

    #this while loop is testing if detection is happening 
    #is video feed working 
    #press q to exit this loop and then game begins
    while True:
        sucess,img = cap.read() # reading image frame by frame
        img = detector.findHands(img) #method find hands detect hands and join landmarks(represented as points)
        lmList = detector.findPosition(img,0,False)#getting list of posion of landmarks
        cv2.imshow("Image", img)
        if cv2.waitKey(3) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


    #this is major loop which helps to play the game again and again
    play_again = 1
    while play_again == 1:
        play_again = 0;

        #global variables of game
        wicket = 0
        target = 0
        score = 0  


        #this part runs only ones and used for 
        #designing a border line
        #calculating target score according to difficulty level
        print("\n\n\n")
        print("Game Start".center(105,"="),"\n\n") #create a border line


        #taking number of wickets user want to play with
        print("  Choose the number of wicket you want play with (maximum is 3)")
        print("  Please Enter 1 or 2 or 3  accordingly")
        while True:
            wickets = input()
            if wickets == '1' or wickets.lower() == 'one':
                wicket = 1
                break
            elif wickets == '2' or wickets.lower() == 'two':
                wicket = 2
                break
            elif wickets == '3' or wickets.lower() == 'three':
                wicket = 3
                break
            else:
                print("Please Enter the valid input i.e. 1 or 2 or 3")

        #asking difficulty level of game and deciding target
        print("Choose Difficulyt Level \n Enter 1 for Easy \n Enter 2 for Medium \n Enter 3 for Hard")
        while True:
            level = int(input())
            if level == 1:
                target = random.randint(15,25)
                break
            elif level == 2:
                target = random.randint(25,35)
                break
            elif level == 3:
                target = random.randint(35,45)
                break
            else:
                print("Enter valid input i.e. 1 or 2 or 3")
        target = target + (wicket-1)*15;
        #target lies b/w 10 - 135
        print(f"\n   Your Target is {target} \n   Your Score is {score}\n\n")
       

 
        #this loop to play one game
        while True:  
         #==============================================================================
                #detecting and finger counting part of code
            countres=[] #count of nuber of fingers
            while True:
                sucess,img = cap.read() # reading image frame by frame
                img = detector.findHands(img) #method find hands detect hands and join landmarks(represented as points)
                lmList = detector.findPosition(img,0,False)#getting list of posion of landmarks
                if len(lmList) != 0:  
                    open=[] #to store state of finger 1- if finger is open
                    tipids =  [8,12,16,20,4]  #tipids are ID or landmark for tip of finger
                    for i in range(0,4):
                        if lmList[tipids[i]][2]< lmList[tipids[i]-2][2]: #comparing y-coordinate to check if finger is open or closed
                            open.append(1) #if finger is open appending 1
                        else:
                            open.append(0)
                    if lmList[tipids[4]][1] > lmList[tipids[4]-1][1]: #for thumb we need slightly different procedure to check if it is open or not
                        open.append(1)
                    else:
                        open.append(0)
                    countres.append(open.count(1)); #counting the number of open fingers
                cv2.imshow("Image", img)
                if cv2.waitKey(3) & 0xFF == ord('q'):
                    break
            # upto this we have read webcam and got the finger count

         #=====================================================================================
                    #now gaming part of code
            hit = max(countres,key=countres.count) 
            countres.clear()
            if(hit==5):
                hit = 6
            #hit variable in above 3 line of code stores the run you have hit 
            #if you have shown 1,2,3,4 - fingers(opened) it will store score as 1,2,3,4 respectively
            #while if your 5 fingers were opened so which is considered as you have hit a 6
            #so 5 fingers represent a score of -6  ||| 5 -> 6

            chit = random.randint(1,5)
            if(chit == 5):
                chit = 6
            #similar to hit chit is the score or guess by computer
            #similar treatment if guess is 5. i.e 5 converted to 6


            #dot ball case 
            if hit == 0:
                print("Dot Ball\n")
                continue
            #else case
            print(f"You Hit {hit} Computer Guessed {chit}") #printing state of this move
            #below we are making decision and printing current status due to above move
            if hit == chit:
                print("!!OUT!!OUT!!OUT!!")
                wicket = wicket-1
                if wicket == 0:
                    break #this break (if user looses or draw) case
                else:
                    print(f"You Have {wicket} wicket left")
                print()
            else:
                score = score + hit
                print(f"Your Current Score is {score}  and Your Target is {target}")
                print(f"You need {target-score+1} more runs to win\n")

             #if score>target breaking because user won the game
            if score>target:
                break; #this is winning break

         #making final decision of this game
        print("\n\n")
        if score > target:
            print("!! YOU WON !! YOU WON !! YOU WON")
            print(f"You Won by {wicket} wicket")
        elif score == target:
            print("!! DRAW !! DRAW !! DRAW")
            print("Ooopps!! Close One!!")
        else:
            print("YOU LOOSE !! \n Better Luck Next Time")
        #till now gaming part ended

        print("\n\n")
        cv2.destroyAllWindows()
     #==========================current gaming loop ended===================================================
        #asking if user want to play again

        print("Enter 1 if you want to play again else Enter 0")
        while True:
            play_again = int(input())
            if play_again == 1:
                break
            elif play_again == 0:
                break
            else:
                print("Enter valid input i.e. 1 or 0")
        #decision making based on input
        if play_again == 1:
            continue
        else:
            break
   
   #game ended
    print("Bye-Bye!!")
    print("\n"*5)
