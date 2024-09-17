from .application.services.game_service import GameService
from .domain.value_objects.move import Move
from .infrastructure.repositories.in_memory_game_repository import InMemoryGameRepository
from .domain.entities.game import GameStatus

def main():
    game_repository = InMemoryGameRepository()
    game_service = GameService(game_repository)

    print("Welcome to Rock-Paper-Scissors Game!")
    player1_name = input("Enter name for Player 1: ")

    vs_computer = input("Play against computer? (y/n): ").lower() == 'y'
    if vs_computer:
        player2_name = "Computer"
    else:
        player2_name = input("Enter name for Player 2: ")

    game = game_service.start_game(player1_name, player2_name, vs_computer)

    while True:
        # Iterate through both players to collect their moves
        for player in [game.player1, game.player2]:
            # Skip input for computer player
            if player.is_computer:
                continue

            # Prompt the current player for their move
            print(f"\n{player.name}'s turn (other player, please close your eyes):")
            player_move = get_valid_move()
            
            # Update the game state with the player's move
            game = game_service.make_move(game.id, player.id, player_move)
            print(f"{player.name} has made their choice.")
            
            # Pause to allow the current player to hide their move
            input("Press Enter to continue...")

        # After both players have made their moves, reveal the choices
        print("\n" + "=" * 40)

        print_round_result(game)
        print_current_scores(game)

        print("=" * 40)

        # Check if the game has reached its end condition
        if game.status != GameStatus.ONGOING:
            break  # End the game loop if the game is no longer ongoing

        # Ask players if they want to continue playing
        play_again = input("\nDo you want to play another round? (y/n): ").lower()
        if play_again != 'y':
            break  # End the game if players choose not to continue

def get_valid_move() -> Move:
    while True:
        print("Choose your move:")
        for i, move in enumerate(Move):
            print(f"{i + 1}. {move.value}")
        try:
            move_choice = int(input("Enter the number of your move: ")) - 1
            if 0 <= move_choice < len(Move):
                return list(Move)[move_choice]
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def print_round_result(game):
    print("\n" + "=" * 40)
    print("🏆 ROUND RESULT 🏆".center(40))
    print("-" * 40)
    
    # Retrieve and display each player's move
    move1 = game.last_round_moves[game.player1.id]
    move2 = game.last_round_moves[game.player2.id]
    print(f"{game.player1.name} chose {move1.value}")
    print(f"{game.player2.name} chose {move2.value}")
    print("-" * 40)

    # Determine and announce the winner of the round
    if game.last_round_winner is None:
        print("  🤝 It's a tie! 🤝".center(38))
    else:
        # Identify the winner's name based on the winning player ID
        winner_name = game.player1.name if game.last_round_winner == game.player1.id else game.player2.name
        print(f"  🎉 {winner_name} wins the round! 🎉".center(38))

def print_current_scores(game):
    print("-" * 40)
    print("📊 CURRENT SCORES 📊".center(40))
    print("-" * 40)

    max_name_length = max(len(game.player1.name), len(game.player2.name))

    for pid, score in game.scores.items():
        # Match the player ID to the correct player name
        pname = game.player1.name if game.player1.id == pid else game.player2.name
        print(f"  {pname:<{max_name_length}} : {score:>2}")

if __name__ == "__main__":
    main()
