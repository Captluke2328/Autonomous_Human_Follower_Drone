
def set_system_state(current_state):
    global state
    state = current_state
    
def get_system_state() -> str:
    return state

def set_time(maximum_time):
    global maxTime
    maxTime = maximum_time

def get_time() -> int:
    return maxTime

def set_airborne(air_state):
    global airState
    airState = air_state

def get_airborne() -> str:
    return airState
    