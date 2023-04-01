from dataclasses import dataclass


@dataclass
class State:
    moving: bool = False
    visible: bool = False
    target: tuple = None
    once: bool = False
    next_animation = None
    callback = None    
