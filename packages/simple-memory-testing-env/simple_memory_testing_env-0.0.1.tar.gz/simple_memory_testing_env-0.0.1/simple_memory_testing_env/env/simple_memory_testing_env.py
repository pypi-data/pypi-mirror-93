import gym_minigrid
from gym_minigrid.minigrid import *
from gym_minigrid.wrappers import *

from gym import spaces 
import copy
import numpy as np

# Map of color names to RGB values
COLORS = {
    'red'   : np.array([255, 0, 0]),
    'green' : np.array([0, 255, 0]),
    'blue'  : np.array([0, 0, 255]),
    'purple': np.array([112, 39, 195]),
    'yellow': np.array([255, 255, 0]),
    'grey'  : np.array([100, 100, 100]),
    'white' : np.array([255, 255, 255]),
}
gym_minigrid.minigrid.COLORS = COLORS

COLOR_NAMES = sorted(list(COLORS.keys()))
gym_minigrid.minigrid.COLOR_NAMES = COLOR_NAMES

# Used to map colors to integers
COLOR_TO_IDX = {
    'red'   : 0,
    'green' : 1,
    'blue'  : 2,
    'purple': 3,
    'yellow': 4,
    'grey'  : 5,
    'white' : 6,
}
gym_minigrid.minigrid.COLOR_TO_IDX = COLOR_TO_IDX

IDX_TO_COLOR = dict(zip(COLOR_TO_IDX.values(), COLOR_TO_IDX.keys()))
gym_minigrid.minigrid.IDX_TO_COLOR = IDX_TO_COLOR

# Map of object type to integers
OBJECT_TO_IDX = {
    'unseen'        : 0,
    'empty'         : 1,
    'wall'          : 2,
    'floor'         : 3,
    'door'          : 4,
    'key'           : 5,
    'ball'          : 6,
    'box'           : 7,
    'goal'          : 8,
    'lava'          : 9,
    'agent'         : 10,

    'red_goal'      : 15,
    'yellow_goal'   : 16,
    'blue_goal'     : 18,
    'green_goal'    : 19,

}
gym_minigrid.minigrid.OBJECT_TO_IDX = OBJECT_TO_IDX

IDX_TO_OBJECT = dict(zip(OBJECT_TO_IDX.values(), OBJECT_TO_IDX.keys()))
gym_minigrid.minigrid.IDX_TO_OBJECT = IDX_TO_OBJECT



class CustomGoal(WorldObj):
    def can_overlap(self):
        return True

    def render(self, img):
        fill_coords(img, point_in_rect(0, 1, 0, 1), COLORS[self.color])

class RedGoal(CustomGoal):
    def __init__(self):
        super().__init__('red_goal', 'red')

class YellowGoal(CustomGoal):
    def __init__(self):
        super().__init__('yellow_goal', 'yellow')

class BlueGoal(CustomGoal):
    def __init__(self):
        super().__init__('blue_goal', 'blue')

class GreenGoal(CustomGoal):
    def __init__(self):
        super().__init__('green_goal', 'green')



