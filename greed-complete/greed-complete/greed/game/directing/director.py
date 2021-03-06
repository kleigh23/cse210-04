from game.casting.cast import Cast
class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

#this stays the same - cristian
    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self.score = 0


#this stays the same - cristian
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()


#this stays the same - cristian
    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")
        velocity = self._keyboard_service.get_direction()
        art_velocity = self._keyboard_service.move_direction()
        robot.set_velocity(velocity)
        for artifact in artifacts: 
            artifact.set_velocity(art_velocity)


#this changes
    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        #the guy youre using, only moves right and left-- the gem catcher - cristian
        robot = cast.get_first_actor("robots")
        #these are meant to be moving too
        artifacts = cast.get_actors("artifacts")

        # banner.set_text("")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)

        #for loop to display the massege of the score when the robot has the same position as the gem or rock.
        for artifact in artifacts:
            artifact.move_next(max_x, max_y)
            if robot.get_position().equals(artifact.get_position()):
                if artifact.get_text() == "*":
                    message = artifact.get_message()
                    self.score += message
                    banner.set_text(f"Score: {self.score}")
                    # added this!!! it removes the artifacts when we touch them
                    cast.remove_actor("artifacts", artifact) 
                elif artifact.get_text() == "o":
                    message = artifact.get_message()
                    self.score -= message
                    banner.set_text(f"Score: {self.score}")
                    cast.remove_actor("artifact", artifact)
                    if self.score < 0:
                        self.score = 0
                        banner.set_text(f"Score: {self.score}")

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()