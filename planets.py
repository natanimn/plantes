from cs1graphics import *
import math
import time
import random

# Create the canvas
canvas = Canvas(1100, 800, "black", "Solar System Simulation")
CENTER = Point(500, 400)

# Intro text for the game
intro_text = Text("Planets Motion", 40, Point(550, 200))
intro_text.setFontColor("white")
canvas.add(intro_text)

# Animate the text (fade in, move up, and grow in size)
for size in range(1, 45, 2):  # Growing text size
    intro_text.setFontSize(size)
    time.sleep(0.05)

for opacity in range(0, 250, 10):
    # Fade in effect (opacity)
    intro_text.setFontColor((opacity, opacity, opacity))  # Simulate opacity with RGB values
    time.sleep(0.07)

# Move text up after fading in
for y in range(200, 30, -2):  # Move upwards
    intro_text.moveTo(550, y)
    time.sleep(0.02)

# Display the sun and planets after intro
time.sleep(1)  # Hold the position before the planets show
# canvas.remove(intro_text)



# Helper function to create a planet with a highlight
def create_planet(center, radius, color):
    body = Circle(radius, center)
    body.setFillColor(color)
    
    highlight = Circle(radius * 0.47, Point(center.getX() - radius * 0.3, center.getY() - radius * 0.3))
    highlight.setFillColor("white")
    highlight.setBorderColor("transparent")
    highlight.setDepth(1)
    
    return body, highlight

# Helper function to create Saturn's ring
def create_ring(center, planet_radius, ring_radius, ring_width):
    ring = Ellipse(ring_radius, ring_width - 10, center)
    ring.setBorderColor("gray")
    ring.setBorderWidth(3)
    ring.setFillColor("transparent")
    ring.setDepth(50)
    return ring

# Add the sun
sun_layer = Layer()
sun_circle = Circle(55, Point(550, 400))
sun_circle.setFillColor("yellow")
sun_highlight = Circle(25, Point(535, 380))
sun_highlight.setFillColor('white')
sun_highlight.setBorderColor('transparent')
sun_layer.add(sun_circle)
sun_layer.add(sun_highlight)
canvas.add(sun_layer)

# Define planets
planets = [
    {"name": "Mercury", "distance": 15, "radius": 7, "color": "light gray", "speed": 2.5},
    {"name": "Venus", "distance": 20, "radius": 10, "color": "orange", "speed": 1.8},
    {"name": "Earth", "distance": 28, "radius": 15, "color": "Deep Sky Blue", "speed": 1.5},
    {"name": "Mars", "distance": 35, "radius": 9, "color": "orange red", "speed": 1.2},
    {"name": "Jupiter", "distance": 45, "radius": 30, "color": "brown", "speed": 0.8},
    {"name": "Saturn", "distance": 55, "radius": 22, "color": "gold", "speed": 0.6},
    {"name": "Uranus", "distance": 65, "radius": 15, "color": "cyan", "speed": 0.4},
    {"name": "Neptune", "distance": 75, "radius": 11, "color": "darkblue", "speed": 0.3},
]

# Add orbit paths
for planet in planets:
    orbit = Ellipse(planet["distance"] * 14, planet["distance"] * 8, Point(550, 400))
    orbit.setBorderColor("Light Steel Blue")
    orbit.setBorderWidth(1)
    orbit.setDepth(100)
    canvas.add(orbit)

# Fixed positions for 400 stars
fixed_star_positions = [
    (x, y) for x in range(50, 1100, 25) for y in range(50, 800, 20)
    if not (450 <= x <= 650 and 300 <= y <= 450)  # Avoid overlapping with the Sun and orbits
]

# Adjust the number of stars
random.shuffle(fixed_star_positions)  # Shuffle positions for natural look
fixed_star_positions = fixed_star_positions[:300]  # Limit to 400 stars

stars = []
# Add stars to the canvas
for x, y in fixed_star_positions:
    size = random.randint(1, 3)  # Slight variation in size
    brightness = random.choice(["white", "lightgray", "gray"])  # Varied brightness
    star = Circle(size, Point(x, y))
    star.setFillColor(brightness)
    star.setBorderColor("transparent")
    canvas.add(star)
    stars.append(star)


# Create planets
planet_layers = []
planet_highlights = []
rings = [] 

for planet in planets:
    initial_position = Point(550 + planet["distance"] * 7, 400)
    planet_layer, planet_highlight = create_planet(initial_position, planet["radius"], planet["color"])
    canvas.add(planet_layer)
    canvas.add(planet_highlight)
    if planet['name'] == "Saturn":
        planet_highlight.setDepth(0)
        planet_layer.setDepth(0)
    planet_layers.append({"layer": planet_layer,
                          "distance": planet["distance"],
                          "angle": 0,
                          "speed": planet["speed"]})
    
    planet_highlights.append({"highlight": planet_highlight,
                              "distance": planet["distance"],
                              "angle": 0, "speed": planet["speed"]})

    if planet["name"] == "Saturn":
        ring = create_ring(initial_position, planet["radius"], 80, 30)
        canvas.add(ring)
        rings.append({"ring": ring, "distance": planet["distance"], "angle": 0})
        rings *= 8

def make_animation(planets):
    for body_obj, highlight_obj, planet, ring_obj in zip(planet_layers, planet_highlights, planets, rings):
         
        body_obj["angle"] += planet["speed"] * 6
        highlight_obj["angle"] += planet["speed"]
        ring_obj["angle"] += planet["speed"]
        
        body_obj["angle"] %= 360
        highlight_obj["angle"] %= 360
        ring_obj["angle"] %= 360
        
        angle_rad = math.radians(body_obj["angle"])
        x = 550 + body_obj["distance"] * math.cos(angle_rad) * 7
        y = 400 + body_obj["distance"] * math.sin(angle_rad) * 4
        
        body_obj["layer"].moveTo(x, y)
        highlight_obj["highlight"].moveTo(x - body_obj["layer"].getRadius() * 0.3, y - body_obj["layer"].getRadius() * 0.3)
        if planet["name"] == "Saturn":
            ring_obj["ring"].moveTo(x, y)


while True:
    make_animation(planets)
    random.shuffle(stars)
    for star in (stars)[:40]:
        brightness_change = random.choice(["white", "lightgray", "gray"])  # Random brightness
        star.setFillColor(brightness_change)
    time.sleep(0.03)