class CustomGrid(Grid):
    def rotate_left(self):
        """
        Rotate the grid to the left (counter-clockwise)
        """

        grid = CustomGrid(self.height, self.width)

        for i in range(self.width):
            for j in range(self.height):
                v = self.get(i, j)
                grid.set(j, grid.height - 1 - i, v)

        return grid

    def slice(self, topX, topY, width, height):
        """
        Get a subset of the grid
        """

        grid = CustomGrid(width, height)

        for j in range(0, height):
            for i in range(0, width):
                x = topX + i
                y = topY + j

                if x >= 0 and x < self.width and \
                   y >= 0 and y < self.height:
                    v = self.get(x, y)
                else:
                    v = Wall()

                grid.set(i, j, v)

        return grid

   
    @staticmethod
    def obj_decode(type_idx, color_idx, state):
        """Create an object from a 3-tuple state description"""

        obj_type = IDX_TO_OBJECT[type_idx]
        color = IDX_TO_COLOR[color_idx]

        if obj_type == 'empty' or obj_type == 'unseen':
            return None

        # State, 0: open, 1: closed, 2: locked
        is_open = state == 0
        is_locked = state == 2

        if obj_type == 'wall':
            v = Wall(color)
        elif obj_type == 'floor':
            v = Floor(color)
        elif obj_type == 'ball':
            v = Ball(color)
        elif obj_type == 'key':
            v = Key(color)
        elif obj_type == 'box':
            v = Box(color)
        elif obj_type == 'door':
            v = Door(color, is_open, is_locked)
        elif obj_type == 'goal':
            v = Goal()
        elif obj_type == 'lava':
            v = Lava()
        elif obj_type == 'red_goal':
            v = RedGoal()
        elif obj_type == 'blue_goal':
            v = BlueGoal()
        elif obj_type == 'yellow_goal':
            v = YellowGoal()
        elif obj_type == 'green_goal':
            v = GreenGoal()
        else:
            assert False, "unknown object type in decode '%s'" % obj_type

        return v

    @staticmethod
    def decode(array):
        """
        Decode an array grid encoding back into a grid
        """

        width, height, channels = array.shape
        assert channels == 3

        vis_mask = np.ones(shape=(width, height), dtype=np.bool)

        grid = CustomGrid(width, height)
        for i in range(width):
            for j in range(height):
                type_idx, color_idx, state = array[i, j]
                v = CustomGrid.obj_decode(type_idx, color_idx, state)
                grid.set(i, j, v)
                vis_mask[i, j] = (type_idx != OBJECT_TO_IDX['unseen'])

        return grid, vis_mask

    


