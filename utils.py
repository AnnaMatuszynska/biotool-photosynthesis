import gettext
import os
from logging import getLogger
from typing import Callable


def get_localised_text(domain: str, version: str, language: str) -> Callable[[str], str]:
    try:
        localizator = gettext.translation(
            domain, localedir=os.path.join("locales", version), languages=[language]
        )
        localizator.install()
        getLogger().warning(f"Using locale {language} and version {version}")
        return localizator.gettext
    except:
        getLogger().warning(f"Could not find locale for language {language} and version {version}")
        return gettext.gettext
