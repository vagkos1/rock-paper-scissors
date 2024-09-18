### Description

The rock-paper-scissors project is a Python implementation of the classic game, structured using Domain-Driven Design (DDD) principles. It encapsulates the core game logic, player management and game sessions within a modular architecture. The project aims to be scalable and maintainable with potential for future enhancements like multiplayer support and leaderboards.

### Domain-Driven Design and Onion Architecture

I chose Domain-Driven Design (DDD) and Onion Architecture to ensure a clean separation of concerns and high modularity.  
By structuring the application into distinct layers (domain, application, infrastructure), I encapsulate the core business logic in the domain layer, while the outer layers handle technical concerns like data access and user interfaces.  
This approach promotes maintainability, testability, and scalability, making the system more adaptable to future changes.
Even though this flexibility is not necessary for this take-home test, I wanted to showcase how I normally approach designing software.

1. Clone the repository:
    ```sh
    git clone https://github.com/vagkos1/rock-paper-scissors.git
    cd rock-paper-scissors
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

Run the app:
```
python -m src.main
```

Run the tests:
```
pytest
```

I didn't give the option to the user to save because the game automatically saves after every move.

