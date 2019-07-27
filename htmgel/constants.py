import os
from . import locator

PATH_TO_HTMGEL = os.path.dirname(os.path.abspath(locator.__file__))
PATH_TO_HTMGEL_BOOTSTRAP3 = os.path.join(os.path.dirname(PATH_TO_HTMGEL), "htmgel_bootstrap3")
PATH_TO_HTMGEL_BOOTSTRAP4 = os.path.join(os.path.dirname(PATH_TO_HTMGEL), "htmgel_bootstrap4")
PATH_TO_HTMGEL_FOUNDATION6 = os.path.join(os.path.dirname(PATH_TO_HTMGEL), "htmgel_foundation6")

if os.path.exists(PATH_TO_HTMGEL_BOOTSTRAP3):
    HTMGEL_FRAMEWORK = "bootstrap3"
elif os.path.exists(PATH_TO_HTMGEL_BOOTSTRAP4):
    HTMGEL_FRAMEWORK = "bootstrap4"
elif os.path.exists(PATH_TO_HTMGEL_FOUNDATION6):
    HTMGEL_FRAMEWORK = "foundation6"
else:
    HTMGEL_FRAMEWORK = None
