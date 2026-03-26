import flet as ft
import requests

API_URL = "http://192.168.100.5:3500"

def show_login(page, on_login_success):
    """แสดงหน้าล็อกอิน"""
    page.clean()
    
    # State for error message and form mode
    error_message = {"text": "", "visible": False}
    form_mode = {"is_register": False}  # False = Login, True = Register
    
    # ---------- HEADER ----------
    header = ft.Text(
        "Sport App",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="#1976d2",
    )
    
    subtitle = ft.Text(
        "Login to continue",
        size=14,
        color="#666666",
    )
    
    # ---------- USERNAME FIELD ----------
    username_field = ft.TextField(
        hint_text="Username",
        width=300,
        height=50,
        color="black",
        bgcolor="#FFFFFF",
        border_radius=8,
        border="1px solid #dddddd",
    )
    
    # ---------- PASSWORD FIELD ----------
    password_field = ft.TextField(
        hint_text="Password",
        width=300,
        height=50,
        color="black",
        bgcolor="#FFFFFF",
        border_radius=8,
        border="1px solid #dddddd",
        password=True,
    )
    
    # ---------- CONFIRM PASSWORD FIELD (for register) ----------
    confirm_password_field = ft.TextField(
        hint_text="Confirm Password",
        width=300,
        height=50,
        color="black",
        bgcolor="#FFFFFF",
        border_radius=8,
        border="1px solid #dddddd",
        password=True,
        visible=False,
    )
    
    # ---------- ERROR MESSAGE ----------
    error_text = ft.Text(
        error_message["text"],
        size=12,
        color="#ff3075",
        visible=error_message["visible"],
    )
    
    # ---------- LOGIN BUTTON ----------
    def on_login_click(e):
        """Handle login/register button click"""
        username = username_field.value.strip()
        password = password_field.value.strip()
        
        if not username or not password:
            error_message["text"] = "Please enter username and password"
            error_message["visible"] = True
            error_text.value = error_message["text"]
            error_text.visible = error_message["visible"]
            page.update()
            return
        
        # Register mode - check confirm password
        if form_mode["is_register"]:
            confirm_password = confirm_password_field.value.strip()
            if not confirm_password:
                error_message["text"] = "Please confirm your password"
                error_message["visible"] = True
                error_text.value = error_message["text"]
                error_text.visible = error_message["visible"]
                page.update()
                return

            if password != confirm_password:
                error_message["text"] = "Passwords do not match"
                error_message["visible"] = True
                error_text.value = error_message["text"]
                error_text.visible = error_message["visible"]
                page.update()
                return

            # Validate password complexity: uppercase, lowercase, number
            if not any(c.isupper() for c in password):
                error_message["text"] = "Password must include at least one uppercase letter"
                error_message["visible"] = True
                error_text.value = error_message["text"]
                error_text.visible = error_message["visible"]
                page.update()
                return
            if not any(c.islower() for c in password):
                error_message["text"] = "Password must include at least one lowercase letter"
                error_message["visible"] = True
                error_text.value = error_message["text"]
                error_text.visible = error_message["visible"]
                page.update()
                return
            if not any(c.isdigit() for c in password):
                error_message["text"] = "Password must include at least one number"
                error_message["visible"] = True
                error_text.value = error_message["text"]
                error_text.visible = error_message["visible"]
                page.update()
                return
        
        try:
            # Send login/register request to API
            response = requests.post(
                f"{API_URL}/user_login",
                json={"username": username, "password": password},
                timeout=5
            )
            
            if response.status_code == 200:
                login_response = response.json()
                
                if login_response.get("success"):
                    # Login/Register successful
                    if form_mode["is_register"]:
                        # Registration successful - show message and go back to login mode
                        error_message["text"] = "Account created successfully! Please login."
                        error_message["visible"] = True
                        error_text.value = error_message["text"]
                        error_text.visible = error_message["visible"]
                        
                        # Auto switch back to login mode
                        form_mode["is_register"] = False
                        subtitle.value = "Login to continue"
                        login_btn.content.value = "Login"
                        toggle_btn.content.value = "Don't have account? Register"
                        confirm_password_field.visible = False
                        username_field.value = ""
                        password_field.value = ""
                        confirm_password_field.value = ""
                        error_message["text"] = ""
                        error_message["visible"] = False
                        error_text.value = error_message["text"]
                        error_text.visible = error_message["visible"]
                        page.update()
                    else:
                        # Login successful - call callback with user data
                        user_data = {
                            "username": username,
                            "user_id": login_response.get("user_id"),
                        }
                        on_login_success(user_data)
                else:
                    # Login/Register failed
                    error_message["text"] = login_response.get("message", "Invalid username or password")
                    error_message["visible"] = True
                    error_text.value = error_message["text"]
                    error_text.visible = error_message["visible"]
                    password_field.value = ""
                    confirm_password_field.value = ""
                    page.update()
            else:
                # HTTP error - server returned non-200 status
                try:
                    error_response = response.json()
                    error_message["text"] = error_response.get("detail", f"Server error: {response.status_code}")
                except:
                    error_message["text"] = f"Server error: {response.status_code}"
                error_message["visible"] = True
                error_text.value = error_message["text"]
                error_text.visible = error_message["visible"]
                password_field.value = ""
                confirm_password_field.value = ""
                page.update()
        except requests.exceptions.ConnectionError as ce:
            print(f"Connection Error: {ce}")
            error_message["text"] = "Cannot connect to server. Please check your connection."
            error_message["visible"] = True
            error_text.value = error_message["text"]
            error_text.visible = error_message["visible"]
            page.update()
        except requests.exceptions.Timeout as te:
            print(f"Timeout Error: {te}")
            error_message["text"] = "Request timeout. Server is slow or offline."
            error_message["visible"] = True
            error_text.value = error_message["text"]
            error_text.visible = error_message["visible"]
            page.update()
        except Exception as ex:
            print(f"Unexpected error: {type(ex).__name__}: {ex}")
            error_message["text"] = f"Error: {str(ex)}"
            error_message["visible"] = True
            error_text.value = error_message["text"]
            error_text.visible = error_message["visible"]
            page.update()
    
    login_btn = ft.Container(
        content=ft.Text(
            "Login",
            size=16,
            color="white",
            weight=ft.FontWeight.BOLD,
        ),
        width=300,
        height=50,
        bgcolor="#1976d2",
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        on_click=on_login_click,
    )
    
    # ---------- TOGGLE BUTTON (Login/Register) ----------
    def on_toggle_mode(e):
        """Toggle between login and register mode"""
        form_mode["is_register"] = not form_mode["is_register"]
        
        if form_mode["is_register"]:
            # Switch to Register mode
            subtitle.value = "Create a new account"
            login_btn.content.value = "Register"
            toggle_btn.content.value = "Back to Login"
            confirm_password_field.visible = True
            error_message["text"] = ""
            error_message["visible"] = False
        else:
            # Switch to Login mode
            subtitle.value = "Login to continue"
            login_btn.content.value = "Login"
            toggle_btn.content.value = "Don't have account? Register"
            confirm_password_field.visible = False
            error_message["text"] = ""
            error_message["visible"] = False
        
        error_text.value = error_message["text"]
        error_text.visible = error_message["visible"]
        username_field.value = ""
        password_field.value = ""
        confirm_password_field.value = ""
        page.update()
    
    toggle_btn = ft.Container(
        content=ft.Text(
            "Don't have account? Register",
            size=12,
            color="#1976d2",
            weight=ft.FontWeight.BOLD,
        ),
        on_click=on_toggle_mode,
        padding=10,
    )
    
    # ---------- LAYOUT ----------
    def get_responsive_layout():
        """Get responsive layout based on screen size"""
        try:
            width = page.window.width if hasattr(page, 'window') else 360
            height = page.window.height if hasattr(page, 'window') else 844
            is_landscape = width > height

            # Responsive dimensions
            if is_landscape:
                container_width = min(width * 0.6, 500)  # Max 500px in landscape
                container_height = height - 100
                field_width = min(width * 0.4, 350)
            else:
                container_width = width - 30
                container_height = height - 100
                field_width = width - 60

            return container_width, container_height, field_width, is_landscape
        except:
            # Fallback for older Flet versions
            return 360, 844, 300, False

    container_width, container_height, field_width, is_landscape = get_responsive_layout()

    # Update field widths
    username_field.width = field_width
    password_field.width = field_width
    confirm_password_field.width = field_width
    login_btn.width = field_width

    top_padding = 30 if not is_landscape else 0
    gap_small = 8
    gap_medium = 10

    login_column = ft.Column(
        [
            ft.Container(height=top_padding),
            ft.Container(content=header, alignment=ft.Alignment(0, 0)),
            ft.Container(content=subtitle, alignment=ft.Alignment(0, 0)),
            ft.Container(height=gap_small),
            ft.Container(content=username_field, alignment=ft.Alignment(0, 0)),
            ft.Container(height=gap_small),
            ft.Container(content=password_field, alignment=ft.Alignment(0, 0)),
            ft.Container(height=gap_small),
            ft.Container(content=confirm_password_field, alignment=ft.Alignment(0, 0)),
            ft.Container(height=gap_small),
            ft.Container(content=error_text, alignment=ft.Alignment(0, 0)),
            ft.Container(height=gap_medium),
            ft.Container(content=login_btn, alignment=ft.Alignment(0, 0)),
            ft.Container(height=gap_medium),
            ft.Container(content=toggle_btn, alignment=ft.Alignment(0, 0)),
        ],
        spacing=0,
    )

    login_container = ft.Container(
        content=login_column,
        width=container_width,
        padding=15,
        bgcolor="white",
        alignment=ft.Alignment(0, -1),
    )

    page.add(
        ft.Container(
            content=ft.ListView(
                [login_container],
                expand=True,
                padding=ft.Padding(5),
            ),
            alignment=ft.Alignment(0, 0),
            expand=True,
        )
    )

    # Ensure responsive enables on_resize to refresh layout
    page.current_page_function = lambda: show_login(page, on_login_success)
