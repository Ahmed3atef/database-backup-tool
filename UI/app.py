from UI.screens import BackupForm, MainMenu
from textual.app import App, ComposeResult

class BackupApp(App):
    CSS_PATH = "css/styles.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]

    def on_mount(self) -> None:
        self.push_screen(MainMenu())
        
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
    )
    
    def action_quit(self) -> None:
        self.exit()

if __name__ == "__main__":
    app = BackupApp()
    app.run()
