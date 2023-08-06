from arcade import *
def Bindows():

	SCREEN_WIDTH = 600
	SCREEN_HEIGHT = 600

	SCREEN_TITLE = "Bindows"

	computer_state = 0

	class Windows(arcade.Window):
		def __init__(self, width, height, title):
			super().__init__(width, height, title)
			self.setup()

		def setup(self):
			set_background_color(color.WHITE)

		def on_draw(self):
			start_render()

		def on_update(self, delta_time: float):
			pass


	Bindows = Windows(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	run()