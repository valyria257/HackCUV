#Poker logic
from enum import Enum
import random

class Suits(Enum):
    Hearts = 0
    Diamond = 1
    Clubs = 2
    Spades = 3

class Faces(Enum):
    Ace_Low = -1
    Two = 0
    Three = 1
    Four = 2
    Five = 3
    Six = 4
    Seven = 5
    Eight = 6
    Nine = 7
    Ten = 8
    Jack = 9
    Queen = 10
    King = 11
    Ace = 12

class Actions(Enum):
    Check = 0
    Raise = 1
    Call = 2
    Fold = 3

class Hands(Enum):
    HighCard = 0
    Pair = 1
    DoublePair = 2
    ThreeKind = 3
    Straight = 4
    Flush = 5
    FullHouse = 6
    FourKind = 7
    StraightFlush = 8

class Card:
    def __init__(self, i):
        if i < 13:
            self.suit = Suits(0)
        elif i < 26:
            self.suit = Suits(1)
        elif i < 39:
            self.suit = Suits(2)
        elif i < 52:
            self.suit = Suits(3)

        i = i % 13
        self.face = Faces(i)

    def prettyPrint(self):
        print(self.suit,self.face)

class Player:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name
        self.chips = 0
        self.inround = True
        self.cards = []

    def askAction(self, Game):
        i = random.randint(0,3)
        act = (Actions(i), 300)
        print(self.name," choose action: ", Actions(i))
        return act


