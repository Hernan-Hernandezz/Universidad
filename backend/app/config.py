from icecream import ic
import os


def setup_icecream():
    if os.getenv("ENVIRONMENT") == "production":
        ic.disable()
    else:
        ic.enable()
        ic.configureOutput(prefix="DEBUG | ")
