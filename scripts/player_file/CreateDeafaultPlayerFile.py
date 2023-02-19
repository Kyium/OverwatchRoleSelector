
PLAYER_FILE_DIR = "../../player_files/"

DEFAULT_NAMES = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]


def create_default_player_file():
    with open(PLAYER_FILE_DIR + "default.plr", "w") as f:
        for name in DEFAULT_NAMES:
            f.write(name + "\n")
