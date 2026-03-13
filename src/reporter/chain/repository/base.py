from pathlib import Path
from typing import Protocol


class BaseRepository(Protocol):
    def get_source_data(self, source: Path) -> list[dict[str, str]]:
        """Чтение данных из источника

        :param source: Источник, из которого будут читаться данные
        :return: Возвращает контракт, полученный из источника
        """
        ...
