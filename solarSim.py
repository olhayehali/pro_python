#Author: Olhayeh ali
#date:24/02/2022

import math
import time
import pygame


WIDTH , HEIGHT = 600,600

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (200,200,100) 
BLUE = (0,0,200)
ORANGE = (255,0,0)

RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

planets = []
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

# Assumed scale: 100 pixels = 1AU.
AU = int(150e6 * 1000)     # 150 million km, in meters.
SCALE = 100 / AU

timestamp =0


# Run until the user asks to quit
running = True
pygame.display.set_caption('solar system simulation')
myfont = pygame.font.SysFont('Comic Sans MS', 30)
font = pygame.font.Font(pygame.font.get_default_font(), 10)
class Body():
    """
    representing a gravitationally-acting body.
    Extra attributes:
    mass : mass in kg
    vx, vy: x, y velocities in m/s
    px, py: x, y positions in m

    """
    # The gravitational constant G
    G = 6.67428e-11

    def __init__(self,name,mass,color,x,y,radius,isStar=False):
        
        self.name = name
        self.mass = mass
        self.color=color
        self.radius = radius #* SCALE
        self.timestep = 15*3600  # One day
        self.isStar = isStar
        self.vx = 0
        self.vy = 0
        self.x = x
        self.y = y
        self.orbit = []
        self.distance_to_sun = 0
    def attraction(self, other):
        """(Body): (fx, fy)

        Returns the force exerted upon this body by the other body.
        """
        # Compute the distance of the other body.
        sx, sy = self.x, self.y
        ox, oy = other.x, other.y
        dx = (ox-sx)
        dy = (oy-sy)
        d = math.sqrt(dx**2 + dy**2)

        # Compute the force of attraction
        f = self.G * self.mass * other.mass / (d**2)
        if other.name == 'sun':
            self.distance_to_sun =d
        # Compute the direction of the force.
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        return fx, fy
    def update_position(self,planets,sun):
        total_fx ,total_fy = 0,0
        for planet in planets:
            if self.name == planet.name:       
                continue
            fx , fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        fx , fy = self.attraction(sun)
        total_fx += fx
        total_fy += fy

        self.vx +=total_fx / self.mass * self.timestep
        self.vy +=total_fy / self.mass * self.timestep

        self.x += self.vx * self.timestep
        self.y += self.vy * self.timestep
        self.orbit.append((self.x,self.y))


    def draw(self,win):
        x = int(self.x*SCALE + WIDTH/2)
        y = int(self.y*SCALE + HEIGHT/2)
        updated_points = []
        if len(self.orbit) > 2:
            for point in self.orbit:
                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        pygame.draw.circle(win,self.color,(int(x),int(y)),self.radius)
        textsurface = font.render(self.name, False, (0, 0, 0),WHITE)
        if self.distance_to_sun > 0:
            distance = font.render(f"{self.distance_to_sun/1000} Km", False, (0, 0, 0),WHITE)
            win.blit(distance,(x+self.radius-10,y-self.radius-10))
        win.blit(textsurface,(x,y-self.radius-10))

def show_info():
    global SCALE
    global timestamp

    textsurface = font.render(f'{timestamp}days Scale:{SCALE} ', False, (0, 0, 0),WHITE)

    WIN.blit(textsurface,(100,100))

def loop(planets,star):
    clock = pygame.time.Clock()
    global running,SCALE,timestamp
    while running:
        clock.tick(60)
        #white background
        WIN.fill(BLACK)
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for planet in planets:
                        planet.timestep -=3600*24
                        print('substract')
                if event.key == pygame.K_RIGHT:
                    for planet in planets:
                        planet.timestep +=3600*24
                        print('added')
                if event.key == pygame.K_UP:
                        SCALE *= 5
                        print('zoom in')
                if event.key == pygame.K_DOWN:
                        SCALE /=5
                        print('zoom out')
        timestamp+=1
            
        star.draw(WIN)
        for planet in planets:
            planet.update_position(planets,star)
            planet.draw(WIN)
        pygame.display.update()
        time.sleep(0.001)
        show_info()
def main():

    # Venus parameters taken from
    # http://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
    sun = Body(name='Sun',color=YELLOW,mass=1.98892 * 10**30,isStar=True,radius=30,x=0,y=0)

    earth = Body(name='Earth',color=BLUE,mass=5.9742 * 10**24,radius=10,x=-1*AU,y=0)
    earth.vy = 29.783 * 1000            # 29.783 km/sec

    venus = Body(name='Venus',color=ORANGE,mass=4.8685 * 10**24,radius=8,x=0.723 * AU,y=0)
    venus.vy = -35.02 * 1000            # 35.02 km/sec

    mercury = Body(name='mercury',color=WHITE,mass=4.8685 * 10**24,radius=4,x=0.387 * AU,y=0)
    mercury.vy = -47.4 * 1000          # 35.02 km/sec

    mars = Body(name='mars',color=RED,mass=4.8685 * 10**24,radius=9,x=-1.524 * AU,y=0)
    mars.vy = 24.077 * 1000            # 35.02 km/sec

    jupiter = Body(name='jupiter',color=(0,250,0),mass=1898.13* 10**24,radius=15,x=5.2 * AU,y=0)
    jupiter.vy = -15.2 * 1000            # 35.02 km/sec


    planets = [earth,venus,mercury,mars,jupiter]
    
    star = sun

    loop(planets,star)

if __name__ == '__main__':
    main()