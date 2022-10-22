
def set_system_state(current_state):
    global state
    state = current_state
    
def get_system_state() -> str:
    return state
    