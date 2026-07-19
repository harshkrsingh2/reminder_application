import random

def play():
    user=input("Enter your choice (rock r, paper p, scissors s): ").lower()
    computer=random.choice(['r', 'p', 's'])
    print(f"Computer chose {computer}.")
    if user == computer:
        print("It's a tie!")
    elif (user == 'r' and computer == 's') or (user == 'p' and computer == 'r') or (user == 's' and computer == 'p'):
        print("You win!")
    else:
        print("You lose!")

play()