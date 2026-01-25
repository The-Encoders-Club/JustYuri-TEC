init python:
    # Updated screenshot function
    def screenshot_srf():
        # Get the render of the root displayable of the current screen.
        srf = renpy.render(renpy.get_screen("predict").root, renpy.get_physical_size()[0], renpy.get_physical_size()[1], 0, 0)
        return srf

    # Updated invert function
    def invert():
        srf = screenshot_srf()
        # Create a new render to hold the inverted surface.
        inv_render = renpy.Render(srf.get_width(), srf.get_height())
        # Get the surface from the render.
        inv_surface = inv_render.canvas().get_surface()
        # Invert the original surface onto the new one.
        renpy.invert_surface(srf, inv_surface, (0,0))
        return inv_surface

    class Invert(renpy.Displayable):
        def __init__(self, delay=0.0, **kwargs):
            super().__init__(**kwargs)
            self.width, self.height = renpy.get_physical_size()
            self.srf = invert()
            self.delay = delay

        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            if st >= self.delay:
                render.blit(self.srf, (0, 0))
            return render

    def hide_windows_enabled(enabled=True):
        global _windows_hidden
        _windows_hidden = not enabled


screen invert(length, delay=0.0):
    add Invert(delay) xysize (1280, 720)
    timer delay action PauseAudio("music")
    timer delay action Play("sound", "sfx/glitch1.ogg")
    timer length + delay action Hide("invert")
    on "show" action Function(hide_windows_enabled, enabled=False)
    on "hide" action PauseAudio("music", False)
    on "hide" action Stop("sound")
    on "hide" action Function(hide_windows_enabled, enabled=True)


init python:
    class TearPiece:
        def __init__(self, startY, endY, offtimeMult, ontimeMult, offsetMin, offsetMax):
            self.startY = startY
            self.endY = endY
            self.offTime = (random.random() * 0.2 + 0.2) * offtimeMult
            self.onTime = (random.random() * 0.2 + 0.2) * ontimeMult
            self.offset = 0
            self.offsetMin = offsetMin
            self.offsetMax = offsetMax

        def update(self, st):
            st = st % (self.offTime + self.onTime)
            if st > self.offTime and self.offset == 0:
                self.offset = random.randint(self.offsetMin, self.offsetMax)
            elif st <= self.offTime and self.offset != 0:
                self.offset = 0

    class Tear(renpy.Displayable):
        def __init__(self, number, offtimeMult, ontimeMult, offsetMin, offsetMax, srf=None, **kwargs):
            super().__init__(**kwargs)
            self.width, self.height = renpy.get_physical_size()
            if float(self.width) / float(self.height) > 16.0/9.0:
                self.width = self.height * 16 // 9
            else:
                self.height = self.width * 9 // 16
            self.number = number
            if not srf: self.srf = screenshot_srf()
            else: self.srf = srf
            self.pieces = []
            tearpoints = [0, self.height]
            for i in range(number):
                tearpoints.append(random.randint(10, self.height - 10))
            tearpoints.sort()
            for i in range(number+1):
                self.pieces.append(TearPiece(tearpoints[i], tearpoints[i+1], offtimeMult, ontimeMult, offsetMin, offsetMax))

        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            render.blit(self.srf, (0,0))
            for piece in self.pieces:
                piece.update(st)
                subsrf = self.srf.subsurface((0, max(0, piece.startY - 1), self.width, max(0, piece.endY - piece.startY)))
                render.blit(subsrf, (piece.offset, piece.startY))
            renpy.redraw(self, 0)
            return render

screen tear(number=10, offtimeMult=1, ontimeMult=1, offsetMin=0, offsetMax=50, srf=None):
    zorder 150
    add Tear(number, offtimeMult, ontimeMult, offsetMin, offsetMax, srf) xysize (1280,720)
    on "show" action Function(hide_windows_enabled, enabled=False)
    on "hide" action Function(hide_windows_enabled, enabled=True)

# This class remains largely the same, but the image definitions using it are updated.
init python:
    class RectStatic(object):
        def __init__(self, theDisplayable, numRects=12, rectWidth = 30, rectHeight = 30):
            self.sm = renpy.SpriteManager(update=self.update)
            self.rects = [ ]
            self.timers = [ ]
            self.displayable = theDisplayable
            self.numRects = numRects
            self.rectWidth = rectWidth
            self.rectHeight = rectHeight

            for i in range(self.numRects):
                self.add(self.displayable)
                self.timers.append(random.random() * 0.4 + 0.1)

        def add(self, d):
            s = self.sm.create(d)
            s.x = random.randint(0, 40) * 32
            s.y = random.randint(0, 23) * 32
            s.width = self.rectWidth
            s.height = self.rectHeight
            self.rects.append(s)

        def update(self, st):
            for i, s in enumerate(self.rects):
                if st >= self.timers[i]:
                    s.x = random.randint(0, 40) * 32
                    s.y = random.randint(0, 23) * 32
                    self.timers[i] = st + random.random() * 0.4 + 0.1
            return 0

