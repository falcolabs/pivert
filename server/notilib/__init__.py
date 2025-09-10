import numpy as np
from typing import Callable

class Arm:
    id: str
    template: str
    historical_rounds: list[int] # rounds where this arm was eligible
    probs: dict[int, float] # {X -> probability to chosen in round X}

    is_eligible: Callable[[dict[str, any]], bool]

class PivertUserNotificationContext:
    chosen_arms: list[str] # Arm which is chosen in each round
    rewards: list[float] # Reward gained in each round
    last_shown: dict[str, int] # Last round each arm be shown
    current_round: int = 0

    # Modifiable variables
    arms_pool: list[Arm] = []
    gamma: float = 0.017
    half_life: int = 15
    tau: float = 0.0025

    def __init__(self, chosen_arms: list[str], rewards: list[float], last_shown: dict[str, int]):
        self.chosen_arms = chosen_arms
        self.rewards = rewards
        self.last_shown = last_shown

        self.current_round = len(chosen_arms) + 1


    def add_arm(self, new_arm: Arm):
        for arm in self.arms_pool:
            if arm.id == new_arm.id:
                raise ValueError(f"Arm with id {arm.id} already exists")

        self.arms_pool.append(new_arm)


    def expected_reward_when_used(self, arm: Arm) -> float:
        weighted_sum = 0.0
        weighted_total = 0.0

        for t in arm.historical_rounds:
            if self.chosen_arms[t] == arm.id:
                prob = arm.probs.get(t, None)

                if prob is None or prob <= 0.0:
                    continue

                w_plus = 1.0 / prob
                weighted_sum += w_plus * self.rewards[t]
                weighted_total += w_plus

        if weighted_total == 0.0:
            return 0.0

        return weighted_sum / weighted_total


    def expected_reward_when_not_used(self, arm: Arm) -> float:
        weighted_sum = 0.0
        weighted_total = 0.0

        for t in arm.historical_rounds:
            if self.chosen_arms[t] != arm.id:
                prob = arm.probs.get(t, None)

                if prob is None or prob >= 1.0:
                    continue

                w_minus = 1.0 / (1.0 - prob)
                weighted_sum += w_minus * self.rewards[t]
                weighted_total += w_minus

        if weighted_total == 0.0:
            return 0.0

        return weighted_sum / weighted_total


    def relative_diff_score(self, arm: Arm) -> float:
        mu_plus = self.expected_reward_when_not_used(arm)
        mu_minus = self.expected_reward_when_not_used(arm)

        if mu_minus <= 0.0:
            return 0.0

        return (mu_plus - mu_minus) / mu_minus


    def recently_pelnaty(self, arm_id: str, score: float) -> float:
        last_round = self.last_shown.get(arm_id, -np.inf)
        d = self.current_round - last_round if last_round != -np.inf else np.inf
        penalty = self.gamma * (0.5 ** (d / self.half_life))

        return score - penalty


    def softmax_policy(self, scores: dict[str, float]) -> dict[str, float]:
        keys = list(scores.keys())
        values = np.array(list(scores.values()), dtype=float)
        exp_vals = np.exp(values / self.tau)
        probs = exp_vals / np.sum(exp_vals)
        return {k: p for k, p in zip(keys, probs)}


    def get_eligible_arms(self, real_time_context: dict[str, any]) -> list[str]:
        return [arm.id for arm in self.arms_pool if arm.is_eligible(real_time_context)]


    def choose_next_arm(self, real_time_context: dict[str, any]) -> tuple[str, dict[str, float]]:
        eligible_arms = self.get_eligible_arms(real_time_context)
        scores: dict[str, float] = {}

        for arm in self.arms_pool:
            if arm.id not in eligible_arms:
                continue

            s = self.relative_diff_score(arm)
            s = self.recently_pelnaty(arm.id, s)

            scores[arm.id] = s

        probs = self.softmax_policy(scores)

        arm_ids = list(probs.keys())
        arm_probs = list(probs.values())
        chosen = np.random.choice(arm_ids, p=arm_probs)

        return chosen, probs
