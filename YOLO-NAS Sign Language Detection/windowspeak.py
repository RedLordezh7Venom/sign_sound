import pygetwindow as gw
import pyautogui
import pyttsx3
import pytesseract

def read_and_speak(window_title):
    try:
        # Get the window by title
        window = gw.getWindowsWithTitle(window_title)[0]

        # Activate the window
        window.activate()

        # Get window dimensions
        left, top, width, height = window.left, window.top, window.width, window.height

        # Capture the entire window
        screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # Extract text from the screenshot using pytesseract
        text_from_window = pytesseract.image_to_string(screenshot)

        # Speak the extracted text
        engine = pyttsx3.init()
        engine.say(text_from_window)
        engine.runAndWait()

    except IndexError:
        print(f"Window with title '{window_title}' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Specify the window title
    window_title = "ChatGPT"

    # Read and speak text from the specified window
    read_and_speak(window_title)
