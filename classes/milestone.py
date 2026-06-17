class Milestone:
    def __init__(
        self,
        name,
        description,
        goal,
        value,
        money,
        reputation,
        unlock_components,
        unlock_engines,
    ):
        self.name = name
        self.description = description
        self.goal = goal
        self.value = value
        self.money = money
        self.reputation = reputation
        self.unlock_components = unlock_components  # names only
        self.unlock_engines = unlock_engines  # names only
        self.achieved = False

    def check_achivement_list(self, player):
        if self.achieved:
            return False
        for milestone_name in player.milestones_completed:
            if milestone_name == self.name:
                return False
        return True

    def check_achievement(self, rocket, player):
        if self.achieved:
            return False
        for milestone_name in player.milestones_completed:
            if milestone_name == self.name:
                return False
        if self.goal == "max_alt":
            if rocket.max_alt >= self.value:
                player.money += self.money
                player.reputation += self.reputation
                player.unlocked_components.extend(self.unlock_components)
                player.unlocked_engines.extend(self.unlock_engines)
                player.milestones_completed.append(self.name)
                self.achieved = True
                return True
        elif self.goal == "max_v":
            if rocket.max_v >= self.value:
                player.money += self.money
                player.reputation += self.reputation
                player.unlocked_components.extend(self.unlock_components)
                player.unlocked_engines.extend(self.unlock_engines)
                player.milestones_completed.append(self.name)
                self.achieved = True
                return True
