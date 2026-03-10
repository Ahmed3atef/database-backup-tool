from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label, Input, Select
from textual.containers import Container, VerticalScroll, Horizontal
from textual.screen import Screen
from core.utils import setup_logger, setup_backups_dir
from core.backup import full_backup
from core.backup.executors import DockerExecutor, LocalExecutor, SSHExecutor, SSHDockerExecutor
from UI.screens import BackupForm
import asyncio
import os

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