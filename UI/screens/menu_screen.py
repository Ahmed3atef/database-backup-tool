from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label, Input, Select
from textual.containers import Container, Vertical, Horizontal, VerticalScroll, HorizontalGroup
from textual.screen import Screen
from UI.screens import BackupForm

class MainMenu(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Database Backup Tool", id="title"),
            VerticalScroll(
                Button("New Backup", variant="success", id="btn_backup"),
                Button("Exit", variant="error", id="btn_exit"),
                id="menu_buttons"
            ),
            id="main_container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_backup":
            self.app.push_screen(BackupForm())
        elif event.button.id == "btn_exit":
            self.app.exit()