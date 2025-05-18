from manim import *

class GeneratedScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        face_grids = []
        grid_size = 6  # Number of small squares per row/column on each face
        cube_size = 2  # Medium-sized cube

        square_size = cube_size / grid_size

        # Define positions and rotations for cube faces
        face_configs = [
            {"pos": (0, 0, cube_size/2), "rot": (0, 0, 0)},                  # Front
            {"pos": (0, 0, -cube_size/2), "rot": (0, PI, 0)},                # Back
            {"pos": (0, cube_size/2, 0), "rot": (-PI/2, 0, 0)},              # Top
            {"pos": (0, -cube_size/2, 0), "rot": (PI/2, 0, 0)},              # Bottom
            {"pos": (cube_size/2, 0, 0), "rot": (0, -PI/2, 0)},              # Right
            {"pos": (-cube_size/2, 0, 0), "rot": (0, PI/2, 0)},              # Left
        ]

        for config in face_configs:
            squares = VGroup()
            for i in range(grid_size):
                for j in range(grid_size):
                    square = Square(
                        side_length=square_size,
                        fill_color=BLUE,
                        fill_opacity=0.8,
                        stroke_width=0.1
                    )
                    square.move_to(np.array([
                        (i - grid_size/2 + 0.5) * square_size,
                        (j - grid_size/2 + 0.5) * square_size,
                        0
                    ]))
                    squares.add(square)

            # Create face group and rotate to correct orientation
            face_group = VGroup(*squares)
            face_group.rotate(config["rot"][0], axis=RIGHT)
            face_group.rotate(config["rot"][1], axis=UP)
            face_group.rotate(config["rot"][2], axis=OUT)
            face_group.move_to(config["pos"])

            # Hide initial squares above scene (z = 5) and store final position
            for square in squares:
                final_pos = square.get_center()
                square.move_to([final_pos[0], final_pos[1], 5])  # Start from above camera view
                face_grids.append((square, final_pos))
                self.add(square)

        # Animate all tiles falling into place
        animations = [sq.animate.move_to(final_pos) for sq, final_pos in face_grids]
        self.play(AnimationGroup(*animations, lag_ratio=0.01, run_time=3))

        # Rotate cube slowly
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)

        
