from manim import *

class GeneratedScene(Scene):
    def construct(self):
        circle = Circle().scale(1.3).set_color(RED)
        square = Square().scale(1.5).set_color(YELLOW)
        self.play(FadeIn(circle))
        self.play(ReplacementTransform(circle, square))
        self.wait(2)