image m_rectstatic:
    RectStatic(Solid("#000"), 32, 32, 32).sm
    pos (0, 0)
    size (32, 32)

# Updated to use Transform instead of im.FactorScale and im.Crop
image m_rectstatic2:
    Transform(
        child=im.Crop("gui/logo.png", (100, 100, 128, 128)),
        zoom=0.25
    )
    RectStatic(2, 32, 32).sm

image m_rectstatic3:
    Transform(
        child=im.Crop("gui/menu_art_s.png", (100, 100, 64, 64)),
        zoom=0.5
    )
    RectStatic(2, 32, 32).sm

init python:
    class ParticleBurst(object):
        def __init__(self, theDisplayable, explodeTime=0, numParticles=20, particleTime = 0.500, particleXSpeed = 3, particleYSpeed = 5):
            self.sm = SpriteManager(update=self.update)

            self.stars = [ ]
            self.displayable = theDisplayable
            self.explodeTime = explodeTime
            self.numParticles = numParticles
            self.particleTime = particleTime
            self.particleXSpeed = particleXSpeed
            self.particleYSpeed = particleYSpeed
            self.gravity = 240
            self.timePassed = 0

            for i in range(self.numParticles):
                self.add(self.displayable, 1)

        def add(self, d, speed):
            s = self.sm.create(d)
            speed = random.random()
            angle = random.random() * 3.14159 * 2
            xSpeed = speed * math.cos(angle) * self.particleXSpeed
            ySpeed = speed * math.sin(angle) * self.particleYSpeed - 1
            s.x = xSpeed * 24
            s.y = ySpeed * 24
            pTime = self.particleTime
            self.stars.append((s, ySpeed, xSpeed, pTime))

        def update(self, st):
            # Iterate backwards so popping items doesn't break the index
            for sindex in range(len(self.stars) - 1, -1, -1):
                
                # UNPACK THE TUPLE
                # In add(), you stored: (s, ySpeed, xSpeed, pTime)
                s, vy, vx, pTime = self.stars[sindex]
                
                # Apply velocity to the sprite's position
                s.x += vx
                s.y += vy

                # If the star goes off screen, remove it
                if s.x < 0 or s.x > config.screen_width or s.y < 0 or s.y > config.screen_height:
                    self.stars.pop(sindex) 
                    s.destroy() # It is good practice to destroy the sprite from the manager
            
            if len(self.stars) == 0:
                self.sm.destroy()
                return None
            
            return 0

    class Blood(object):
        def __init__(self, theDisplayable, density=120.0, particleTime=1.0, dripChance=0.05, dripSpeedX=0.0, dripSpeedY=120.0, dripTime=180.0, burstSize=100, burstSpeedX=200.0, burstSpeedY=400.0, numSquirts=4, squirtPower=400, squirtTime=0.25):
            self.sm = renpy.SpriteManager(update=self.update)
            self.drops = []
            self.squirts = []
            self.displayable = theDisplayable
            self.density = density
            self.particleTime = particleTime
            self.dripChance = dripChance
            self.dripSpeedX = dripSpeedX
            self.dripSpeedY = dripSpeedY
            self.gravity = 800.0
            self.dripTime = dripTime
            self.burstSize = burstSize
            self.burstSpeedX = burstSpeedX
            self.burstSpeedY = burstSpeedY
            self.lastUpdate = 0
            self.delta = 0.0

            for i in range(burstSize): self.add_burst(theDisplayable, 0)
            for i in range(numSquirts): self.add_squirt(squirtPower, squirtTime)

        def add_squirt(self, squirtPower, squirtTime):
            angle = random.random() * 6.283
            xSpeed = squirtPower * math.cos(angle)
            ySpeed = squirtPower * math.sin(angle)
            self.squirts.append([xSpeed, ySpeed, squirtTime])

        def add_burst(self, d, startTime):
            s = self.sm.create(d)
            xSpeed = (random.random() - 0.5) * self.burstSpeedX + 20
            ySpeed = (random.random() - 0.75) * self.burstSpeedY + 20
            pTime = self.particleTime
            self.drops.append([s, xSpeed, ySpeed, pTime, startTime])

        def add_drip(self, d, startTime):
            s = self.sm.create(d)
            xSpeed = (random.random() - 0.5) * self.dripSpeedX + 20
            ySpeed = random.random() * self.dripSpeedY + 20
            pTime = self.particleTime
            self.drops.append([s, xSpeed, ySpeed, pTime, startTime])

        def update(self, st):
            delta = st - self.lastUpdate
            self.delta += st - self.lastUpdate
            self.lastUpdate = st

            for squirt in self.squirts[:]:
                if st > squirt[2]:
                    self.squirts.remove(squirt)

            if st < self.dripTime:
                while self.delta * self.density >= 1.0:
                    self.delta -= (1.0 / self.density)
                    if random.random() >= 1 - self.dripChance: self.add_drip(self.displayable, st)
                    for xSpeed, ySpeed, squirtTime in self.squirts:
                        s = self.sm.create(self.displayable)
                        s.x += (random.random() - 0.5) * 5
                        s.y += (random.random() - 0.5) * 5
                        self.drops.append([s, xSpeed + (random.random() - 0.5) * 20, ySpeed + (random.random() - 0.5) * 20, self.particleTime, st])

            for drop in self.drops[:]:
                s, xSpeed, ySpeed, particleTime, startTime = drop
                if (st - startTime < particleTime):
                    s.x += xSpeed * delta
                    s.y += ySpeed * delta
                    drop[2] += self.gravity * delta
                else:
                    s.destroy()
                    self.drops.remove(drop)
            return 0

