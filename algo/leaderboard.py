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

# Merge sort function to sort the leaderboard by time
def merge_sort(arr):
    if len(arr) > 1:
        left_arr = arr[:len(arr)//2]
        right_arr = arr[len(arr)//2:]
        
        merge_sort(left_arr)
        merge_sort(right_arr)

        i = 0
        j = 0
        k = 0

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i][1] < right_arr[j][1]:  # Compare by time (second element of the tuple)
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1

# Format time to two decimal places for display
def format_time(seconds):
    return f"{seconds:.2f} seconds"

# Flet UI for the leaderboard
def main(page: ft.Page):
    page.title = "Leaderboard"
    page.scroll = "auto"
    
    # Load leaderboard data and keep only the lowest time for each user
    leaderboard = read_leaderboard_data()
    
    # Sort leaderboard by time using merge_sort
    merge_sort(leaderboard)
    
    # Define a general style for the page
    page.padding = 20
    page.bgcolor = ft.colors.WHITE

    # Header styling
    title = ft.Text(
        "🏆 Leaderboard (Best Times)",
        size=40,
        weight="bold",
        text_align="center",
        color=ft.colors.BLUE_700,
    )
    
    subtitle = ft.Text(
        "See who has the fastest times!",
        size=18,
        italic=True,
        text_align="center",
        color=ft.colors.GREY_500,
    )

    # Create the leaderboard table with added styles
    leaderboard_table = ft.Column(
        spacing=15,  # Add space between the rows
        alignment=ft.MainAxisAlignment.CENTER,  # Center-align the items
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Horizontal alignment of content
    )

    # Add rows to the leaderboard UI
    for idx, (username, seconds) in enumerate(leaderboard, start=1):
        formatted_time = format_time(seconds)
        
        leaderboard_table.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"{idx}. {username}", size=22, weight="bold", color=ft.colors.BLACK87),
                        ft.Text(f"Time: {formatted_time}", size=20, color=ft.colors.GREEN_700),
                    ],
                    alignment="spaceBetween",
                ),
                padding=ft.padding.all(10),
                border_radius=10,
                bgcolor=ft.colors.BLUE_GREY_50,  # Light background for each row
                margin=ft.margin.symmetric(vertical=5),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=5,
                    color=ft.colors.GREY_400,
                    offset=ft.Offset(2, 2),
                ),
            )
        )

    # Footer with a button to return to the main menu (or any other action)
    footer_button = ft.ElevatedButton(
        text="Back to Main Menu",
        width=300,
        height=50,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE_700,
        on_click=lambda e: page.go("/"),  # You can adjust this action
    )

    # Add components to the page
    page.add(
        ft.Column(
            [
                title,
                subtitle,
                leaderboard_table,
                footer_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Center-align all elements vertically
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center-align all elements horizontally
            spacing=20,  # Add spacing between components
        )
    )

# Run the app
if __name__ == "__main__":
    ft.app(target=main)