class pokerGame():
    def __init__(self):
        self.h_all = [
            self.h_StraightFlush,
            self.h_FourKind,
            self.h_FullHouse,
            self.h_Flush,
            self.h_Straight,
            self.h_ThreeKind,
            self.h_DoublePair,
            self.h_Pair,
            self.h_HighCard
        ]
        self.usedCards = []
        self.players = [
            Player("uid1", "Alex"),
            Player("uid2", "Buddy"),
            Player("uid3", "Connel"),
            Player("uid4", "Davy Jones"),
            Player("uid5", "Elton"),
            Player("uid8", "Fred")
        ]
        self.startingValues = 1000
        self.bigBlindValue = int(self.startingValues * 0.02)
        self.lilBlindValue = int(self.startingValues * 0.01)
        self.dealer = 0;
        self.pot = 0;
        self.tableCards = [];
        self.playersCnt = len(self.players)
        for p in self.players:
            self.giveMoney(p, self.startingValues)


    def printScoreBoard(self):
        for p in self.players:
            print(p.name, ":", p.chips)

    def newCard(self):
        i = random.randint(0,51)
        if i in self.usedCards:
            if len(self.usedCards <= 52):
                return newCard()
            else:
                return -1
        return Card(i)

    def giveMoney(self, plyr, amount):
        plyr.chips += amount

    def addPot(self, plyr, amount):
        self.pot += amount
        self.giveMoney(plyr, -amount)

    def moreThanOne(self):
        inCnt = 0
        for p in self.players:
            if p.inround:
                inCnt += 1
        return (inCnt > 1)

    def dealPlayers(self):
        for p in self.players:
            p.cards = [self.newCard(), self.newCard()]
            p.inround = True

    def roundOfBetting(self, rndNum):
        bets = [0] * self.playersCnt
        betValue = 0
        #Calculates positions of which player has what role per round
        if rndNum == 0:
            self.dealer = (self.dealer + 1) % len(self.players)
            lilBlind = self.dealer - 1
            bigBlind = self.dealer - 2
            if lilBlind < 0:
                lilBlind = self.playersCnt - 1
                bigBlind = self.playersCnt - 2
            elif bigBlind < 0:
                bigBlind = self.playersCnt - 1
            self.addPot(self.players[bigBlind], self.bigBlindValue)
            bets[bigBlind] += self.bigBlindValue
            self.addPot(self.players[lilBlind], self.lilBlindValue)
            bets[lilBlind] += self.lilBlindValue
            self.folders = 0

        betValue = self.bigBlindValue


        curP = self.dealer
        asksRemaining = self.playersCnt
        while asksRemaining > 0:
            curPlayer = self.players[curP]
            if curPlayer.inround == False:
                asksRemaining -= 1
                curP = (curP + 1) % self.playersCnt
                continue

            (action, amount) = self.askAction(curPlayer)

            if action is Actions.Raise:
                difference = betValue - bets[curP] + amount
                if difference <= curPlayer.chips:
                    bets[curP] += difference
                    betValue += amount
                    self.addPot(curPlayer, difference)
                    asksRemaining = self.playersCnt
                else:
                    continue

            elif action is Actions.Call:
                callAmount = betValue  - bets[curP]
                if callAmount == 0:
                    continue
                if callAmount > curPlayer.chips:
                    callAmount = curPlayer.chips
                self.addPot(curPlayer, callAmount)
                bets[curP] += callAmount

            elif action is Actions.Check:
                if bets[curP] != betValue:
                    continue

            else: #only other action is a fold
                if self.folders < self.playersCnt - 1:
                    curPlayer.inround = False
                    self.folders += 1
                else:
                    continue

            asksRemaining -= 1
            curP = (curP + 1) % self.playersCnt
            #print("betvalue is at:", betValue)
            print("Heres what everyone has bet:")
            i = 0
            for p in self.players:
                print(p.name, ":",bets[i])
                i += 1
            #print("Heres what everyone has bet:", bets)
            print("The Pot is now at: ", self.pot, "dollars")

    def sortHand(self, hand):
        hand.sort(key=lambda x: x.face.value, reverse=True)
        return hand

    def calcWinner(self):
        highScore = -1
        winner = -1
        for p in self.players:
            if p.inround:
                scr = self.calculateScore(p.cards)
                print(p.name, scr)
                if scr > highScore:
                    highScore = scr
                    winner = p
        return winner

    def removeLosers(self):
        i = 0
        while i < self.playersCnt:
            if(self.players[i].chips <= 0):
                del self.players[i]
                self.playersCnt -= 1
            else:
                i+=1

    def calculateScore(self, userCards):
        hand = userCards + self.tableCards.copy()
        score = 9
        for h in self.h_all:
            (has, used, remaining) = h(hand.copy())
            if has:
                tieBreakCards = used

                diff = 5 - len(used)
                if diff > 0:
                    tieBreakCards += self.sortHand(remaining)[0:diff]

                tieBreakCards = self.sortHand(tieBreakCards)
                mult = 0.01
                for c in tieBreakCards:
                    score += c.face.value * mult
                    mult *= 0.01

                return score

            score -= 1

        return -1


    def h_HighCard(self, hand):
        return (True, hand, [])

    def h_Pair(self, hand):
        for ind1, card1 in enumerate(hand):
            for ind2, card2 in enumerate(hand):
                if ind1 != ind2 and card1.face == card2.face:
                    del hand[ind2]
                    del hand[ind1]
                    return (True, [card1, card2], hand)
        return (False, [], hand)

    def h_DoublePair(self, hand):
        (firstPair, firstUsed, firstRemaining) = self.h_Pair(hand)
        if firstPair:
            (secondPair, secondUsed, secondRemaining) = self.h_Pair(firstRemaining)
            if secondPair:
                return (True, firstUsed + secondUsed, secondRemaining)
        return (False, [], hand)

    def h_ThreeKind(self, hand):
        for ind1, card1 in enumerate(hand):
            for ind2, card2 in enumerate(hand):
                for ind3, card3 in enumerate(hand):
                    if ind1 != ind2 and ind2 != ind3 and ind3 != ind1 and card1.face == card2.face and card2.face == card3.face:
                        del hand[ind3]
                        del hand[ind2]
                        del hand[ind1]
                        return (True, [card1, card2, card3], hand)
        return (False, [], hand)

    def h_Straight(self, hand):
        usedCards = []
        cardsInRow = 0

        for ind1, card1 in enumerate(hand):
            if cardsInRow >= 4:
                usedCards.append(ind1)
                break

            nextInd = ind1 + 1
            if nextInd < len(hand):
                diff = card1.face.value - hand[nextInd].face.value
                if diff == 1:
                    cardsInRow += 1
                    usedCards.append(ind1)
                elif diff != 0:
                    usedCards = []
                    cardsInRow = 0
                    startInd = nextInd


        if cardsInRow >= 4:
            resultHand = []
            usedCards.reverse()

            for ind in usedCards:
                resultHand.append(hand[ind])
                del hand[ind]
            return(True, resultHand, hand)

        return (False, [], hand)

    def h_Flush(self, hand):
        counts = [0] * 4
        for card in hand:
            counts[card.suit.value] += 1

        for indSuit, c in enumerate(counts):
            if c >= 5:
                resultHand = []
                for indCard, card in enumerate(hand):
                    if card.suit.value == indSuit:
                        resultHand.append(card)
                        del hand[indCard]
                return (True, resultHand, hand)


        return (False, [], hand)

    def h_FullHouse(self, hand):
        (firstPair, firstUsed, firstRemaining) = self.h_ThreeKind(hand)
        if firstPair:
            (secondPair, secondUsed, secondRemaining) = self.h_Pair(firstRemaining)
            if secondPair:
                return (True, firstUsed + secondUsed, secondRemaining)
        return (False, [], hand)

    def h_FourKind(self, hand):
        (firstPair, firstUsed, firstRemaining) = self.h_Pair(hand)
        if firstPair:
            (secondPair, secondUsed, secondRemaining) = self.h_Pair(firstRemaining)
            if secondPair and firstUsed[0].face == secondUsed[1].face:
                return (True, firstUsed + secondUsed, secondRemaining)
        return (False, [], hand)

    def h_StraightFlush(self, hand):
        (hasStraight, straightCards, remaining) = self.h_Straight(hand)
        if hasStraight:
            (hasFlush, flushCards, remaining) = self.h_Flush(straightCards)
            if hasFlush:
                return (True, straightCards, remaining)
        return (False, [], hand)








    def round(self):
        print("-----------------Round Begin-----------------")
        self.dealPlayers()
        self.roundOfBetting(0)
        if self.moreThanOne():
            self.tableCards = [self.newCard(), self.newCard(), self.newCard()]
            self.roundOfBetting(1)
            if self.moreThanOne():
                self.tableCards.append(self.newCard())
                self.roundOfBetting(2)
                if self.moreThanOne():
                    self.tableCards.append(self.newCard())
                    self.roundOfBetting(3
                    )

        winner = self.calcWinner()
        self.giveMoney(winner,self.pot)
        self.pot = 0

        print("=======================Cards=======================")
        print("Table:")
        for c in self.tableCards:
            c.prettyPrint()
        print("Players:")
        for u in self.players:
            print(u.name)
            u.cards[0].prettyPrint()
            u.cards[1].prettyPrint()
        print("===================Cards End=======================")
        self.removeLosers()

        print("round winner:",winner.name)
        self.printScoreBoard()
        print("-----------------Round End-----------------")





    def askAction(self, plyr):
        return plyr.askAction(self)









def prettyPrintScore(has, used, remaining):
    print(has)
    print("used:")
    for u in used:
        print(u.face,":",u.suit)
    print("remaining:")
    for r in remaining:
        print(r.face,":",r.suit)





if __name__ == "__main__":
    Game = pokerGame()

    while Game.playersCnt > 1:
        Game.round()