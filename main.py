from ui import StudySyncApp

def main():
    """
    The main entry point of the StudySync application.
    Initializes the UI and starts the application.
    """
    # Initialize the StudySyncApp, which in turn initializes the database, auth, and other modules
    app = StudySyncApp()

if __name__ == "__main__":
    main()
