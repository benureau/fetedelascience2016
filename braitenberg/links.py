class Link:
    """A link joins a pre and post-plug, and transmit a weighted activation."""

    def __init__(self, pre, post, w0=1.0):
        """Link between pre and post plugs"""
        self.pre  = pre
        self.post = post
        self.w    = w0

    def step(self):
        """Transmit activation from the pre to the post plug."""
        self.post.receive(self.w * self.pre.act)

    def draw(self):
        """Draw the link. Assumes world coordinates."""
        x1, y1, a1 = self.pre.world_pos()
        x2, y2, a2 = self.post.world_pos()

        stroke(0)
        noFill()
        bezier(x1, y1, x1 + self.pre.bend  * cos(a1), y1 + self.pre.bend * sin(a1),
                       x2 + self.post.bend * cos(a2), y2 + self.post.bend * sin(a2), x2, y2)


class Plug:
    """A small positional object to connect stuff aesthetically."""

    def __init__(self, parent, x, y, angle=0.0, bend=20.0):
        self.parent    = parent
        self.x, self.y = x, y
        self.angle     = angle
        self.bend      = bend

    def world_pos(self):
        """Return the world position of the plug."""
        px, py, pangle = self.parent.world_pos()
        dx, dy = ( self.x * cos(-pangle) + self.y * sin(-pangle),
                  -self.x * sin(-pangle) + self.y * cos(-pangle))
        return px + dx, py + dy, pangle + self.angle

    @property
    def act(self):
        return self.parent.act

    def receive(self, act):
        return self.parent.receive(act)
