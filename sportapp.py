import flet as ft
import requests
import json
from datetime import datetime
from login import show_login

API_URL = "http://192.168.100.5:3500"

# Global data storage
all_teams = []
all_athletes = []
all_sports = []
all_matches = []
all_medals = []
all_leaderboard = []

current_page_state = {"page": None}
current_user = {"username": None, "user_id": None, "is_authenticated": False}

def update_layout_for_size(page):
    """Update layout based on current window size and orientation"""
    width = None
    height = None
    
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    # Set default values if window dimensions are not available
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    # Determine if landscape or portrait
    is_landscape = width > height

    # Store current orientation for use in page functions
    page.is_landscape = is_landscape
    page.window_width = width
    page.window_height = height

    # If we have a current page function, refresh it
    if hasattr(page, 'current_page_function') and page.current_page_function:
        page.current_page_function()
        page.update()

# ================== HELPER FUNCTIONS ==================

def get_team_name(team_id):
    """Get team name by ID from global all_teams"""
    for team in all_teams:
        if team.get('id') == team_id:
            return team.get('team_name', f'Team {team_id}')
    return f'Team {team_id}'

def get_sport_name(sport_id):
    """Get sport name by ID from global all_sports"""
    for sport in all_sports:
        if sport.get('id') == sport_id:
            return sport.get('sport_name', f'Sport {sport_id}')
    return f'Sport {sport_id}'

# ================== API FUNCTIONS ==================

