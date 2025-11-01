class Donkey:
    """
    Represents the space donkey that travels across the galaxy.
    Keeps track of health, energy, food, age, and remaining life span.
    """

    HEALTH_LEVELS = ["excellent", "good", "regular", "bad", "dying", "dead"]

    def __init__(self, health="excellent", age=5, energy=100, grass_kg=10, life_left=100):
        self.health = health              # Health condition
        self.age = age                    # Age in years
        self.energy = energy              # 0 - 100 (%)
        self.grass_kg = grass_kg          # Amount of grass available
        self.life_left = life_left        # Life expectancy in light-years
        self.current_star = None          # Current location (Star object or ID)
        self.alive = True

    # -------------------------------------------------
    #  Core status methods
    # -------------------------------------------------
    def is_alive(self):
        """Returns True if the donkey is still alive."""
        return self.alive and self.health != "dead" and self.life_left > 0

    def lose_life(self, amount):
        """Reduces life span when traveling."""
        self.life_left -= amount
        if self.life_left <= 0:
            self.die()

    def consume_energy(self, amount):
        """Consumes donkey energy due to travel or research."""
        self.energy -= amount
        if self.energy <= 0:
            self.energy = 0
            self.update_health_on_low_energy()

    def eat_grass(self, kg):
        """
        Donkey eats grass to recover energy.
        Each kg gives different recovery depending on health.
        """
        if self.grass_kg <= 0:
            return

        kg_to_eat = min(kg, self.grass_kg)
        self.grass_kg -= kg_to_eat

        recovery_rate = {
            "excellent": 5,
            "good": 4,
            "regular": 3,
            "bad": 2,
            "dying": 1
        }.get(self.health, 0)

        recovered = recovery_rate * kg_to_eat
        self.energy = min(100, self.energy + recovered)

    def update_health_on_low_energy(self):
        """Degrades the donkey's health when energy is too low."""
        if self.energy < 20:
            if self.health == "excellent":
                self.health = "good"
            elif self.health == "good":
                self.health = "regular"
            elif self.health == "regular":
                self.health = "bad"
            elif self.health == "bad":
                self.health = "dying"
            elif self.health == "dying":
                self.die()

    def die(self):
        """Handles donkey's death."""
        self.health = "dead"
        self.alive = False
        self.energy = 0
        print("💀 The donkey has died...")  # Later we’ll trigger sound here.

    # -------------------------------------------------
    #  Movement and interaction
    # -------------------------------------------------
    def move_to(self, star, distance):
        """Moves the donkey to a new star and consumes life and energy."""
        if not self.is_alive():
            return False

        self.current_star = star
        self.consume_energy(distance * 2)   # arbitrary travel cost
        self.lose_life(distance)            # 1 year per light-year traveled
        return self.is_alive()

    def research_at_star(self, star):
        """Simulates research work that consumes energy and time."""
        if not self.is_alive():
            return False

        self.consume_energy(star.energy_cost)
        self.lose_life(star.investigation_time)
        self.life_left += star.life_delta   # gain or lose depending on the star
        return self.is_alive()

    def recharge_on_hypergiant(self):
        """Special ability for hypergiant stars."""
        if not self.is_alive():
            return
        self.energy = min(100, self.energy * 1.5)
        self.grass_kg *= 2

    def to_dict(self):
        """Returns a dictionary for serialization or reporting."""
        return {
            "health": self.health,
            "age": self.age,
            "energy": self.energy,
            "grass_kg": self.grass_kg,
            "life_left": self.life_left,
            "current_star": self.current_star.name if self.current_star else None,
            "alive": self.alive
        }

    def __repr__(self):
        return (f"Donkey(health={self.health}, energy={self.energy}%, "
                f"grass={self.grass_kg}kg, life_left={self.life_left}ly)")
