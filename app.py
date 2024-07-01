import math
from flask import Flask, render_template, redirect, url_for
from poker import PokerGame
from openai_api import preflop_ai_feedback

app = Flask(__name__)
app.secret_key = 'nithilan_poker_app'  

@app.route('/')
def index():
    poker_game = PokerGame()
    # Deal hands
    numplayers = 4
    hands = poker_game.deal_hand(numplayers)  # Deal 2 cards to 4 players

    hands_info = []
    preflop_messages = []
    for hand in hands:
        this_hand = []
        for card in hand:
            this_hand.append((card.suit, card.rank))
        hands_info.append(this_hand)


        preflop_message = poker_game.pre_flop_message(hand[0], hand[1])
        preflop_messages.append(preflop_message)

    # Deal community cards
    community_cards = poker_game.deal_community_card()

    community_info = []
    for card in community_cards:
        rank = card.rank
        suit = card.suit
        community_info.append({'rank': rank, 'suit': suit})

    flop = community_info[:3]
    turn = community_info[3]
    river = community_info[4]
    
    hand_evaluations = []
    score_num = []
    for hand in hands:
        score = poker_game.evaluate_hand(hand,community_cards)
        score_num.append(score)

        evaluation = poker_game.evaluate_hand_str(hand,community_cards)
        hand_evaluations.append(evaluation)
    
    opponent_score = max(score_num[1:])
    my_score = score_num[0]

    result_str = ""
    fold_str = ""
    won_round = False
    if(my_score == opponent_score):
        result_str = "You ended up drawing with CPU. In this case, we'd split the pot."
        fold_str = "You would have drew here! Safe fold, not a big loss at all!"
        won_round = True
    elif(math.floor(my_score/10) == math.floor(opponent_score/10)):
        if(my_score > opponent_score):
            won_round = True
            result_str = "Phew! CPU also had that hand, but you won off of strength of cards!"
            fold_str = "You had the best hand on the board. Be wiser with your folds."
        if(my_score < opponent_score):
            result_str = "CPU had the same hand, but beat you off of strength of cards."
            fold_str = "Great fold! Though your hand was good, you recognized that better hands were possible!"
    else:
        if(my_score > opponent_score):
            won_round = True
            result_str = "You won the pot! Good job recognizing the strength of your hand!"
            fold_str = "You had the best hand on the board. Be wiser with your folds."
        if(my_score < opponent_score):
            if(math.floor(my_score/10) == 1):
                result_str = "CPU Won. Remember, betting with high card is difficult to win."
                fold_str = "Nice fold! Good job recognizing that you had low odds of winning this round."
            else: 
                result_str = "CPU Won. You'll get em next time!"
                fold_str = "Good fold! You recognized that others could have better cards."
    ai_analysis = ""
    ai_analysis = preflop_ai_feedback(hands_info[0][0], hands_info[0][1]) # A call for the AI Feedback.
    return render_template("frontend.html", 
                           ai_analysis=ai_analysis,
                           numplayers = numplayers,
                           score=score,
                           hands_info=hands_info, 
                           community_info=community_info,
                           flop=flop,
                           turn=turn,
                           river=river, 
                           preflop_messages=preflop_messages, 
                           hand_evaluations=hand_evaluations,
                           won_round=won_round,
                           result_str=result_str,
                           fold_str=fold_str)

@app.route('/restart')
def restart():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
