class Contract:
    def __init__(
        self,
        name,
        description,
        goal,
        value,
        money,
        reputation,
        company,
        stage,
        reputation_required,
        unlock_components,
        unlock_engines,
    ):
        self.name = name
        self.description = description
        self.goal = goal
        self.value = value
        self.money = money
        self.reputation = reputation
        self.company = company
        self.stage = stage
        self.reputation_required = reputation_required
        self.unlock_components = unlock_components
        self.unlock_engines = unlock_engines
        self.completed = False

    def check_contract_completion(self, player, rocket):
        from assets.asset_loader import update_loaded_components, update_loaded_engines

        if self.goal == "launch_with":
            values = self.value.split("/")
            if values[0] == "engine":
                if rocket.engine.name == values[1] and self.completed == False:
                    # handle completion
                    player.money += self.money
                    player.reputation += self.reputation
                    player.unlocked_engines.extend(self.unlock_engines)
                    player.unlocked_components.extend(self.unlock_components)
                    player.completed_contracts.append(self.name)
                    update_loaded_engines(player)
                    update_loaded_components(player)
                    self.completed = True
                    return True
                elif rocket.engine.name == values[1]:
                    return True
            elif values[0] == "structure":
                if rocket.check_component(values[1]) and self.completed == False:
                    # handle completion
                    player.money += self.money
                    player.reputation += self.reputation
                    player.unlocked_engines.extend(self.unlock_engines)
                    player.unlocked_components.extend(self.unlock_components)
                    player.completed_contracts.append(self.name)
                    update_loaded_engines(player)
                    update_loaded_components(player)
                    self.completed = True
                    return True
                elif rocket.check_component(values[1]):
                    return True
        elif self.goal == "max_alt":
            if rocket.max_alt >= self.value and self.completed == False:
                # handle completion
                player.money += self.money
                player.reputation += self.reputation
                player.unlocked_engines.extend(self.unlock_engines)
                player.unlocked_components.extend(self.unlock_components)
                player.completed_contracts.append(self.name)
                update_loaded_engines(player)
                update_loaded_components(player)
                self.completed = True
                return True
            elif rocket.max_alt >= self.value:
                return True
        elif self.goal == "max_v":
            if rocket.max_v >= self.value and self.completed == False:
                # handle completion
                player.money += self.money
                player.reputation += self.reputation
                player.unlocked_engines.extend(self.unlock_engines)
                player.unlocked_components.extend(self.unlock_components)
                player.completed_contracts.append(self.name)
                update_loaded_engines(player)
                update_loaded_components(player)
                self.completed = True
                return True
            elif rocket.max_v >= self.value:
                return True
        return False

    def check_requirements(self, player):
        for i in player.completed_contracts:
            if i == self.name:
                return False
        if player.reputation < self.reputation_required or player.stage != self.stage:
            return False
        else:
            return True
