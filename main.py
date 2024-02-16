import random


def deposit():
    while True:
        deposit_amount = input("\nHow much money would you like to deposit? $")
        if deposit_amount.isdigit():
            deposit_amount = int(deposit_amount)
            if deposit_amount > 0:
                break
            else:
                print("\nDeposit must be greater than 0.")
        else:
            print("\nPlease enter a number.")

    return deposit_amount


def win_lose_logic(player_hand, player_hand_value, dealer_hand_value, bet):
    global account_balance
    global session_balance_change

    if player_hand_value == 21 and len(player_hand) == 2:
        account_balance += bet * 1.5
        session_balance_change += bet * 1.5
        print("\nYou win with a Blackjack! You get 1.5x your bet!")
    elif player_hand_value > 21:
        account_balance -= bet
        session_balance_change -= bet
        print("\nYou Busted!")
    elif dealer_hand_value > 21:
        account_balance += bet
        session_balance_change += bet
        print("\nDealer Busted!")
    elif player_hand_value == dealer_hand_value:
        print("\nIt's a Tie!")
    elif player_hand_value > dealer_hand_value:
        account_balance += bet
        session_balance_change += bet
        print("\nYou Win!")
    else:
        account_balance -= bet
        session_balance_change -= bet
        print("\nYou lost!")

    return account_balance


def hit_stay_logic(player_hand, dealer_hand, deck, bet):
    global deck_of_cards
    global account_balance
    global session_balance_change
    while True:
        decision = input("\nDo you want to Hit or Stay? (h/s): ").lower()

        if decision == 'h':
            new_card = random.choice(list(deck.keys()))
            player_hand.append(new_card)
            del deck[new_card]

            player_hand_value = sum(deck_of_cards[card] for card in player_hand)
            dealer_hand_value = sum(deck_of_cards[card] for card in dealer_hand)

            print('\nYour Hand:', player_hand)
            print('Hand Value:', player_hand_value)

            print('\nDealer\'s Hand:', dealer_hand)
            print('Value:', dealer_hand_value)

            if player_hand_value > 21:
                print("\nYou Busted!")
                account_balance -= bet
                session_balance_change -= bet
                print(f'Balance: ${account_balance}\n+/-: ${session_balance_change}')
                return

        elif decision == 's':
            print("\nYou chose to stay.")
            player_hand_value = sum(deck_of_cards[card] for card in player_hand)
            dealer_hand_value = finish_dealer_hand(player_hand, dealer_hand, deck)
            new_account_balance = win_lose_logic(player_hand, player_hand_value, dealer_hand_value, bet)
            print(f'Balance: ${new_account_balance}\n+/-: ${session_balance_change}')
            break

        else:
            print("Invalid choice. Please enter 'h' to Hit or 's' to Stay.")

    return


def finish_dealer_hand(player_hand, dealer_hand, deck):
    global deck_of_cards
    dealer_hand_value = sum(deck_of_cards[card] for card in dealer_hand)
    player_hand_value = sum(deck_of_cards[card] for card in player_hand)

    while dealer_hand_value < 17:
        new_card = random.choice(list(deck.keys()))
        dealer_hand.append(new_card)
        del deck[new_card]
        dealer_hand_value = sum(deck_of_cards[card] for card in dealer_hand)

    if dealer_hand_value > 21:
        num_aces = dealer_hand.count('Ace')
        while dealer_hand_value > 21 and num_aces > 0:
            dealer_hand_value -= 10
            num_aces -= 1

    print('\nYour Hand:', player_hand)
    print('Value:', player_hand_value)

    print('\nDealer\'s Hand:', dealer_hand)
    print('Value:', dealer_hand_value)

    return dealer_hand_value


def start_blackjack_hand(amount_bet):
    global account_balance
    global deck_of_cards
    global session_balance_change

    # Copy the deck of cards
    copy_deck_of_cards = deck_of_cards.copy()

    # Initialize hands for player and dealer
    player_hand = []
    dealer_hand = []

    # Deal a random card to the player
    player_card_1 = random.choice(list(copy_deck_of_cards.keys()))
    player_hand.append(player_card_1)
    del copy_deck_of_cards[player_card_1]

    # Deal a random card to the dealer
    dealer_card_1 = random.choice(list(copy_deck_of_cards.keys()))
    dealer_hand.append(dealer_card_1)
    del copy_deck_of_cards[dealer_card_1]

    # Deal another random card to the player
    player_card_2 = random.choice(list(copy_deck_of_cards.keys()))
    player_hand.append(player_card_2)
    del copy_deck_of_cards[player_card_2]

    # Display player's hand + value
    print('\nYour Hand:', player_hand)
    player_hand_value = sum(deck_of_cards[card] for card in player_hand)
    print('Value:', player_hand_value)

    # Display dealer's hand (with one card hidden) and hand value
    print('\nDealer\'s Hand:', [dealer_card_1])
    dealer_hand_value = deck_of_cards[dealer_card_1]
    print('Value:', dealer_hand_value)

    # Call hit_stay_logic function with player and dealer hands
    hit_stay_logic(player_hand, dealer_hand, copy_deck_of_cards, amount_bet)

    if account_balance == 0:
        zero_balance = input('\nYour balance is at $0. Want to deposit more money to keep playing?(y or n) ')
        if zero_balance == 'y':
            deposit_amount = deposit()
            account_balance += deposit_amount
            session_balance_change -= deposit_amount

            blackjack()

        if zero_balance == 'n':
            main()

    play_blackjack_again(account_balance)