init python:
    class AnimatedMask(renpy.Displayable):
        def __init__(self, child, mask, maskb, oc, op, moving=True, speed=1.0, frequency=1.0, amount=0.5, **properties):
            super().__init__(**properties)

            self.child = renpy.displayable(child)
            self.mask = renpy.displayable(mask)
            self.maskb = renpy.displayable(maskb)
            self.oc = oc
            self.op = op # This is ramplen for AlphaDissolve
            self.moving = moving
            self.speed = speed
            self.amount = amount
            self.frequency = frequency

        def render(self, width, height, st, at):
            # 1. Calculate the completion value for the dissolve.
            complete = self.oc + math.pow(math.sin(st * self.speed / 8.0), 64.0 * self.frequency) * self.amount
            complete = max(0.0, min(1.0, complete)) # Clamp value between 0.0 and 1.0

            # 2. Create a displayable for the animated mask.
            mask_container = Fixed()
            if self.moving:
                mask_container.add(Transform(self.mask, xpos=((-st * 50) % (width * 2)) - (width * 2)))
                mask_container.add(Transform(self.maskb, xpos=-width / 2.0))
            else:
                mask_container.add(self.mask)
                mask_container.add(self.maskb)

            # 3. Create an AlphaDissolve transition instance for this frame.
            # *** THIS IS THE CORRECTED LINE ***
            transition = AlphaDissolve(mask_container, time=1.0, ramplen=self.op, alpha=True)

            # 4. Create the transition displayable for the current state, manually setting the completion.
            trans_disp = transition(
                old_widget=Solid((0, 0, 0, 0)), # A transparent solid
                new_widget=self.child,
                alpha=complete
            )

            # 5. Render the result of the transition and return it.
            child_render = renpy.render(trans_disp, width, height, st, at)
            
            rv = renpy.Render(width, height)
            rv.blit(child_render, (0,0))
            
            renpy.redraw(self, 0)
            return rv

    def monika_alpha(trans, st, at):
        trans.alpha = math.pow(math.sin(st / 8), 64) * 1.4
        return 0

image blood_particle_drip:
    "gui/blood_drop.png"
    yzoom 0 yanchor 0.2 subpixel True
    linear 10 yzoom 8

image blood_particle:
    subpixel True
    "gui/blood_drop.png"
    zoom 0.75
    alpha 0.75
    choice:
        linear 0.25 zoom 0
    choice:
        linear 0.35 zoom 0
    choice:
        linear 0.35 zoom 0
    choice:
        linear 0.55 zoom 0

image blood:
    size (1, 1)
    truecenter
    Blood("blood_particle").sm

image blood_eye:
    size (1, 1)
    truecenter
    Blood("blood_particle", dripChance=0.5, numSquirts=0).sm

image blood_eye2:
    size (1, 1)
    truecenter
    Blood("blood_particle", dripChance=0.005, numSquirts=0, burstSize=0).sm

image bsod_1:
    "images/bg/bsod.png"
    size (1280,720)
image bsod_2:
    "black"
    0.1
    yoffset 250
    0.1
    yoffset 500
    0.1
    yoffset 750

image bsod = LiveComposite((1280, 720), (0, 0), "bsod_1", (0, 0), "bsod_2")

image veins:
    AnimatedMask("images/bg/veinmask.png", "images/bg/veinmask.png", "images/bg/veinmaskb.png", 0.15, 16, moving=False, speed=10.0, frequency=0.25, amount=0.1)
    xanchor 0.05
    zoom 1.10
    xpos -5
    subpixel True
    parallel:
        ease 2.0 xpos 5
        ease 1.0 xpos 0
        ease 1.0 xpos 5
        ease 2.0 xpos -5
        ease 1.0 xpos 0
        ease 1.0 xpos -5
        repeat
    parallel:
        choice:
            0.6
        choice:
            0.2
        choice:
            0.3
        choice:
            0.4
        choice:
            0.5
        pass
        choice:
            xoffset 0
        choice:
            xoffset 1
        choice:
            xoffset 2
        choice:
            xoffset -1
        choice:
            xoffset -2
        repeat
