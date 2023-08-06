from typing import Dict, Optional, cast
from pytket.config import PytketConfig, PytketExtConfig


class QSharpConfig(PytketExtConfig):
    resourceId: Optional[str]
    location: Optional[str]
    storage: Optional[str]

    def __init__(self, config: PytketConfig) -> None:
        if "qsharp" in config.extensions:
            config_dict = cast(Dict[str, str], config.extensions["qsharp"])
            self.resourceId = config_dict.get("resourceId")
            self.location = config_dict.get("location")
            self.storage = config_dict.get("storage")

        else:
            self.resourceId = None
            self.location = None
            self.storage = None
