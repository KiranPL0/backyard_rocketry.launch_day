class Player:
    def __init__(
        self,
        money=200,
        reputation=0,
        active_contract=None,
        completed_contracts=[],
        stage=0,
        unlocked_components=[],
        unlocked_engines=[],
        xp=0,
        launches=0,
        career_apogee=0,
        career_max_velocity=0,
        milestones_completed=[],
    ):
        self.money = money
        self.reputation = reputation
        self.active_contract = active_contract
        self.completed_contracts = completed_contracts  # names only
        self.stage = stage
        self.unlocked_components = unlocked_components
        self.unlocked_engines = unlocked_engines
        self.xp = xp
        self.launches = launches
        self.career_apogee = career_apogee
        self.career_max_velocity = career_max_velocity
        self.milestones_completed = milestones_completed
        self.unlocked_engines = []  # names only
        self.unlocked_components = []  # names only

    def accept_contract(self, contract):
        self.active_contract = contract

    def export_data(self):
        return {
            "money": self.money,
            "reputation": self.reputation,
            "active_contract": (
                self.active_contract.name if self.active_contract is not None else None
            ),
            "completed_contracts": self.completed_contracts,
            "stage": self.stage,
            "unlocked_components": self.unlocked_components,
            "unlocked_engines": self.unlocked_engines,
            "xp": self.xp,
            "launches": self.launches,
            "career_apogee": self.career_apogee,
            "career_max_velocity": self.career_max_velocity,
            "milestones_completed": self.milestones_completed,
        }
