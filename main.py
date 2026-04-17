import pygame
from game import Game


def main():

    # initialize audio first (reduces sound latency)
    pygame.mixer.pre_init(44100, -16, 2, 512)

    # initialize pygame
    pygame.init()

    # ===== MULTIPLAYER CONFIGURATION =====
    # Set enable_multiplayer=True to connect to server
    # Set enable_multiplayer=False for single-player mode
    ENABLE_MULTIPLAYER = True
    SERVER_HOST = 'localhost'
    SERVER_PORT = 5001
    
    # create game
    game = Game(
        enable_multiplayer=ENABLE_MULTIPLAYER,
        server_host=SERVER_HOST,
        server_port=SERVER_PORT
    )

    # load assets
    game.load_assets()

    try:
        # start game loop
        game.play()
    finally:
        # Cleanup network on exit
        game.disconnect_network()


if __name__ == "__main__":
    main()