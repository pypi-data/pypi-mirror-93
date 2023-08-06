"""
Constants for the gym-idsgame environment
"""

class RENDERING:
    """
    Rendering constants
    """
    RECT_SIZE = 200
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    RED_ALPHA = (255, 0, 0, 255)
    GREEN = (0, 128, 0)
    GREEN_ALPHA = (0, 128, 0, 255)
    LIME = (0, 255, 0)
    BLACK_ALPHA = (0, 0, 0, 255)
    WHITE_ALPHA = (255, 255, 255, 255)
    RED_ALPHA = (128, 0, 0, 255)
    WHITE = (255, 255, 255)
    GREY = (220, 220, 220)
    RESOURCES_DIR = "resources"
    HACKER_AVATAR_FILENAME = "hacker.png"
    SERVER_AVATAR_FILENAME = "ibm_tower.png"
    DATA_AVATAR_FILENAME = "data.png"
    CAGE_AVATAR_FILENAME = "cage.png"
    GLASS_AVATAR_FILENAME = "glass1.png"
    ATTACKER_AVATAR_SCALE = 0.3
    SERVER_AVATAR_SCALE = 0.2
    DATA_AVATAR_SCALE = 0.2
    CAGE_AVATAR_SCALE = 0.05
    PANEL_HEIGHT = 75
    PANEL_LEFT_MARGIN = 60
    PANEL_TOP_MARGIN = 30
    PANEL_FONT_SIZE = 12
    NODE_STATE_FONT_SIZE = 10
    LINE_WIDTH = 2
    MANUAL_NUM_BLINKS = 14
    MANUAL_BLINK_INTERVAL = 0.3
    AGENT_NUM_BLINKS = 10
    AGENT_BLINK_INTERVAL = 0.05
    CAPTION = "IDS Game"
    MIN_WIDTH = 600
    DEFAULT_HEIGHT = 800

class GAME_CONFIG:
    """
    Game constants
    """
    POSITIVE_REWARD = 1
    NEGATIVE_REWARD = -1
    MAX_GAME_STEPS = 100
    INITIAL_RECONNAISSANCE_STATE = 10
