class Explosion:
    def __init__(self, x, y, explosion_frames):
        self.frames = explosion_frames
        self.image_index = 0
        self.rect = self.frames[self.image_index].get_rect()
        self.rect.center = (x, y)
        self.frame_delay = 5
        self.frame_counter = 0
        self.is_active = True

    def update(self):
        if self.is_active:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.image_index += 1
                if self.image_index >= len(self.frames):
                    self.is_active = False

    def draw(self, screen):
        if self.is_active:
            screen.blit(self.frames[self.image_index], self.rect)

