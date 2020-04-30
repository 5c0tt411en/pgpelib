import pybullet_envs
import gym
from gym.envs.registration import register, EnvSpec


class TinyTrajHumanoidBulletEnv(gym.Env):
    ID = "TinyTrajHumanoidBulletEnv-v0"
    ENTRY_POINT = __name__ + ":TinyTrajHumanoidBulletEnv"
    MAX_EPISODE_STEPS = 200

    def __init__(self, trajectory_length=200):
        gym.Env.__init__(self)

        self.__tlimit = trajectory_length
        self.__done = True
        self.__t = 0
        self.__contained_env = gym.make('HumanoidBulletEnv-v0')

        self.observation_space = self.__contained_env.observation_space
        self.action_space = self.__contained_env.action_space
        self.reward_range = (float('-inf'), float('inf'))

    def step(self, action):
        assert not self.__done, "Trying to progress in a finished trajectory"

        observation, _, done, info = self.__contained_env.step(action)
        self.__t += 1

        if self.__t >= self.__tlimit:
            done = True

        self.__done = done

        reward = sum(self.__contained_env.rewards[1:])
        return observation, reward, done, info

    def reset(self):
        self.__done = False
        self.__t = 0
        return self.__contained_env.reset()

    def render(self, mode='human', **kwargs):
        self.__contained_env.render(mode=mode, **kwargs)

    def close(self):
        return self.__contained_env.close()

    def seed(self, seed=None):
        return self.__contained_env.seed(seed)

    @property
    def rewards(self):
        if hasattr(self.__contained_env, "rewards"):
            return self.__contained_env.rewards
        else:
            return None

    @property
    def reward(self):
        if hasattr(self.__contained_env, "reward"):
            return self.__contained_env.reward
        else:
            return None

    @property
    def body_xyz(self):
        if hasattr(self.__contained_env.robot, "body_xyz"):
            return self.__contained_env.robot.body_xyz
        else:
            return None

    @property
    def body_rpy(self):
        if hasattr(self.__contained_env.robot, "body_rpy"):
            return self.__contained_env.robot.body_rpy
        else:
            return None

    def camera_adjust(self):
        return self.__contained_env.camera_adjust()

    @property
    def robot(self):
        return self.__contained_env


register(
    id=TinyTrajHumanoidBulletEnv.ID,
    entry_point=TinyTrajHumanoidBulletEnv.ENTRY_POINT,
    max_episode_steps=TinyTrajHumanoidBulletEnv.MAX_EPISODE_STEPS
)

