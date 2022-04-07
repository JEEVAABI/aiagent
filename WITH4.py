import random
import time


class Thing:
    """
    This represents any physical object that can appear in an Environment.
    """

    def is_alive(self):
        """Things that are 'alive' should return true."""
        return hasattr(self, "alive") and self.alive

    def show_state(self):
        """Display the agent's internal state. Subclasses should override."""
        print("I don't know how to show_state.")


class Agent(Thing):
    """
    An Agent is a subclass of Thing
    """

    def __init__(self, program=None):
        self.alive = True
        self.performance = 0
        self.program = program

    def can_grab(self, thing):
        """Return True if this agent can grab this thing.
        Override for appropriate subclasses of Agent and Thing."""
        return False

def TableDrivenAgentProgram(table):
    """
    [Figure 2.7]
    This agent selects an action based on the percept sequence.
    It is practical only for tiny domains.
    To customize it, provide as table a dictionary of all
    {percept_sequence:action} pairs.
    """
    percepts = []

    def program(percept):
        percepts.append(percept)
        action = table.get(tuple(percept))
        return action

    return program


room_A, room_B,room_C, room_D = (0,0), (1,0),(1,1),(0,1) # The four locations for the Doctor to treat


def TableDrivenDoctorAgent():
    """
    Tabular approach towards hospital function.
    """
    table = {
        (room_A, "healthy"): "Right",
        (room_A, "unhealthy"): "treat",
        (room_B, "healthy"): "Up",
        (room_B, "unhealthy"): "treat",
        (room_C, "healthy"): "Left",
        (room_C, "unhealthy"): "treat",
        (room_D, "healthy"): "Down",
        (room_D, "unhealthy"): "treat",
        
    }
    return Agent(TableDrivenAgentProgram(table))


class Environment:
    """Abstract class representing an Environment. 'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def percept(self, agent):
        """Return the percept that the agent sees at this point. (Implement this.)"""
        raise NotImplementedError

    def execute_action(self, agent, action):
        """Change the world to reflect this action. (Implement this.)"""
        raise NotImplementedError

    def default_location(self, thing):
        """Default location to place a new thing with unspecified location."""
        return None

    def is_done(self):
        """By default, we're done when we can't find a live agent."""
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do. If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this.)"""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = (
                location if location is not None else self.default_location(thing)
            )
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: {} at {}".format(thing, thing.location))
            print(
                "  from list: {}".format(
                    [(thing, thing.location) for thing in self.things]
                )
            )
        if thing in self.agents:
            self.agents.remove(thing)


class TrivialDoctorEnvironment(Environment):
    """This environment has two locations, A and B. Each can be Dirty
    or Clean. The agent perceives its location and the location's
    status. This serves as an example of how to implement a simple
    Environment."""

    def __init__(self):
        super().__init__()
        self.status = {
            room_A: random.choice(["healthy", "unhealthy"]),
            room_B: random.choice(["healthy", "unhealthy"]),
            room_C: random.choice(["healthy", "unhealthy"]),
            room_D: random.choice(["healthy", "unhealthy"])
        }

    def thing_classes(self):
        return [TableDrivenDocterAgent]

    def percept(self, agent):
        """Returns the agent's location, and the location status (unhealthy/healthy)."""
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        if action == "Right":
            agent.location = room_B
            agent.performance -= 1
        elif action == "Up":
            agent.location = room_C
            agent.performance -= 1
        elif action == "Left":
            agent.location = room_D
            agent.performance -= 1
        elif action == "Down":
            agent.location = room_A
            agent.performance -= 1
        elif action == "treat":
            self.status[agent.location]=='unhealthy'
            tem=float(input("Enter your temperature"))
            if tem>=98.5:
                agent.performance += 10
                print("medicine prescribed: paracetamol,anti-biotic(low dose)")
                self.status[agent.location] = "healthy"
        


    def default_location(self, thing):
        """Agents start in either location at random."""
        return random.choice([room_A, room_B, room_C, room_D])


if __name__ == "__main__":
    agent = TableDrivenDoctorAgent()
    environment = TrivialDoctorEnvironment()
    environment.add_thing(agent)
    print("\tStatus of patients in rooms before treatment")
    print(environment.status)
    print("AgentLocation : {0}".format(agent.location))
    print("Performance : {0}".format(agent.performance))
    time.sleep(3)

    for i in range(5):
        environment.run(steps=10)
        print("\n\tStatus of patient in room after the treatment")
        print(environment.status)
        print("AgentLocation : {0}".format(agent.location))
        print("Performance : {0}".format(agent.performance))
        time.sleep(3)
