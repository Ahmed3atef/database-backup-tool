from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label, Select
from textual.containers import Container, VerticalScroll, HorizontalGroup
from textual.screen import Screen
from core.utils import project_root, setup_logger
from core.compression.tar_utils import compress_backup
import os

class CompressionScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            VerticalScroll(
                Label("Select Backup to Compress"),
                Select(
                    options=self.get_backup_files(),
                    id="backup_select"
                ),
                HorizontalGroup(
                    Button("Compress", variant="success", id="btn_compress"),
                    Button("Back", variant="default", id="btn_back"),
                ),
                id="form_container"
            ),
            id="main_container"
        )
        yield Footer()

    def get_backup_files(self) -> list[tuple[str, str]]:
        backups_dir = os.path.join(project_root, "backups")
        if not os.path.exists(backups_dir):
            return []
        
        files = [f for f in os.listdir(backups_dir) if os.path.isfile(os.path.join(backups_dir, f)) and not f.endswith(".tar.gz")]
        return [(f, f) for f in files]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_back":
            self.app.pop_screen()
        elif event.button.id == "btn_compress":
            self.handle_compression()

    def handle_compression(self) -> None:
        select = self.query_one("#backup_select", Select)
        filename = select.value
        
        if not filename or filename == Select.BLANK:
            self.app.notify("Please select a file to compress", severity="warning")
            return
            
        backups_dir = os.path.join(project_root, "backups")
        backup_file = os.path.join(backups_dir, filename)
        output_file = backup_file + ".tar.gz"
        
        try:
            logger = setup_logger()
            compress_backup(backup_file, output_file, logger)
            self.app.notify(f"Compressed: {os.path.basename(output_file)}", severity="success")
            # Refresh list
            select.options = self.get_backup_files()
            select.value = Select.BLANK
        except Exception as e:
            self.app.notify(f"Compression failed: {str(e)}", severity="error")