def fetch_teams():
    try:
        res = requests.get(f"{API_URL}/teams", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error: {e}")
    return []

def fetch_athletes():
    try:
        res = requests.get(f"{API_URL}/athletes", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error: {e}")
    return []

def fetch_sports():
    try:
        res = requests.get(f"{API_URL}/sports", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error: {e}")
    return []

def fetch_matches():
    try:
        res = requests.get(f"{API_URL}/matches", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error: {e}")
    return []

def fetch_medals():
    try:
        res = requests.get(f"{API_URL}/medals", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error: {e}")
    return []

def fetch_leaderboard():
    try:
        res = requests.get(f"{API_URL}/leaderboard", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Error: {e}")
    return []


def _get_match_datetime(match):
    try:
        dt = match.get('match_date', '')
        tm = match.get('match_time', '')
        if dt and tm:
            return datetime.fromisoformat(f"{dt}T{tm}")
        if dt:
            return datetime.fromisoformat(dt)
    except Exception:
        pass
    return datetime.max

# ================== TEAMS PAGE

def build_team_cards(teams, page):
    cards = []
    for team in teams:
        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(team.get("team_name", "No name"), size=14, weight=ft.FontWeight.BOLD, color="#000000", max_lines=2),
                ],
                spacing=8,
            ),
            width=160,
            padding=10,
            bgcolor="#E3F2FD",
            border_radius=10,
            on_click=lambda e, t=team: show_team_detail(page, t),
        )
        cards.append(card)
    return cards

def build_team_cards_edit(teams, page):
    """Build team cards with edit and delete buttons for Edit Center"""
    cards = []
    for team in teams:
        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(team.get("team_name", "No name"), size=14, weight=ft.FontWeight.BOLD, color="#000000", max_lines=2),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Edit", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=45,
                                height=30,
                                bgcolor="#4CAF50",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, t=team: show_team_form_edit(page, t),
                            ),
                            ft.Container(
                                content=ft.Text("Delete", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=50,
                                height=30,
                                bgcolor="#f44336",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, t=team: delete_team(page, t['id'], is_edit=True),
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=8,
            ),
            width=160,
            padding=10,
            bgcolor="#E3F2FD",
            border_radius=10,
        )
        cards.append(card)
    return cards

def show_teams(page):
    """แสดงหน้าทีม"""
    if hasattr(page, 'navigation_bar') and page.navigation_bar is not None:
        page.navigation_bar.selected_index = 2
    page.clean()

    global all_teams
    all_teams = fetch_teams()

    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height

    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)

    is_landscape = width > height

    # Responsive layout
    if is_landscape:
        container_width = width
        container_height = height - 120
        card_width = 120  # Smaller cards in landscape
        cols = max(1, int(container_width / 150))  # More columns in landscape
    else:
        container_width = width
        container_height = height - 120
        card_width = 160
        cols = max(1, int(container_width / 180))

    # ---------- HEADER ----------
    header = ft.Text("Teams", size=24, weight=ft.FontWeight.BOLD, color="#1976d2")

    header_row = ft.Row([header], spacing=10)

    teams_row = ft.Row(wrap=True, spacing=10, run_spacing=10)
    teams_row.controls = build_team_cards(all_teams, page)

    main_container = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.Container(
                    content=ft.ListView([teams_row], expand=True),
                    width=container_width,
                    expand=True,
                ),
            ],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )

    page.add(
        ft.Container(
            content=ft.Row(
                [main_container],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

    # Store current page function for responsive updates
    page.current_page_function = lambda: show_teams(page)

def show_team_form(page, team):
    """แสดงฟอร์มเพิ่ม/แก้ไขทีม (normal version - returns to show_teams)"""
    page.clean()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    if is_landscape:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    else:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    
    team_name = ft.TextField(
        label="Team Name",
        width=text_width,
        value=team.get("team_name", "") if team else "",
    )
    
    def on_submit(e):
        if not team_name.value.strip():
            show_alert(page, "Please enter team name")
            return
        
        try:
            if team:
                # Update
                requests.put(
                    f"{API_URL}/teams/{team['id']}",
                    json={"team_name": team_name.value},
                    timeout=5
                )
            else:
                # Create
                requests.post(
                    f"{API_URL}/teams",
                    json={"team_name": team_name.value},
                    timeout=5
                )
            show_teams(page)
        except Exception as ex:
            show_alert(page, f"Error: {str(ex)}")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_teams(page),
    )
    
    submit_btn = ft.Container(
        content=ft.Text("Save", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=on_submit,
    )
    
    header_row = ft.Row([ft.Text(f"{'Edit' if team else 'Add'} Team", size=20, weight=ft.FontWeight.BOLD), ft.Container(expand=True), submit_btn, back_btn], spacing=10)
    
    container = ft.Container(
        content=ft.Column(
            [header_row, team_name, ft.Container(expand=True)],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(container)

def show_team_form_edit(page, team):
    """แสดงฟอร์มเพิ่ม/แก้ไขทีม (edit version - returns to show_teams_edit)"""
    page.clean()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    if is_landscape:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    else:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    
    team_id_field = ft.TextField(
        label="Team ID",
        width=text_width,
        value=str(team.get("id", "")) if team else "",
        read_only=True,
        visible=team is not None,
    )
    
    team_name = ft.TextField(
        label="Team Name",
        width=text_width,
        value=team.get("team_name", "") if team else "",
    )
    
    def on_submit(e):
        if not team_name.value.strip():
            show_alert(page, "Please enter team name")
            return
        
        try:
            if team:
                # Update
                requests.put(
                    f"{API_URL}/teams/{team['id']}",
                    json={"team_name": team_name.value},
                    timeout=5
                )
            else:
                # Create
                requests.post(
                    f"{API_URL}/teams",
                    json={"team_name": team_name.value},
                    timeout=5
                )
            show_teams_edit(page)
        except Exception as ex:
            show_alert(page, f"Error: {str(ex)}")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_teams_edit(page),
    )
    
    submit_btn = ft.Container(
        content=ft.Text("Save", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=on_submit,
    )
    
    header_row = ft.Row([ft.Text(f"{'Edit' if team else 'Add'} Team", size=20, weight=ft.FontWeight.BOLD), ft.Container(expand=True), submit_btn, back_btn], spacing=10)
    
    container = ft.Container(
        content=ft.Column(
            [header_row, team_id_field, team_name, ft.Container(expand=True)],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(container)

def show_team_detail(page, team):
    """แสดงรายละเอียดทีม พร้อมรายชื่อสมาชิก"""
    page.clean()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    if is_landscape:
        container_width = width
        container_height = height - 100
    else:
        container_width = width
        container_height = height - 100

    global all_athletes
    all_athletes = fetch_athletes()
    team_members = [a for a in all_athletes if a.get('team_id') == team.get('id')]

    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_teams(page),
    )

    member_list = ft.Column(spacing=5)
    if team_members:
        for m in team_members:
            member_list.controls.append(ft.Text(f"• {m.get('first_name','')} {m.get('last_name','')}", size=12))
    else:
        member_list.controls.append(ft.Text("No members found", size=12, color="#999999"))

    detail = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Team ID: {team.get('id', '-')}", size=14, color="#666666"),
                ft.Text(team.get("team_name", "No name"), size=18, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Divider(),
                ft.Text("Members", size=16, weight=ft.FontWeight.BOLD),
                member_list,
                ft.Divider(),
                back_btn,
            ],
            spacing=10,
        ),
        width=container_width,
        height=container_height,
        padding=15,
        bgcolor="white",
    )

    page.add(detail)

def show_teams_edit(page):
    """แสดงหน้าแก้ไขทีม (สำหรับ Edit Center)"""
    page.clean()
    
    global all_teams
    all_teams = fetch_teams()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    # Responsive layout
    if is_landscape:
        container_width = width
        container_height = height - 120
    else:
        container_width = width
        container_height = height - 120
    
    # ---------- HEADER ----------
    header = ft.Text("Teams", size=24, weight=ft.FontWeight.BOLD, color="#1976d2")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_edit_page(page),
    )
    
    add_btn = ft.Container(
        content=ft.Text("Add", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_team_form_edit(page, None),
    )
    
    header_row = ft.Row([header, ft.Container(expand=True), add_btn, back_btn], spacing=10)
    
    teams_row = ft.Row(wrap=True, spacing=10, run_spacing=10)
    teams_row.controls = build_team_cards_edit(all_teams, page)
    
    main_container = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.Container(
                    content=ft.ListView([teams_row], expand=True),
                    width=container_width,
                    expand=True,
                ),
            ],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(
        ft.Container(
            content=ft.Row(
                [main_container],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

    # Store current page function for responsive updates
    page.current_page_function = lambda: show_teams_edit(page)

def delete_team(page, team_id, is_edit=False):
    """ลบทีม"""
    try:
        requests.delete(f"{API_URL}/teams/{team_id}", timeout=5)
        if is_edit:
            show_teams_edit(page)
        else:
            show_teams(page)
    except Exception as e:
        show_alert(page, f"Error: {str(e)}")

# ================== ATHLETES PAGE ==================

def build_athlete_cards(athletes, page):
    cards = []
    for athlete in athletes:
        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"ID: {athlete.get('id', '-')}", size=10, color="#999999"),
                    ft.Text(f"{athlete.get('first_name', '')} {athlete.get('last_name', '')}", size=13, weight=ft.FontWeight.BOLD, color="#000000", max_lines=2),
                    ft.Text(f"Team: {athlete.get('team_id', '-')}", size=10, color="#666666"),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Edit", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=45,
                                height=30,
                                bgcolor="#4CAF50",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, a=athlete: show_athlete_form(page, a),
                            ),
                            ft.Container(
                                content=ft.Text("Delete", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=50,
                                height=30,
                                bgcolor="#f44336",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, a=athlete: delete_athlete(page, a['id']),
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=5,
            ),
            width=160,
            padding=10,
            bgcolor="#F3E5F5",
            border_radius=10,
        )
        cards.append(card)
    return cards

def show_athletes(page):
    """แสดงหน้านักกีฬา"""
    page.clean()
    
    global all_athletes
    all_athletes = fetch_athletes()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    # Responsive layout
    if is_landscape:
        container_width = width
        container_height = height - 120
    else:
        container_width = width
        container_height = height - 120
    
    header = ft.Text("Athletes", size=24, weight=ft.FontWeight.BOLD, color="#7b1fa2")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_edit_page(page),
    )
    
    add_btn = ft.Container(
        content=ft.Text("Add", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_athlete_form(page, None),
    )
    
    header_row = ft.Row([header, ft.Container(expand=True), add_btn, back_btn], spacing=10)
    
    athletes_row = ft.Row(wrap=True, spacing=10, run_spacing=10)
    athletes_row.controls = build_athlete_cards(all_athletes, page)
    
    main_container = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.Container(
                    content=ft.ListView([athletes_row], expand=True),
                    width=container_width,
                    expand=True,
                ),
            ],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(
        ft.Container(
            content=ft.Row(
                [main_container],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

    # Store current page function for responsive updates
    page.current_page_function = lambda: show_athletes(page)

def show_athlete_form(page, athlete):
    """แสดงฟอร์มเพิ่ม/แก้ไขนักกีฬา"""
    page.clean()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    if is_landscape:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    else:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    
    first_name = ft.TextField(
        label="First Name",
        width=text_width,
        value=athlete.get("first_name", "") if athlete else "",
    )
    last_name = ft.TextField(
        label="Last Name",
        width=text_width,
        value=athlete.get("last_name", "") if athlete else "",
    )
    team_id = ft.TextField(
        label="Team ID",
        width=text_width,
        value=str(athlete.get("team_id", "")) if athlete else "",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    
    def on_submit(e):
        if not first_name.value.strip() or not last_name.value.strip() or not team_id.value.strip():
            show_alert(page, "Please fill all fields")
            return
        
        try:
            data = {
                "first_name": first_name.value,
                "last_name": last_name.value,
                "team_id": int(team_id.value),
            }
            if athlete:
                requests.put(f"{API_URL}/athletes/{athlete['id']}", json=data, timeout=5)
            else:
                requests.post(f"{API_URL}/athletes", json=data, timeout=5)
            show_athletes(page)
        except Exception as ex:
            show_alert(page, f"Error: {str(ex)}")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_athletes(page),
    )
    
    submit_btn = ft.Container(
        content=ft.Text("Save", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=on_submit,
    )
    
    header_row = ft.Row([ft.Text(f"{'Edit' if athlete else 'Add'} Athlete", size=20, weight=ft.FontWeight.BOLD), ft.Container(expand=True), submit_btn, back_btn], spacing=10)
    
    container = ft.Container(
        content=ft.Column(
            [header_row, first_name, last_name, team_id, ft.Container(expand=True)],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(container)

def delete_athlete(page, athlete_id):
    """ลบนักกีฬา"""
    try:
        requests.delete(f"{API_URL}/athletes/{athlete_id}", timeout=5)
        show_athletes(page)
    except Exception as e:
        show_alert(page, f"Error: {str(e)}")

# ================== SPORTS PAGE ==================

def build_sport_cards(sports, page):
    cards = []
    for sport in sports:
        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"Sport #{sport.get('id', '-')}", size=10, color="#999999"),
                    ft.Text(sport.get("sport_name", "No name"), size=14, weight=ft.FontWeight.BOLD, color="#000000", max_lines=2),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Edit", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=45,
                                height=30,
                                bgcolor="#4CAF50",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, s=sport: show_sport_form(page, s),
                            ),
                            ft.Container(
                                content=ft.Text("Delete", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=50,
                                height=30,
                                bgcolor="#f44336",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, s=sport: delete_sport(page, s['id']),
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=8,
            ),
            width=160,
            padding=10,
            bgcolor="#FCE4EC",
            border_radius=10,
        )
        cards.append(card)
    return cards

def show_sports(page):
    """แสดงหน้ากีฬา"""
    page.clean()
    
    global all_sports
    all_sports = fetch_sports()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    # Responsive layout
    if is_landscape:
        container_width = width
        container_height = height - 120
    else:
        container_width = width
        container_height = height - 120
    
    header = ft.Text("Sports", size=24, weight=ft.FontWeight.BOLD, color="#c2185b")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_edit_page(page),
    )
    
    add_btn = ft.Container(
        content=ft.Text("Add", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_sport_form(page, None),
    )
    
    header_row = ft.Row([header, ft.Container(expand=True), add_btn, back_btn], spacing=10)
    
    sports_row = ft.Row(wrap=True, spacing=10, run_spacing=10)
    sports_row.controls = build_sport_cards(all_sports, page)
    
    main_container = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.Container(
                    content=ft.ListView([sports_row], expand=True),
                    width=container_width,
                    expand=True,
                ),
            ],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(
        ft.Container(
            content=ft.Row(
                [main_container],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

    # Store current page function for responsive updates
    page.current_page_function = lambda: show_sports(page)

def show_sport_form(page, sport):
    """แสดงฟอร์มเพิ่ม/แก้ไขกีฬา"""
    page.clean()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    if is_landscape:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    else:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    
    sport_name = ft.TextField(
        label="Sport Name",
        width=text_width,
        value=sport.get("sport_name", "") if sport else "",
    )
    
    # ID field for editing (read-only)
    sport_id_field = ft.TextField(
        label="Sport ID",
        width=text_width,
        value=str(sport.get("id", "")) if sport else "",
        read_only=True,
        visible=sport is not None,
    )
    
    def on_submit(e):
        if not sport_name.value.strip():
            show_alert(page, "Please enter sport name")
            return
        
        try:
            if sport:
                requests.put(
                    f"{API_URL}/sports/{sport['id']}",
                    json={"sport_name": sport_name.value},
                    timeout=5
                )
            else:
                requests.post(
                    f"{API_URL}/sports",
                    json={"sport_name": sport_name.value},
                    timeout=5
                )
            show_sports(page)
        except Exception as ex:
            show_alert(page, f"Error: {str(ex)}")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_sports(page),
    )
    
    submit_btn = ft.Container(
        content=ft.Text("Save", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=on_submit,
    )
    
    header_row = ft.Row([ft.Text(f"{'Edit' if sport else 'Add'} Sport", size=20, weight=ft.FontWeight.BOLD), ft.Container(expand=True), submit_btn, back_btn], spacing=10)
    
    container = ft.Container(
        content=ft.Column(
            [header_row, sport_id_field, sport_name, ft.Container(expand=True)],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(container)

def delete_sport(page, sport_id):
    """ลบกีฬา"""
    try:
        requests.delete(f"{API_URL}/sports/{sport_id}", timeout=5)
        show_sports(page)
    except Exception as e:
        show_alert(page, f"Error: {str(e)}")

# ================== MATCHES PAGE ==================

def build_match_cards(matches, page):
    cards = []
    for match in matches:
        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"Match #{match.get('id', '-')}", size=10, color="#999999"),
                    ft.Text(f"Sport: {match.get('sport_id', '-')}", size=10, color="#666666"),
                    ft.Text(f"Team A: {match.get('team_a_id', '-')} vs Team B: {match.get('team_b_id', '-')}", size=11, weight=ft.FontWeight.BOLD, color="#000000"),
                    ft.Text(f"{match.get('match_date', '')} {match.get('match_time', '')}", size=9, color="#666666"),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Edit", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=45,
                                height=30,
                                bgcolor="#4CAF50",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, m=match: show_match_form(page, m),
                            ),
                            ft.Container(
                                content=ft.Text("Delete", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=50,
                                height=30,
                                bgcolor="#f44336",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, m=match: delete_match(page, m['id']),
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=5,
            ),
            width=160,
            padding=10,
            bgcolor="#E8F5E9",
            border_radius=10,
        )
        cards.append(card)
    return cards

def show_matches(page):
    """แสดงหน้าแข่งขัน (จัดระเบียบตามกีฬา)"""
    if hasattr(page, 'navigation_bar') and page.navigation_bar is not None:
        page.navigation_bar.selected_index = 1
    page.clean()

    global all_matches, all_sports, all_teams
    all_matches = sorted(
        fetch_matches(),
        key=lambda m: _get_match_datetime(m)
    )
    all_sports = fetch_sports()
    all_teams = fetch_teams()

    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    # Responsive layout
    if is_landscape:
        container_width = width
        container_height = height - 120
    else:
        container_width = width
        container_height = height - 120

    header = ft.Text("Matches", size=24, weight=ft.FontWeight.BOLD, color="#2e7d32")

    header_row = ft.Row([header], spacing=10)

    matches_list = ft.Column(spacing=10)
    
    # Group matches by sport
    matches_by_sport = {}
    for match in all_matches:
        sport_id = match.get('sport_id')
        if sport_id not in matches_by_sport:
            matches_by_sport[sport_id] = []
        matches_by_sport[sport_id].append(match)
    
    # Display matches organized by sport
    for sport_id in sorted(matches_by_sport.keys()):
        sport_name = get_sport_name(sport_id)
        matches_list.controls.append(
            ft.Text(f"🏆 {sport_name}", size=14, weight=ft.FontWeight.BOLD, color="#2e7d32")
        )
        
        for match in matches_by_sport[sport_id]:
            team_a_name = get_team_name(match.get('team_a_id'))
            team_b_name = get_team_name(match.get('team_b_id'))
            
            matches_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"{team_a_name} vs {team_b_name}", size=12, weight=ft.FontWeight.BOLD, color="#000000"),
                            ft.Text(f"{match.get('match_date','-')} {match.get('match_time','-')}", size=10, color="#666666"),
                        ],
                        spacing=3,
                    ),
                    padding=10,
                    bgcolor="#F1F8E9",
                    border_radius=5,
                    margin=ft.Margin.only(left=15),
                )
            )

    main_container = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.Container(
                    content=ft.ListView([matches_list], expand=True),
                    width=container_width,
                    expand=True,
                ),
            ],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )

    page.add(
        ft.Container(
            content=ft.Row(
                [main_container],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

    # Store current page function for responsive updates
    page.current_page_function = lambda: show_matches(page)


def show_matches_edit(page):
    """แสดงหน้าจัดการแข่งขัน (Edit Center)"""
    page.clean()

    global all_matches
    all_matches = fetch_matches()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    # Responsive layout
    if is_landscape:
        container_width = width
        container_height = height - 120
    else:
        container_width = width
        container_height = height - 120

    header = ft.Text("Matches", size=24, weight=ft.FontWeight.BOLD, color="#2e7d32")

    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_edit_page(page),
    )

    add_btn = ft.Container(
        content=ft.Text("Add", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_match_form(page, None),
    )

    header_row = ft.Row([header, ft.Container(expand=True), add_btn, back_btn], spacing=10)

    matches_row = ft.Row(wrap=True, spacing=10, run_spacing=10)
    matches_row.controls = build_match_cards(all_matches, page)

    main_container = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.Container(
                    content=ft.ListView([matches_row], expand=True),
                    width=container_width,
                    expand=True,
                ),
            ],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )

    page.add(
        ft.Container(
            content=ft.Row(
                [main_container],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

    # Store current page function for responsive updates
    page.current_page_function = lambda: show_matches_edit(page)


def show_match_form(page, match):
    """แสดงฟอร์มเพิ่ม/แก้ไขแข่งขัน"""
    page.clean()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    if is_landscape:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    else:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    
    sport_id = ft.TextField(
        label="Sport ID",
        width=text_width,
        value=str(match.get("sport_id", "")) if match else "",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    
    # ID field for editing (read-only)
    match_id_field = ft.TextField(
        label="Match ID",
        width=text_width,
        value=str(match.get("id", "")) if match else "",
        read_only=True,
        visible=match is not None,
    )
    team_a_id = ft.TextField(
        label="Team A ID",
        width=text_width,
        value=str(match.get("team_a_id", "")) if match else "",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    team_b_id = ft.TextField(
        label="Team B ID",
        width=text_width,
        value=str(match.get("team_b_id", "")) if match else "",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    match_date = ft.TextField(
        label="Match Date (YYYY-MM-DD)",
        width=text_width,
        value=match.get("match_date", "") if match else "",
    )
    match_time = ft.TextField(
        label="Match Time (HH:MM)",
        width=text_width,
        value=match.get("match_time", "") if match else "",
    )
    
    def on_submit(e):
        if not all([sport_id.value, team_a_id.value, team_b_id.value, match_date.value, match_time.value]):
            show_alert(page, "Please fill all fields")
            return
        
        try:
            data = {
                "sport_id": int(sport_id.value),
                "team_a_id": int(team_a_id.value),
                "team_b_id": int(team_b_id.value),
                "match_date": match_date.value,
                "match_time": match_time.value,
            }
            if match:
                requests.put(f"{API_URL}/matches/{match['id']}", json=data, timeout=5)
            else:
                requests.post(f"{API_URL}/matches", json=data, timeout=5)
            show_matches(page)
        except Exception as ex:
            show_alert(page, f"Error: {str(ex)}")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_matches(page),
    )
    
    submit_btn = ft.Container(
        content=ft.Text("Save", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=on_submit,
    )
    
    header_row = ft.Row([ft.Text(f"{'Edit' if match else 'Add'} Match", size=20, weight=ft.FontWeight.BOLD), ft.Container(expand=True), submit_btn, back_btn], spacing=10)
    
    container = ft.Container(
        content=ft.Column(
            [header_row, match_id_field, sport_id, team_a_id, team_b_id, match_date, match_time, ft.Container(expand=True)],
            spacing=10,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(container)

def delete_match(page, match_id):
    """ลบแข่งขัน"""
    try:
        requests.delete(f"{API_URL}/matches/{match_id}", timeout=5)
        show_matches(page)
    except Exception as e:
        show_alert(page, f"Error: {str(e)}")

# ================== MEDALS PAGE ==================

def build_medal_cards(medals, page):
    cards = []
    for medal in medals:
        card = ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"Medal #{medal.get('id', '-')}", size=10, color="#999999"),
                    ft.Text(f"Team: {medal.get('team_id', '-')} | Sport: {medal.get('sport_id', '-')}", size=10, color="#666666"),
                    ft.Text(f"🥇 {medal.get('gold_count', 0)} 🥈 {medal.get('silver_count', 0)} 🥉 {medal.get('bronze_count', 0)}", size=12, weight=ft.FontWeight.BOLD, color="#000000"),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Edit", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=45,
                                height=30,
                                bgcolor="#4CAF50",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, m=medal: show_medal_form(page, m),
                            ),
                            ft.Container(
                                content=ft.Text("Delete", size=10, color="white", weight=ft.FontWeight.BOLD),
                                width=50,
                                height=30,
                                bgcolor="#f44336",
                                border_radius=5,
                                alignment=ft.Alignment(0, 0),
                                on_click=lambda e, m=medal: delete_medal(page, m['id']),
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=5,
            ),
            width=160,
            padding=10,
            bgcolor="#FFF3E0",
            border_radius=10,
        )
        cards.append(card)
    return cards

def show_medals(page):
    """แสดงหน้าเหรียญ"""
    page.clean()
    
    global all_medals
    all_medals = fetch_medals()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    # Responsive layout
    if is_landscape:
        container_width = width
        container_height = height - 120
    else:
        container_width = width
        container_height = height - 120
    
    header = ft.Text("Medals", size=24, weight=ft.FontWeight.BOLD, color="#f57f17")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_edit_page(page),
    )
    
    add_btn = ft.Container(
        content=ft.Text("Add", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_medal_form(page, None),
    )
    
    header_row = ft.Row([header, ft.Container(expand=True), add_btn, back_btn], spacing=10)
    
    medals_row = ft.Row(wrap=True, spacing=10, run_spacing=10)
    medals_row.controls = build_medal_cards(all_medals, page)
    
    main_container = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.Container(
                    content=ft.ListView([medals_row], expand=True),
                    width=container_width,
                    expand=True,
                ),
            ],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(
        ft.Container(
            content=ft.Row(
                [main_container],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

    # Store current page function for responsive updates
    page.current_page_function = lambda: show_medals(page)

def show_medal_form(page, medal):
    """แสดงฟอร์มเพิ่ม/แก้ไขเหรียญ"""
    page.clean()
    
    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height
    
    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)
    
    is_landscape = width > height
    
    if is_landscape:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    else:
        container_width = width
        container_height = height - 100
        text_width = min(300, container_width - 40)
    
    team_id = ft.TextField(
        label="Team ID",
        width=text_width,
        value=str(medal.get("team_id", "")) if medal else "",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    
    # ID field for editing (read-only)
    medal_id_field = ft.TextField(
        label="Medal ID",
        width=text_width,
        value=str(medal.get("id", "")) if medal else "",
        read_only=True,
        visible=medal is not None,
    )
    sport_id = ft.TextField(
        label="Sport ID",
        width=text_width,
        value=str(medal.get("sport_id", "")) if medal else "",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    gold_count = ft.TextField(
        label="Gold Count",
        width=text_width,
        value=str(medal.get("gold_count", "")) if medal else "",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    silver_count = ft.TextField(
        label="Silver Count",
        width=text_width,
        value=str(medal.get("silver_count", "")) if medal else "",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    bronze_count = ft.TextField(
        label="Bronze Count",
        width=text_width,
        value=str(medal.get("bronze_count", "")) if medal else "",
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    
    def on_submit(e):
        if not all([team_id.value, sport_id.value, gold_count.value, silver_count.value, bronze_count.value]):
            show_alert(page, "Please fill all fields")
            return
        
        try:
            data = {
                "team_id": int(team_id.value),
                "sport_id": int(sport_id.value),
                "gold_count": int(gold_count.value),
                "silver_count": int(silver_count.value),
                "bronze_count": int(bronze_count.value),
            }
            if medal:
                requests.put(f"{API_URL}/medals/{medal['id']}", json=data, timeout=5)
            else:
                requests.post(f"{API_URL}/medals", json=data, timeout=5)
            show_medals(page)
        except Exception as ex:
            show_alert(page, f"Error: {str(ex)}")
    
    back_btn = ft.Container(
        content=ft.Text("Back", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#f44336",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=lambda e: show_medals(page),
    )
    
    submit_btn = ft.Container(
        content=ft.Text("Save", size=12, color="white", weight=ft.FontWeight.BOLD),
        width=70,
        height=35,
        bgcolor="#4CAF50",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=on_submit,
    )
    
    header_row = ft.Row([ft.Text(f"{'Edit' if medal else 'Add'} Medal", size=20, weight=ft.FontWeight.BOLD), ft.Container(expand=True), submit_btn, back_btn], spacing=10)
    
    container = ft.Container(
        content=ft.Column(
            [header_row, medal_id_field, team_id, sport_id, gold_count, silver_count, bronze_count, ft.Container(expand=True)],
            spacing=10,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )
    
    page.add(container)
    
    # Store current page function for responsive updates
    page.current_page_function = lambda: show_medal_form(page, medal)

def delete_medal(page, medal_id):
    """ลบเหรียญ"""
    try:
        requests.delete(f"{API_URL}/medals/{medal_id}", timeout=5)
        show_medals(page)
    except Exception as e:
        show_alert(page, f"Error: {str(e)}")

# ================== LEADERBOARD PAGE ==================

def show_leaderboard(page):
    """แสดงตารางคะแนน (เรียงคะแนนสูงสุดลงต่ำสุด, ดูได้อย่างเดียว)"""
    if hasattr(page, 'navigation_bar') and page.navigation_bar is not None:
        page.navigation_bar.selected_index = 0
    page.clean()

    global all_medals, all_teams
    all_medals = fetch_medals()
    all_teams = fetch_teams()

    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height

    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)

    is_landscape = width > height

    # Responsive layout
    # ใช้ขอบซ้าย-ขวา 20px เพื่อให้เต็มจอแต่ไม่ชิดขอบเกินไป
    container_width = width
    container_height = max(0, height - 120)
    if is_landscape:
        team_name_width = 120
        medal_width = 140
    else:
        team_name_width = 80
        medal_width = 100

    # Calculate leaderboard from medals
    medals_by_team = {}
    for medal in all_medals:
        team_id = medal.get('team_id')
        if team_id not in medals_by_team:
            medals_by_team[team_id] = {
                'team_id': team_id,
                'total_gold': 0,
                'total_silver': 0,
                'total_bronze': 0,
                'total_score': 0
            }
        medals_by_team[team_id]['total_gold'] += medal.get('gold_count', 0)
        medals_by_team[team_id]['total_silver'] += medal.get('silver_count', 0)
        medals_by_team[team_id]['total_bronze'] += medal.get('bronze_count', 0)
        # Calculate score: Gold=3pts, Silver=2pts, Bronze=1pt
        medals_by_team[team_id]['total_score'] += (
            medal.get('gold_count', 0) * 3 +
            medal.get('silver_count', 0) * 2 +
            medal.get('bronze_count', 0) * 1
        )

    # Sort by total score
    all_leaderboard = sorted(medals_by_team.values(), key=lambda x: x.get('total_score', 0), reverse=True)

    header = ft.Text("Leaderboard", size=24, weight=ft.FontWeight.BOLD, color="#0277bd")
    header_row = ft.Row([header], spacing=10)

    # Build leaderboard list
    leaderboard_items = ft.Column(spacing=5)
    for idx, lb in enumerate(all_leaderboard, 1):
        item = ft.Container(
            content=ft.Row(
                [
                    ft.Text(f"#{idx}", size=12, weight=ft.FontWeight.BOLD, width=30),
                    ft.Text(get_team_name(lb.get('team_id', '-')), size=12, weight=ft.FontWeight.BOLD, width=team_name_width),
                    ft.Text(f"🥇{lb.get('total_gold', 0)} 🥈{lb.get('total_silver', 0)} 🥉{lb.get('total_bronze', 0)}", size=11, width=medal_width),
                    ft.Text(f"Points: {lb.get('total_score', 0)}", size=11, weight=ft.FontWeight.BOLD, color="#ff6f00"),
                ],
                spacing=5,
            ),
            padding=10,
            bgcolor="#F5F5F5" if idx % 2 == 0 else "#FFFFFF",
            border_radius=5,
        )
        leaderboard_items.controls.append(item)

    main_container = ft.Container(
        content=ft.Column(
            [
                header_row,
                ft.Container(
                    content=ft.ListView([leaderboard_items], expand=True),
                    width=container_width,
                    expand=True,
                ),
            ],
            spacing=15,
        ),
        width=container_width,
        height=container_height,
        padding=10,
        bgcolor="white",
    )

    page.add(
        ft.Container(
            content=ft.Row(
                [main_container],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

    # Store current page function for responsive updates
    page.current_page_function = lambda: show_leaderboard(page)

# ================== HOME PAGE ==================

def show_home(page):
    """แสดงหน้าแรก"""
    page.clean()
    
    header = ft.Text("Sport App", size=28, weight=ft.FontWeight.BOLD, color="#1565c0")
    subtitle = ft.Text("Manage your sports data", size=14, color="#666666")
    
    # Menu buttons
    buttons = [
        ("Teams", "#1976d2", lambda e: show_teams(page)),
        ("Athletes", "#7b1fa2", lambda e: show_athletes(page)),
        ("Sports", "#c2185b", lambda e: show_sports(page)),
        ("Matches", "#2e7d32", lambda e: show_matches(page)),
        ("Medals", "#f57f17", lambda e: show_medals(page)),
        ("Leaderboard", "#0277bd", lambda e: show_leaderboard(page)),
    ]
    
    menu_buttons = ft.Column(spacing=10)
    for label, color, on_click in buttons:
        btn = ft.Container(
            content=ft.Text(label, size=16, color="white", weight=ft.FontWeight.BOLD),
            width=320,
            height=50,
            bgcolor=color,
            border_radius=10,
            alignment=ft.Alignment(0, 0),
            on_click=on_click,
            shadow=ft.BoxShadow(blur_radius=15, color="#00000020"),
        )
        menu_buttons.controls.append(btn)
    
    main_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=20),
                header,
                subtitle,
                ft.Container(height=30),
                menu_buttons,
                ft.Container(expand=True),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=360,
        height=844,
        padding=15,
        bgcolor="white",
    )
    
    page.add(main_container)


def show_edit_page(page):
    """หน้าต่างแก้ไข: รวมการเข้าถึง Teams / Athletes / Sports / Medals"""
    if hasattr(page, 'navigation_bar') and page.navigation_bar is not None:
        page.navigation_bar.selected_index = 3
    page.clean()

    # Get responsive dimensions
    width = None
    height = None
    if hasattr(page, 'window') and page.window is not None:
        width = page.window.width
        height = page.window.height

    if width is None or height is None:
        width = getattr(page, 'window_width', 360)
        height = getattr(page, 'window_height', 844)

    is_landscape = width > height

    # Responsive layout
    if is_landscape:
        container_width = width
        container_height = height - 100
        button_width = (width - 40) / 2
        # In landscape, arrange buttons in rows
        buttons_per_row = 2
    else:
        container_width = width
        container_height = height - 100
        button_width = width - 40
        buttons_per_row = 1

    header = ft.Text("Edit Center", size=24, weight=ft.FontWeight.BOLD, color="#1976d2")

    def do_logout(e):
        """Logout and return to login page"""
        current_user["username"] = None
        current_user["user_id"] = None
        current_user["is_authenticated"] = False
        page.navigation_bar = None

        # Callback for login after logout
        def on_login_success_callback(user_data):
            """Callback after successful login"""
            global current_user
            current_user["username"] = user_data.get("username")
            current_user["user_id"] = user_data.get("user_id")
            current_user["is_authenticated"] = True
            # Recreate navigation bar
            page.navigation_bar = ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.icons.Icons.LEADERBOARD, label="Leaderboard"),
                    ft.NavigationBarDestination(icon=ft.icons.Icons.SPORTS_BASKETBALL, label="Matches"),
                    ft.NavigationBarDestination(icon=ft.icons.Icons.GROUP, label="Teams"),
                    ft.NavigationBarDestination(icon=ft.icons.Icons.EDIT, label="Edit"),
                ],
                selected_index=0,
                on_change=_on_nav_change,
            )
            show_leaderboard(page)

        show_login(page, on_login_success_callback)

    buttons = [
        ("Teams", "#1976d2", lambda e: show_teams_edit(page)),
        ("Athletes", "#7b1fa2", lambda e: show_athletes(page)),
        ("Sports", "#c2185b", lambda e: show_sports(page)),
        ("Matches", "#2e7d32", lambda e: show_matches_edit(page)),
        ("Medals", "#f57f17", lambda e: show_medals(page)),
    ]

    # Create menu buttons with responsive layout
    menu_buttons = ft.Column(spacing=10)
    if is_landscape and buttons_per_row > 1:
        # Arrange buttons in rows for landscape
        current_row = ft.Row(spacing=10)
        for i, (label, color, on_click) in enumerate(buttons):
            btn = ft.Container(
                content=ft.Text(label, size=16, color="white", weight=ft.FontWeight.BOLD),
                width=(button_width - 10) / buttons_per_row,
                height=50,
                bgcolor=color,
                border_radius=10,
                alignment=ft.Alignment(0, 0),
                on_click=on_click,
                shadow=ft.BoxShadow(blur_radius=15, color="#00000020"),
            )
            current_row.controls.append(btn)

            if (i + 1) % buttons_per_row == 0 or i == len(buttons) - 1:
                menu_buttons.controls.append(current_row)
                current_row = ft.Row(spacing=10)
    else:
        # Single column for portrait
        for label, color, on_click in buttons:
            btn = ft.Container(
                content=ft.Text(label, size=16, color="white", weight=ft.FontWeight.BOLD),
                width=button_width,
                height=50,
                bgcolor=color,
                border_radius=10,
                alignment=ft.Alignment(0, 0),
                on_click=on_click,
                shadow=ft.BoxShadow(blur_radius=15, color="#00000020"),
            )
            menu_buttons.controls.append(btn)

    # Logout button
    logout_btn = ft.Container(
        content=ft.Text("Logout", size=16, color="white", weight=ft.FontWeight.BOLD),
        width=button_width,
        height=50,
        bgcolor="#d32f2f",
        border_radius=10,
        alignment=ft.Alignment(0, 0),
        on_click=do_logout,
        shadow=ft.BoxShadow(blur_radius=15, color="#00000020"),
    )

    main_content = ft.Column(
        [
            ft.Container(height=20),
            ft.Container(content=header, alignment=ft.Alignment(0, 0)),
            ft.Container(height=20),
            ft.Container(content=menu_buttons, alignment=ft.Alignment(0, 0)),
            ft.Container(height=10),
            ft.Container(content=logout_btn, alignment=ft.Alignment(0, 0)),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    main_container = ft.Container(
        content=ft.ListView([main_content], expand=True),
        width=container_width,
        height=container_height,
        padding=15,
        bgcolor="white",
    )

    page.add(
        ft.Container(
            content=ft.Row(
                [main_container],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    )

    # Store current page function for responsive updates
    page.current_page_function = lambda: show_edit_page(page)


def show_alert(page, message):
    """แสดงข้อความแจ้งเตือน"""
    dlg = ft.AlertDialog(
        title=ft.Text("Notice"),
        content=ft.Text(message),
        actions=[ft.TextButton("OK")],
    )
    page.dialog = dlg
    dlg.open = True
    page.update()

# ================== MAIN APP ==================

def _on_nav_change(e):
    page = current_page_state.get("page")
    if page is None:
        return
    selected_index = e.control.selected_index
    if selected_index == 0:
        show_leaderboard(page)
    elif selected_index == 1:
        show_matches(page)
    elif selected_index == 2:
        show_teams(page)
    elif selected_index == 3:
        show_edit_page(page)


def main(page: ft.Page):
    page.title = "Sport App"
    # Remove fixed dimensions for responsive design
    page.window.resizable = True
    page.window.min_width = 320
    page.window.min_height = 480
    page.bgcolor = "white"
    current_page_state["page"] = page

    # Handle window resize/orientation changes
    def on_window_resize(e):
        """Handle window resize and orientation changes"""
        update_layout_for_size(page)

    page.on_resize = on_window_resize

    # Navigation bar will be added after login
    page.navigation_bar = None

    def create_navigation_bar():
        """Create navigation bar for authenticated pages"""
        return ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.Icons.LEADERBOARD, label="Leaderboard"),
                ft.NavigationBarDestination(icon=ft.icons.Icons.SCHEDULE, label="Matches"),
                ft.NavigationBarDestination(icon=ft.icons.Icons.GROUP, label="Teams"),
                ft.NavigationBarDestination(icon=ft.icons.Icons.EDIT, label="Edit"),
            ],
            selected_index=0,
            on_change=_on_nav_change,
        )

    def on_login_success(user_data):
        """Callback after successful login"""
        global current_user
        current_user["username"] = user_data.get("username")
        current_user["user_id"] = user_data.get("user_id")
        current_user["is_authenticated"] = True
        # Add navigation bar after login
        page.navigation_bar = create_navigation_bar()
        show_leaderboard(page)

    show_login(page, on_login_success)


if __name__ == "__main__":
    ft.run(main)
