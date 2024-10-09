import flet as ft
import os

# Function to read the leaderboard data from the txt file and keep only the lowest time for each user
def read_leaderboard_data():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "player_data.txt")
    leaderboard = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line:  # Check if the line is not empty
                    try:
                        # Split the line to extract username and time
                        parts = line.split(",")
                        username = parts[0].strip()
                        time_str = parts[1].strip().replace(" seconds", "")
                        time_in_seconds = float(time_str)
                        
                        # If username is already in leaderboard, keep the lowest time
                        if username in leaderboard:
                            leaderboard[username] = min(leaderboard[username], time_in_seconds)
                        else:
                            leaderboard[username] = time_in_seconds
                    except (ValueError, IndexError):
                        print(f"Error parsing line: {line}")
    except Exception as e:
        print(f"Error reading file: {e}")
    return list(leaderboard.items())

# Format time to two decimal places for display
def format_time(seconds):
    return f"{seconds:.2f} seconds"

# Flet UI for the leaderboard
def main(page: ft.Page):
    page.title = "Leaderboard"
    page.scroll = "auto"
    
    # Load leaderboard data and keep only the lowest time for each user
    leaderboard = read_leaderboard_data()
    
    # Sort leaderboard by time (ascending) since lower seconds is better
    leaderboard.sort(key=lambda x: x[1])
    
    # UI Components
    title = ft.Text("Leaderboard (Best Times)", size=30, weight="bold", text_align="center")
    leaderboard_table = ft.Column()

    # Add rows to the leaderboard UI
    for idx, (username, seconds) in enumerate(leaderboard, start=1):
        formatted_time = format_time(seconds)
        leaderboard_table.controls.append(
            ft.Row(
                controls=[
                    ft.Text(f"{idx}. {username}", size=20),
                    ft.Text(f"Time: {formatted_time}", size=20, weight="bold"),
                ],
                alignment="spaceBetween",
            )
        )
    
    # Add components to the page
    page.add(title, leaderboard_table)

# Run the app
if __name__ == "__main__":
    ft.app(target=main)
