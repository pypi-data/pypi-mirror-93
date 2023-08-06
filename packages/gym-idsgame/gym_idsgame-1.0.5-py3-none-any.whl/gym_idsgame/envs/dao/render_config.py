"""
Render-configuration for the gym-idsgame environment
"""

# In case running on server without screen
try:
    import pyglet
except:
    pass
from gym_idsgame.envs.constants import constants

class RenderConfig:
    """
    DTO with configuration parameters for the UI rendering
    """
    def __init__(self, resources_dir: str = constants.RENDERING.RESOURCES_DIR,
                 blink_interval: float = constants.RENDERING.AGENT_BLINK_INTERVAL,
                 num_blinks: int = constants.RENDERING.AGENT_NUM_BLINKS, title="IdsGame",
                 attacker_view : bool = False, defender_view : bool = False):
        """
        Constructor, initializes the DTO

        :param resources_dir: directory with resources for rendering
        :param blink_interval: the interval for blinking when simulating attack/defense operations
        :param num_blinks: the number of blinks when simulating attack/defense operations
        :param attacker_view: boolean flag whether to show the attacker's view (otherwise fully observed view is shown)
        :param defender_view: boolean flag whether to show the defender's view (otherwise fully observed view is shown)
        """
        self.rect_size = constants.RENDERING.RECT_SIZE
        self.bg_color = constants.RENDERING.WHITE
        self.border_color = constants.RENDERING.BLACK
        self.attacker_filename = constants.RENDERING.HACKER_AVATAR_FILENAME
        self.server_filename = constants.RENDERING.SERVER_AVATAR_FILENAME
        self.data_filename = constants.RENDERING.DATA_AVATAR_FILENAME
        self.cage_filename = constants.RENDERING.CAGE_AVATAR_FILENAME
        self.glass_filename = constants.RENDERING.GLASS_AVATAR_FILENAME
        self.minimum_width = constants.RENDERING.MIN_WIDTH
        self.attacker_scale = constants.RENDERING.ATTACKER_AVATAR_SCALE
        self.server_scale = constants.RENDERING.SERVER_AVATAR_SCALE
        self.data_scale = constants.RENDERING.DATA_AVATAR_SCALE
        self.cage_scale = constants.RENDERING.CAGE_AVATAR_SCALE
        self.line_width = constants.RENDERING.LINE_WIDTH
        self.caption = constants.RENDERING.CAPTION
        self.resources_dir = resources_dir
        self.blink_interval = blink_interval
        self.num_blinks = num_blinks
        self.new_window()
        self.height = constants.RENDERING.DEFAULT_HEIGHT
        self.width = constants.RENDERING.MIN_WIDTH
        self.title=title
        self.attacker_view = attacker_view
        self.defender_view = defender_view


    def new_window(self):
        # in case on a server without pyglet
        try:
            self.batch = pyglet.graphics.Batch()
            self.background = pyglet.graphics.OrderedGroup(0)
            self.first_foreground = pyglet.graphics.OrderedGroup(1)
            self.second_foreground = pyglet.graphics.OrderedGroup(2)
        except:
            pass


    def manual_default(self) -> None:
        """
        default settings for manual rendering
        :return:  None
        """
        self.num_blinks = constants.RENDERING.MANUAL_NUM_BLINKS
        self.blink_interval = constants.RENDERING.MANUAL_BLINK_INTERVAL


    def set_height(self, num_rows: int) -> None:
        """
        Sets the height for the main gameframe

        :param num_rows: number of rows in the network
        :return: None
        """
        self.height = constants.RENDERING.PANEL_HEIGHT + int((self.rect_size / 1.5)) * num_rows


    def set_width(self, num_cols: int) -> None:
        """
        Sets the width for the main gameframe

        :param num_cols: the number of columns in the network
        :return: None
        """
        self.width = max(self.minimum_width, self.rect_size * num_cols)
