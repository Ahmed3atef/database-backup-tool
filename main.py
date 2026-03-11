from UI.app import BackupApp


if __name__ == "__main__":
    try:
        app = BackupApp()
        app.run()
    except ImportError as e:
        raise e