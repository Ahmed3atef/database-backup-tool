from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Label, Input, Select
from textual.containers import Container, VerticalScroll, Horizontal
from textual.screen import Screen
from core.utils import setup_logger, setup_backups_dir
from core.backup import full_backup
from core.backup.executors import DockerExecutor, LocalExecutor, SSHExecutor, SSHDockerExecutor
import asyncio
import os

class BackupForm(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            VerticalScroll(
                Label("Database Name"),
                Input(placeholder="db_name", id="db_name"),
                Label("Username"),
                Input(placeholder="user", id="db_user"),
                Label("Password"),
                Input(placeholder="password", password=True, id="db_pass"),
                Label("Database Type"),
                Select(
                    options=[(t, t) for t in ["mysql", "postgresql", "sqlite", "mongodb"]],
                    id="db_type"
                ),
                Label("Executor Type"),
                Select(
                    options=[(t, t) for t in ["local", "docker", "ssh", "ssh_docker"]],
                    id="executor_type"
                ),
                # Dynamic fields container
                VerticalScroll(id="dynamic_fields"),
                Horizontal(
                    Button("Run Backup", variant="success", id="btn_run"),
                    Button("Back", variant="default", id="btn_back"),
                ),
                id="form_container"
            ),
            id="main_container"
        )
        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "executor_type":
            self.update_dynamic_fields(event.value)

    def update_dynamic_fields(self, executor_type: str) -> None:
        if not executor_type or executor_type == Select.BLANK:
            return
            
        container = self.query_one("#dynamic_fields", VerticalScroll)
        container.remove_children()
        
        if executor_type in ["docker", "ssh_docker"]:
            container.mount(Label("Container Name"))
            container.mount(Input(placeholder="container_name", id="container_name"))
        
        if executor_type in ["ssh", "ssh_docker"]:
            container.mount(Label("SSH Host"))
            container.mount(Input(placeholder="host", id="ssh_host"))
            container.mount(Label("SSH Port"))
            container.mount(Input(placeholder="22", id="ssh_port", value="22"))
            container.mount(Label("SSH User"))
            container.mount(Input(placeholder="username", id="ssh_user"))
            container.mount(Label("SSH Password"))
            container.mount(Input(placeholder="password", password=True, id="ssh_pass"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_back":
            self.app.pop_screen()
        elif event.button.id == "btn_run":
            self.run_backup_task()

    def run_backup_task(self) -> None:
        asyncio.create_task(self.run_backup())

    async def run_backup(self) -> None:
        try:
            db_name = self.query_one("#db_name", Input).value
            db_user = self.query_one("#db_user", Input).value
            db_pass = self.query_one("#db_pass", Input).value
            db_type = self.query_one("#db_type", Select).value
            executor_type = self.query_one("#executor_type", Select).value

            if not all([db_name, db_user, db_pass, db_type, executor_type]) or db_type == Select.BLANK or executor_type == Select.BLANK:
                self.app.notify("Please fill all required fields", severity="error")
                return

            # Prepare executor
            if executor_type == "local":
                executor = LocalExecutor()
            elif executor_type == "docker":
                container_name = self.query_one("#container_name", Input).value
                executor = DockerExecutor(container_name=container_name)
            elif executor_type == "ssh":
                host = self.query_one("#ssh_host", Input).value
                user = self.query_one("#ssh_user", Input).value
                password = self.query_one("#ssh_pass", Input).value
                executor = SSHExecutor(host=host, user=user, password=password)
            elif executor_type == "ssh_docker":
                host = self.query_one("#ssh_host", Input).value
                user = self.query_one("#ssh_user", Input).value
                password = self.query_one("#ssh_pass", Input).value
                container_name = self.query_one("#container_name", Input).value
                executor = SSHDockerExecutor(host=host, user=user, password=password, container_name=container_name)
            else:
                self.app.notify(f"Invalid executor type: {executor_type}", severity="error")
                return

            self.app.notify("Starting backup...", severity="info")
            
            logger = setup_logger()
            output_file = setup_backups_dir(db_name)
            
            # Run the backup logic
            await full_backup(
                db_type=db_type,
                db_name=db_name,
                db_user=db_user,
                db_pass=db_pass,
                output_file=output_file,
                logger=logger,
                executor=executor
            )
            self.app.notify(f"Backup successful! Saved to {os.path.basename(output_file)}", severity="success")
        except Exception as e:
            self.app.notify(f"Error: {str(e)}", severity="error")
