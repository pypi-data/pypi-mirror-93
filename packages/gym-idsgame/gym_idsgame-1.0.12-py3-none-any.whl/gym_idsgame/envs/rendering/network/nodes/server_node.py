"""
Represents a server node in the network of the gym-idsgame environment
"""
from typing import Union
import pyglet
from pyglet import clock
from gym_idsgame.envs.constants import constants
from gym_idsgame.envs.rendering.network.nodes.resource_node import ResourceNode
from gym_idsgame.envs.dao.idsgame_config import IdsGameConfig
from gym_idsgame.envs.dao.node_type import NodeType

class ServerNode(ResourceNode):
    """
    Represents a server node in the grid network
    """
    def __init__(self, idsgame_config: IdsGameConfig, row: int, col: int, id: int):
        """
        Initializes the node

        :param idsgame_config: configuration for the IdsGameEnv
        :param row: the row in the grid
        :param col: the column in the grid
        :param id: the id of the node
        """
        avatar = pyglet.resource.image(idsgame_config.render_config.server_filename)
        super(ServerNode, self).__init__(avatar, idsgame_config,
                                         idsgame_config.render_config.background)
        self.col = col
        self.row = row
        self._id = id
        self.scale = idsgame_config.render_config.server_scale
        self.reset()

    @property
    def node_type(self) -> NodeType:
        """
        :return: the type of the node (SERVER)
        """
        return NodeType.SERVER

    @property
    def id(self) -> int:
        """
        :return: the id of the node
        """
        return self._id

    def init_labels(self) -> None:
        """
        Initializes the labels of the node

        :return: None
        """
        attack_label_x = self.x + self.idsgame_config.render_config.rect_size / 14
        attack_label_y = self.row * int((self.idsgame_config.render_config.rect_size) / 1.5) + \
                         self.idsgame_config.render_config.rect_size / 4
        defense_label_x = self.x + self.idsgame_config.render_config.rect_size / 14
        defense_label_y = self.row * int((self.idsgame_config.render_config.rect_size) / 1.5) + \
                          self.idsgame_config.render_config.rect_size / 7
        det_label_x = self.x - self.idsgame_config.render_config.rect_size / 12
        det_label_y = self.row * int((self.idsgame_config.render_config.rect_size) / 1.5) + \
                      self.idsgame_config.render_config.rect_size / 3
        self.create_labels(attack_label_x=attack_label_x, attack_label_y=attack_label_y,
                           defense_label_x=defense_label_x, defense_label_y=defense_label_y,
                           det_label_x=det_label_x, det_label_y=det_label_y)

    def visualize_attack(self, attack_type:int, attacker_pos: Union[int, int], edges_list:list=None) -> None:
        """
        Simulates an attack against the node.

        :param attack_type: the type of the attack
        :param attacker_pos: the current position of the attacker
        :param edges_list: edges list for visualization (blinking)
        :return: None
        """
        for i in range(0, self.idsgame_config.render_config.num_blinks):
            if i % 2 == 0:
                clock.schedule_once(self.blink_red_attack, self.idsgame_config.render_config.blink_interval * i,
                                    attacker_pos)
            else:
                clock.schedule_once(self.blink_black_attack, self.idsgame_config.render_config.blink_interval * i,
                                    attacker_pos)

    def blink_red_attack(self, dt, attacker_pos: Union[int, int], edges_list: list = None) -> None:
        """
        Makes the node and its links blink red to visualize an attack

        :param dt: the time since the last scheduled blink
        :param attacker_pos: the attackers position
        :param edges_list: list of edges to blink
        :return: None
        """
        color = constants.RENDERING.RED
        color_list = list(color) + list(color)
        attacker_row, attacker_col = attacker_pos
        if attacker_row > self.row:
            for edge in self.incoming_edges:
                edge.colors = color_list
        elif attacker_row < self.row:
            for edge in self.outgoing_edges:
                edge.colors = color_list
        else:
            #assert len(self.horizontal_edges) > 0
            if len(self.horizontal_edges) > 0:
                if attacker_col < self.col:
                    self.horizontal_edges[0].colors = color_list
                else:
                    if len(self.horizontal_edges) > 1:
                        self.horizontal_edges[1].colors = color_list
                    else:
                        self.horizontal_edges[0].colors = color_list

        lbl_color = constants.RENDERING.RED_ALPHA
        self.attack_label.color = lbl_color
        self.color = constants.RENDERING.RED


    def blink_black_attack(self, dt, attacker_pos: Union[int, int], edges_list: list = None) -> None:
        """
        Makes the node and its links blink black to visualize an attack

        :param dt: the time since the last scheduled blink
        :param attacker_pos: the attackers position
        :param edges_list: list of edges to blink
        :return: None
        """
        color = constants.RENDERING.BLACK
        color_list = list(color) + list(color)
        attacker_row, attacker_col = attacker_pos
        if attacker_row > self.row:
            for edge in self.incoming_edges:
                edge.colors = color_list
        elif attacker_row < self.row:
            for edge in self.outgoing_edges:
                edge.colors = color_list
        else:
            #assert len(self.horizontal_edges) > 0
            if len(self.horizontal_edges) > 0:
                if attacker_col < self.col:
                    self.horizontal_edges[0].colors = color_list
                else:
                    if len(self.horizontal_edges) > 1:
                        self.horizontal_edges[1].colors = color_list
                    else:
                        self.horizontal_edges[0].colors = color_list
        lbl_color = constants.RENDERING.BLACK_ALPHA
        self.attack_label.color = lbl_color
        self.color = constants.RENDERING.WHITE

    def center_avatar(self) -> None:
        """
        Utiltiy function for centering the avatar inside a cell

        :return: The centered coordinates in the grid
        """
        if self.col < (self.idsgame_config.game_config.network_config.num_cols//2):
            self.x = self.idsgame_config.render_config.width // 2 - \
                     (self.idsgame_config.game_config.network_config.num_cols//2 - (self.col)) * \
                     self.idsgame_config.render_config.rect_size
        elif self.col > (self.idsgame_config.game_config.network_config.num_cols//2):
            self.x = self.idsgame_config.render_config.width // 2 + \
                     (self.col - (self.idsgame_config.game_config.network_config.num_cols//2)) * \
                     self.idsgame_config.render_config.rect_size
        else:
            self.x = self.idsgame_config.render_config.width // 2

        self.y = int((self.idsgame_config.render_config.rect_size/1.5))*self.row + \
                 self.idsgame_config.render_config.rect_size/3.5

    def get_link_coords(self, upper: bool= True, lower: bool= False) -> Union[float, float, int, int]:
        """
        Gets the coordinates of link endpoints of the node

        :param upper: if True, returns the upper endpoint
        :param lower: if False, returns the lower endpoint
        :return: (x-coordinate, y-coordinate, grid-column, grid-row)
        """
        if upper:
            x = self.x + self.idsgame_config.render_config.rect_size / 14
            y = (self.row+1)*(self.idsgame_config.render_config.rect_size/1.5) - \
                self.idsgame_config.render_config.rect_size/6
        elif lower:
            x = self.x + self.idsgame_config.render_config.rect_size / 14
            y = (self.row + 1) * (self.idsgame_config.render_config.rect_size / 1.5) - \
                self.idsgame_config.render_config.rect_size / 1.75
        return x, y, self.col, self.row