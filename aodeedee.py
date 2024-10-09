import flet as ft
import subprocess  # Import subprocess to restart the script
import os  # Import os to handle paths
import time
import random
from solitaire import Solitaire
from dev import save_winner_data

SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 450

def main(page: ft.Page):
    # Enable keyboard event listener
    page.window_event_listener = True
    page.on_keyboard_event = lambda e: print(f"Key pressed: {e.key}")

    # Create an input field for the username and a button to start the game
    username_input = ft.TextField(label="Enter your username", autofocus=True)

    def start_game(e):
        # Get the player's username from the input field
        player_username = username_input.value.strip()
        if player_username:
            # Create the Solitaire game with the player's username and pass the page reference
            solitaire = Solitaire(username=player_username, page=page)
            
            # Clear the page and add the Solitaire game
            page.clean()
            page.add(solitaire)
            
            # Add the "Finish Game" button to the game area
            finish_button = ft.ElevatedButton(
                text="Finish Game",
                on_click=solitaire.finish_game,  # Set the action for the button click
                width=150,
                height=50,
            )
            
            # Create the admin console area and add it below the game area
            admin_console = create_admin_console()
            
            # Add the "Finish Game" button and the admin console to the page
            page.add(
                ft.Column(
                    [
                        finish_button,  # Finish game button
                        admin_console  # Admin console section
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        else:
            page.add(ft.Text("Please enter a username before starting the game.", color="red"))

    def create_admin_console():
        """Create the admin console section below the game area."""
        # Create the "Show Leaderboard" button
        show_leaderboard_button = ft.ElevatedButton(
            text="Show Leaderboard",
            on_click=show_leaderboard,  # Set the action for the leaderboard button
            width=200,
            height=50,
        )

        # Create the "Restart Game" button
        restart_button = ft.ElevatedButton(
            text="Restart Game",
            on_click=restart_game,  # Set the action for the restart button
            width=200,
            height=50,
        )

        # Create a container to act as the admin console area with all buttons
        admin_console_container = ft.Container(
            content=ft.Column(
                controls=[show_leaderboard_button, restart_button],  # Add buttons to the column
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            width=300,
            padding=ft.padding.all(10),
            border=ft.border.all(1, "gray"),
            border_radius=10,
            bgcolor=ft.colors.GREY_100,  # Set background color for the admin console area
        )

        return admin_console_container

    def show_leaderboard(e):
        """Run the leaderboard.py file when the button is clicked."""
        # Get the absolute path of the current script directory
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to leaderboard.py relative to the current directory
        leaderboard_path = os.path.join(current_directory, "leaderboard.py")
        
        try:
            # Run the leaderboard.py file
            subprocess.run(["python", leaderboard_path])
        except Exception as ex:
            print(f"Error running leaderboard.py: {ex}")

    def restart_game(e):
        """Restart the current script (aodeedee.py) to restart the game."""
        # Get the absolute path of the current script
        current_script = os.path.abspath(__file__)
        try:
            # Run the script using subprocess
            subprocess.Popen(["python", current_script])
        except Exception as ex:
            print(f"Error restarting game: {ex}")

    # Display the input field and the button
    page.add(username_input, ft.ElevatedButton("Start Game", on_click=start_game))

ft.app(target=main, assets_dir="assets")