def play_blackjack_again(balance):
    while True:
        decision = input("\nPlay Again? (y or n) ")

        if decision == 'y':
            amount_bet = set_blackjack_bet(account_balance)
            start_blackjack_hand(amount_bet)

        elif decision == 'n':
            blackjack()

        else:
            print('Invalid Choice.')


def start_slotmachine_spin():
    print('Not Implemented Yet')


def blackjack():
    global account_balance
    global session_balance_change
    bet = 0
    print(f'\nWelcome to the Blackjack Game!')
    while True:
        print(f'\nBalance: ${account_balance}\n+/-: ${session_balance_change}')
        print('\n1. Start Hand')
        print('2. Rules')
        print('3. Switch Game')
        print('4. Exit Casino')

        choice = input("\nWhat would you like to do? ")

        if choice == '1':
            bet = set_blackjack_bet(account_balance)
            start_blackjack_hand(bet)

        elif choice == '2':
            get_blackjack_rules()

        elif choice == '3':
            game_selection()

        elif choice == '4':
            print('\nThank you for playing!')
            quit()

        else:
            print('\nInvalid choice. Please try again.')


def set_blackjack_bet(balance):
    while True:
        bet = input(f'\nHow much do you want to bet? ')
        if bet.isdigit():
            bet = int(bet)
            if 0 < bet <= balance:
                break
            else:
                print("\nPlease enter a valid number.")
        else:
            print("\nPlease enter a valid number.")

    return bet


def get_blackjack_rules():
    print("\nBlackjack Rules:")
    print("1. The goal is to beat the dealer's hand without going over 21.")
    print("2. Face cards are worth 10. Aces are worth 1 or 11, whichever makes a better hand.")
    print("3. Each player starts with two cards, one of the dealer's cards is hidden until the end.")
    print("4. To 'Hit' is to ask for another card. To 'Stand' is to hold your total and end your turn.")
    print("5. If you go over 21, you bust and the dealer wins regardless of the dealer's hand.")
    print("6. If you are dealt 21 from the start (Ace & 10), you got a Blackjack.")
    print("7. Blackjack usually pays out 3:2, meaning you win 1.5 times your bet.")
    print("8. Insurance, if the dealer's face-up card is an ace, you can take insurance.")
    print("   Insurance is a side bet at 2:1 of your original bet and protects you if the dealer has a Blackjack. \n")


def get_slotmachine_rules():
    pass


def slot_machine():
    global account_balance
    print("\nWelcome to the Slot Machines!")
    while True:
        print(f'\nBalance: ${account_balance}')
        print('\n1. Spin')
        print('2. Set Bets')
        print('3. Rules')
        print('4. Switch Game')
        print('5. Exit Casino')

        choice = input("\nWhat would you like to do? ")

        if choice == '1':
            start_slotmachine_spin()

        elif choice == '2':
            print('Not Implemented yet')

        elif choice == '3':
            get_slotmachine_rules()

        elif choice == '4':
            game_selection()

        elif choice == '5':
            print('\nThank you for playing!')
            quit()

        else:
            print('\nInvalid choice.')


def game_selection():
    global account_balance
    global session_balance_change
    while True:
        print(f'\nBalance: ${account_balance}\n+/-: ${session_balance_change}')
        print('\n1. BlackJack')
        print('2. Slot Machine')
        print('3. Exit Game Selection')
        print('4. Exit Casino')

        choice = input('\nWhat would you like to do? ')

        if choice == '1':
            blackjack()

        elif choice == '2':
            slot_machine()

        elif choice == '3':
            main()

        elif choice == '4':
            print('\nThank you for playing!')
            quit()

        else:
            print('\nInvalid choice. Please try again.')


def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = {}

    for suit in suits:
        for rank in ranks:
            card_name = f"{rank} of {suit}"
            if rank in ['Jack', 'Queen', 'King']:
                value = 10
            elif rank == 'Ace':
                value = 11
            else:
                value = int(rank)
            deck[card_name] = value
    return deck


def main():
    global account_balance
    global session_balance_change
    print('\nWelcome to my Python Casino!\nCreated by Charles-Olivier Ipperciel.')
    while True:
        print(f'\nBalance: ${account_balance}\n+/-: ${session_balance_change}')
        print('\n1. Deposit Money')
        print('2. Choose a Game')
        print('3. Exit Casino')

        choice = input('\nWhat would you like to do? ')

        if choice == '1':
            deposit_amount = deposit()
            account_balance += deposit_amount
            session_balance_change -= deposit_amount

        elif choice == '2':
            if account_balance == 0:
                print('\nYou don\'t have enough in your account.')
            else:
                game_selection()

        elif choice == '3':
            print('\nThank you for playing!')
            break

        else:
            print('\nInvalid choice. Please try again.')


if __name__ == "__main__":
    account_balance = 0
    session_balance_change = 0
    deck_of_cards = create_deck()
    main()