class SimpleMemoryTestingEnv(MiniGridEnv):
    """
    """
    def __init__(
        self,
        easy=False,
        nbr_colors=4,
        width=13,
        height=9,
        see_through_walls=False,
        seed=1337,
        agent_view_size=7,
        max_nbr_steps=50,
    ):  
        self.easy = easy
        self.nbr_colors = nbr_colors

        self.max_nbr_steps = max_nbr_steps

        self.goalEnum2id = {"red":0, "blue":1, "yellow":2, "green":3}
        self.id2goalEnum = dict(zip(self.goalEnum2id.values(), self.goalEnum2id.keys()))
        self.nbr_goals = len(self.goalEnum2id)
        
        self.agent_start_dir = 0

        if self.easy:
            self.goal_positions = [
                np.array([4*width//5, 2*height//5-1]), 
                np.array([4*width//5, 3*height//5+1])
            ]

            self.indicator_position = np.array([width//2+2, height//2])
            self.agent_start_pos = (width//2+1, height//2)
        else:
            self.goal_positions = [
                np.array([4*width//5-1, 2*height//5-1]), 
                np.array([4*width//5-1, 3*height//5+1])
            ]

            self.indicator_position = np.array([width//4+1, height//2])
            # Current position and direction of the agent
            self.agent_start_pos = (width//4, height//2)
                        
        
        super().__init__(
            width=width,
            height=height,
            max_steps=max_nbr_steps,
            see_through_walls=see_through_walls,
            seed=seed,
        )

    def reset(self, **kwargs):
        if 'seed' in kwargs.keys():
            self.seed(seed=kwargs.pop('seed'))
        return super(SimpleMemoryTestingEnv, self).reset(**kwargs)

    def _gen_grid(self, width, height):
        self.door_closed = False

        # Create an empty grid
        self.grid = CustomGrid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        """
        self.goals = np.random.choice(
            a=[RedGoal,BlueGoal,YellowGoal,GreenGoal][:self.nbr_colors],
            size=(2,),
            replace=False
        )
        """
        self.goals = self.np_random.choice(
            a=[RedGoal,BlueGoal,YellowGoal,GreenGoal][:self.nbr_colors],
            size=(2,),
            replace=False
        )

        self.grid.horz_wall(0, width//2-3, width//2)
        self.grid.vert_wall(width//2, 0, height//2)
        self.grid.vert_wall(width//2, height//2+1, height//2-1)
        self.grid.horz_wall(0, width//2-1, width//2)
        
        self.indicator_goal_idx = np.random.randint(low=0, high=2, size=1)
        self.put_obj(self.goals[self.indicator_goal_idx.item()](), *self.indicator_position)
        for goal_id, goal_fn in enumerate(self.goals):
            self.put_obj(goal_fn(), *self.goal_positions[goal_id])

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "get to the indicated goal square."
        self.step_counter = 0

    def get_obs_render(self, obs, tile_size=TILE_PIXELS//2):
        """
        Render an agent observation for visualization
        """

        grid, vis_mask = CustomGrid.decode(obs)

        # Render the whole grid
        img = grid.render(
            tile_size,
            agent_pos=(self.agent_view_size // 2, self.agent_view_size - 1),
            agent_dir=3,
            highlight_mask=vis_mask
        )

        return img

    def __str__(self):
        """
        Produce a pretty string of the environment's grid along with the agent.
        A grid cell is represented by 2-character string, the first one for
        the object and the second one for the color.
        """

        # Map of object types to short string
        OBJECT_TO_STR = {
            'wall'          : 'W',
            'floor'         : 'F',
            'door'          : 'D',
            'key'           : 'K',
            'ball'          : 'A',
            'box'           : 'B',
            'goal'          : 'G',
            'lava'          : 'V',
            'wall_up'       : ' ',
            'wall_down'     : '_',
            'wall_left'     : '|',
            'wall_left_up'  : '[',
            'wall_left_down': ']',
            'wall_right'    : '|',
            'wall_right_up' : '<',
            'wall_right_down': '>',
            'time_bonus'    : 'T',
            'red_goal'      : 'G',
            'blue_goal'     : 'G',
            'yellow_goal'   : 'G',
            'green_goal'    : 'G',
        }

        # Short string for opened door
        OPENDED_DOOR_IDS = '_'

        str = ''

        for j in range(self.grid.height):

            for i in range(self.grid.width):
                if i == self.agent_pos[0] and j == self.agent_pos[1]:
                    str += 'AA'
                    continue

                c = self.grid.get(i, j)

                if c == None:
                    str += '  '
                    continue

                if c.type == 'door':
                    if c.is_open:
                        str += '__'
                    elif c.is_locked:
                        str += 'L' + c.color[0].upper()
                    else:
                        str += 'D' + c.color[0].upper()
                    continue

                str += OBJECT_TO_STR[c.type] + c.color[0].upper()

            if j < self.grid.height - 1:
                str += '\n'

        return str

    def step(self, action):
        self.step_counter += 1

        next_obs, reward, done, next_info = super(SimpleMemoryTestingEnv, self).step(action)

        reward, done = self._reward_done()
        if not self.door_closed\
        and self.agent_pos[0]>self.width//2:
            self.put_obj(Door('yellow', is_locked=True), self.width//2, self.height//2)
            self.door_closed = True 

        return next_obs, reward, done, next_info


    def _reward_done(self):
        reward = -0.1
        done = False 

        # Get the content of the cell where the agent is:
        current_cell = self.grid.get(*self.agent_pos)

        if current_cell is not None\
        and 'goal' in current_cell.type:
            for goal_id, goal_pos in enumerate(self.goal_positions):
                if np.all(self.agent_pos == goal_pos):
                    done = True
                    if goal_id == self.indicator_goal_idx:
                        reward = 5
                    else:
                        reward -= 1
                    break

        if self.step_counter>= self.max_nbr_steps:
            done = True 
            # if reward==0:   
            #     reward = -1

        return reward, done 


def generate_env(easy=False, **kwargs):
    env = SimpleMemoryTestingEnv(easy=easy, **kwargs)
    env = RGBImgPartialObsWrapper(env) # Get pixel observations
    env = ImgObsWrapper(env) # Get rid of the 'mission' field
    return env 

def generate_2colors_env(**kwargs):
    return generate_env(easy=False, nbr_colors=2, **kwargs)

def generate_easy_env(**kwargs):
    return generate_env(easy=True, **kwargs)

def generate_easy_2colors_env(**kwargs):
    return generate_env(easy=True, nbr_colors=2, **kwargs)