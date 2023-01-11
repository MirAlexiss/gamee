from projectile import Projectile

class Ship:
    COOLDOWN = 30
    
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.projectile_img = None
        self.projectiles = []
        self.cool_down_counter = 0

    def draw(self, surfacedow):
        surfacedow.blit(self.ship_img, (self.x, self.y))
        for projectile in self.projectiles:
            projectile.draw(surfacedow)

    def move_projectiles(self, vel, obj):
        self.cooldown()
        for projectile in self.projectiles:
            projectile.move(vel)
            if projectile.off_screen(500):
                self.projectiles.remove(projectile)
            elif projectile.collision(obj):
                obj.health -= 10
                self.projectiles.remove(projectile)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            projectile = Projectile(self.x - 8, self.y - 30, self.projectile_img)
            self.projectiles.append(projectile)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
