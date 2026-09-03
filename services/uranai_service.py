import random

fortunes = [
    ("大吉", "✨🐟🐟🐟✨", 5),
    ("吉", "✨🐟✨", 15),
    ("中吉", "🐟", 50),
    ("小吉", "🪼", 20),
    ("末吉", "🫧", 10),
]

def draw_fortune():
    return random.choices(fortunes, weights=[fortune[2] for fortune in fortunes], k=1)[0]