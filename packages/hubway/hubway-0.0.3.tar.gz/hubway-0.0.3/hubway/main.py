import os.path
from pyrustic.app import App
from hubway import about
from hubway.misc import my_theme
from hubway.view.main_view import MainView


def main():
    app = App(about.ROOT_DIR)
    app.root.title("Hubway - built with Pyrustic")
    app.theme = my_theme.get_theme()
    app.view = MainView(app)
    app.center()
    app.start()


if __name__ == "__main__":
    main()
