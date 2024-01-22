from PIL import ImageGrab
import os

class Screenshot:
    def __init__(self):
        # You can initialize any required variables here
        self.screenshot = ImageGrab.grab()

    def store(self, filename):
        # Resize the screenshot to 1080p
        resized_screenshot = self.screenshot.resize((1920, 1080))

        # Save the resized screenshot
        resized_screenshot.save(filename, format="PNG")

        print(f"Screenshot saved as {filename} at 1080p resolution")
        
