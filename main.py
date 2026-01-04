from fastmcp import FastMCP
import random

mcp = FastMCP(name="DemoMCP")

@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
    """Roll a specified number of six-sided dice."""
    return [random.randint(1, 7) for _ in range(n_dice)]

@mcp.tool
def add_two_numbers(a: float,b:float)->float:
    """Add two numbers and return the result."""
    return a + b

if __name__ == "__main__":
    mcp.run()
