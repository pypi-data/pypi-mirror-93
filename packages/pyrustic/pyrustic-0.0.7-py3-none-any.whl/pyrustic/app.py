import tkinter as tk
import copy
import platform
import sys
import os
import os.path
from pyrustic.viewable import Viewable
from pyrustic import tkmisc
from pyrustic import about as pyrustic_about
from pyrustic.exception import PyrusticAppException
from pyrustic.private.enhance_tk import EnhanceTk
from pyrustic.jasonix import Jasonix


_DEFAULT_CONFIG_PATH = os.path.join(pyrustic_about.ROOT_DIR,
                                    "private",
                                    "default_app_config.json")


class App:
    """
    Pyrustic Framework's entry point.
    This class should be instantiated inside the file "main.py".
    """
    def __init__(self, root_dir=None):
        """
        Create an App instance.
        It's recommended to don't write any code above this instantiation.
        """
        self._root_dir = root_dir
        self._project_name = None
        self._is_running = False
        self._root = tk.Tk()
        self._theme = None
        self._view = None
        self._center_window = False
        self._config_data = None
        self._setup()
        self._config_path = self._get_config_path()
        self._set_default_title()

    # ============================================
    #                PROPERTIES
    # ============================================
    @property
    def root(self):
        """
        Get the main tk root
        """
        return self._root

    @property
    def config(self):
        """
        Get a dict-like deepcopy of your config file if it exists and is valid.
        Else you will get the default config dict.
        """
        return self._config_path, copy.deepcopy(self._config_data)

    @property
    def theme(self):
        """
        Get the theme object
        For more information about what a theme is:
        - check 'pyrustic.theme.Theme';
        - then check the beautiful theme 'pyrustic.theme.cyberpunk'
        """
        return self._theme

    @theme.setter
    def theme(self, val):
        """
        Set the theme object.
        If you set None, it will invalidate the previous theme.
        Don't forget to call the method "restart()" or "start()" to apply the change !
        Remember that "start()" should be called only once !
        For more information about what a theme is:
        - check "pyrustic.theme.Theme";
        - then check the beautiful theme "pyrustic.theme.cyberpunk"
        """
        self._root.option_clear()
        self._theme = val

    @property
    def view(self):
        """
        Get the view object.
        A view should implement "pyrustic.viewable.Viewable"
        """
        return self._view

    @view.setter
    def view(self, val):
        """
        Set a view object.
        If you set None, the previous view will be destroyed.
        A view should implement "pyrustic.viewable.Viewable".
        The new view will destroy the previous one if there are a previous one.
        """
        if val is not None and not isinstance(val, Viewable):
            raise PyrusticAppException("{} isn't a Viewable".format(val))
        if self._view:
            self._view.destroy()
        self._view = val

    # ============================================
    #               PUBLIC METHODS
    # ============================================
    def start(self):
        """
        Call this method to start the app.
        It should be called once and put on the last line of the file.
        """
        if self._is_running:
            message = "This method shouldn't be called twice. Please use 'restart' instead"
            raise PyrusticAppException(message)
        self._is_running = True
        self._root.protocol("WM_DELETE_WINDOW", self._on_exit)
        EnhanceTk(self._root)
        self._set_config()
        self._set_theme()
        self._install_view()
        try:
            self._root.mainloop()
        except KeyboardInterrupt:
            pass

    def restart(self):
        """
        Call this method to restart the app.
        You would need to submit a new view first before calling this method.
        """
        if not self._is_running:
            message = "The app should be already running before you could call this method"
            raise PyrusticAppException(message)
        self._set_theme()
        self._install_view()

    def exit(self):
        """
        Exit, simply ;-)
        Depending on your config file, the application will close quickly or not.
        A quick exit will ignore the lifecycle of a Viewable (pyrustic.viewable).
        In others words, '_on_destroy()' methods won't be called.
        Exit quickly if you don't care clean-up but want the app to close as fast as possible.
        """
        self._on_exit()

    def maximize(self):
        """
        Maximize the window
        """
        system = platform.system()
        if system == "Linux":
            self._root.attributes("-zoomed", True)
        else:  # for "Darwin" (OSX) and "Window"
            self._root.state("zoomed")

    def center(self):
        """
        Center the window
        """
        self._center_window = True

    # ============================================
    #               PRIVATE METHODS
    # ============================================
    def _set_config(self):
        if not os.path.exists(self._config_path):
            return
        jasonix = Jasonix(self._config_path,
                            _DEFAULT_CONFIG_PATH)
        self._config_data = jasonix.data
        # app geometry
        if not self._config_data["ignore_geometry"]:
            self._root.geometry(self._config_data["root_geometry"])
        # background
        background_color = self._config_data["root_background"]
        self._root.config(background=background_color)
        # resizable width and height
        resizable_width = self._config_data["resizable_width"]
        resizable_height = self._config_data["resizable_height"]
        self._root.resizable(width=resizable_width, height=resizable_height)
        # maximize screen
        if self._config_data["maximize_window"]:
            self.maximize()

    def _set_theme(self):
        if not self._config_data["allow_theme"]:
            return
        if not self._theme:
            return
        self._theme.target(self._root)

    def _install_view(self):
        if not self._view:
            return
        if not self._view.build():
            return
        if isinstance(self._view.body, tk.Frame):
            self._view.body.pack(in_=self._root,
                                 expand=1, fill=tk.BOTH)
        # center
        if self._center_window:
            tkmisc.center_window(self._root)


    def _on_exit(self):
        if self._view:
            self._view.destroy()
            self._view = None
        if self._root:
            self._root.destroy()
            self._root = None
        sys.exit()

    def _set_default_title(self):
        title = "{} | built with Pyrustic".format(self._project_name)
        self._root.title(title)

    def _get_config_path(self):
        pyrustic_data = os.path.join(self._root_dir, "pyrustic_data")
        if not os.path.exists(pyrustic_data):
            os.mkdir(pyrustic_data)
        return os.path.join(pyrustic_data, "gui.json")

    def _setup(self):
        if self._root_dir is None:
            try:
                import about
                self._root_dir = about.ROOT_DIR
                self._project_name = about.PROJECT_NAME
            except ImportError:
                message = "Please set the root_dir or put an about.py module in the root of your project"
                raise PyrusticAppException(message)
        if not self._project_name:
            self._project_name = os.path.basename(self._root_dir)
