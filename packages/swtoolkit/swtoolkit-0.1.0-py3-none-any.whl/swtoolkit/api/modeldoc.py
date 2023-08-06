from .interfaces.imodeldoc import IModelDoc
from .enums.enum_options import StandardViews, SaveAsOptions
from .enums.enum_types import DocumentTypes


class ModelDoc(IModelDoc):
    def __init__(self, system_object=None):
        super().__init__(system_object)

    def __repr__(self):
        return f"{self.__class__.__name__} <{self.title}>"

    def __str__(self):
        return self.title

    @property
    def title(self) -> str:
        """Returns the title of the document or model."""
        return self._get_title()

    @property
    def type(self):
        """Returns the document or model type."""
        return DocumentTypes(self._get_type())

    @property
    def path(self) -> str:
        """Returns the path of the document or model."""
        return self._get_path_name()

    def save(self, options: str = "silent"):
        """Saves the current ModelDoc object

        Args:
            options (str, optional): Save as options. Defaults to "silent".

        Returns:
            Tuple: True if save is successful, followed by Errors and Warnings
        """
        _options = SaveAsOptions[options.upper().replace(" ", "_")].value
        retval, err, warn = self.save3(_options)
        return retval, err.value, warn.value

    def set_view(self, view_name: str, fit: bool = False):
        """Allows the model view to be selected

        Args:
            view_name (str): Name of the view to show.
            fit (bool, optional): Fits model to viewport if True.

        Example:
            model.show_view('Isometric')
        """
        _view_id = StandardViews[view_name.upper().replace(" ", "_")].value
        self.show_named_view2(str(), _view_id)
        if fit:
            self.zoom_to_fit()

    def zoom_to_fit(self):
        """Fits model to viewport."""
        self.view_zoom_to_fit2()
