from vpython import sphere, vector, rate
from vpython import *
import random



G = 1
M = 1
R = 1
rsoft = 0.3
w = vector(0,0.08,0)
n = 0
N = 9
stars = []

# Create the sun at the center
sun = sphere(pos=vector(0,0,0), radius=R/5, color=color.yellow, make_trail=True)
sun.m = 10*M  # Sun has much larger mass
sun.p = vector(0, 0, 0)  # Sun starts stationary
sun.F = vector(0, 0, 0)
stars.append(sun)

while n<N:
  # Place objects in a ring between 3R and 5R from the sun
  distance = 3*R + 2*R*random.random()  # Random distance between 3R and 5R
  angle_xy = 2*3.14159*random.random()  # Random angle in xy plane
  angle_z = 0.2*(2*random.random()-1)   # Small random z component
  
  rt = distance * vector(cos(angle_xy), sin(angle_z), sin(angle_xy))
  
  # Create bright vivid colors for each star
  bright_colors = [color.red, color.blue, color.green, color.magenta, 
                   color.cyan, color.orange, color.purple, color.white]
  random_color = bright_colors[random.randint(0, len(bright_colors)-1)]
  
  stars = stars + [sphere(pos=rt,radius=R/30,make_trail=True,retain=350,color=random_color)]
  n = n + 1

for star in stars:
  if star != sun:  # Skip the sun when setting properties for smaller stars
    star.m = M/N
    
    # Calculate proper orbital velocity to prevent crashing into sun
    distance_from_sun = mag(star.pos)
    orbital_speed = 0.5*sqrt(G * sun.m / distance_from_sun)
    
    # Create velocity perpendicular to position vector (tangential to orbit)
    pos_xy = vector(star.pos.x, 0, star.pos.z)  # Project to xy plane
    velocity_direction = vector(-pos_xy.z, 0, pos_xy.x)  # Rotate 90 degrees
    velocity_direction = norm(velocity_direction)  # Normalize to unit vector
    
    star.p = star.m * orbital_speed * velocity_direction
    star.F = vector(0,0,0)

t = 0
dt = 0.01

while t<100:
  rate(100)
  for star in stars:
    star.F = vector(0,0,0)
  for i in range(len(stars)):
    for j in range(len(stars)):
      if i!=j:
        rji = stars[i].pos - stars[j].pos
        stars[i].F = stars[i].F - G*stars[i].m*stars[j].m*norm(rji)/(mag(rji)**2+rsoft**2)
        
  for star in stars:
    star.p = star.p + star.F*dt
    star.pos = star.pos + star.p*dt/star.m
  t = t + dt


