import datetime as dt
import json
import typing as t

from analytix import InvalidRequest
from analytix.youtube.abc import YouTubeAnalytics
from analytix.youtube.features import (
    YOUTUBE_ANALYTICS_DEFAULT_METRICS,
    YOUTUBE_ANALYTICS_DEFAULT_PLAYLIST_METRICS,
    YOUTUBE_ANALYTICS_DEFAULT_PROVINCE_METRICS,
    Dimensions,
    Filters,
)


class BasicYouTubeAnalytics(YouTubeAnalytics):
    """A class to retrieve basic user activity data.

    Args:
        service (YouTubeService): The YouTube service to perform the operation on.
        by_province (bool): Whether to get data for provinces or countries. Defaults to False.

    Attributes:
        dimensions (Dimensions): An object for dimension verification.
        metrics (tuple[str, ...]): A tuple containing all valid metrics.
        filters (Filters): An object for filter verification.
    """

    __slots__ = ("service", "dimensions", "_by_province", "metrics", "filters")

    def __init__(self, service, by_province=False):
        super().__init__(service)
        self.dimensions = Dimensions(none=True)
        self.by_province = by_province

    @property
    def by_province(self):
        """A Boolean shortcut to change the list of allowed metrics, dimensions, and filters by changing whether the data is fetched by province."""
        return self._by_province

    @by_province.setter
    def by_province(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"expected bool for by_province, got {type(value).__name__}")

        self._by_province = value
        if not value:
            self.metrics = YOUTUBE_ANALYTICS_DEFAULT_METRICS
            self.filters = Filters(opt=[("country", "continent", "subContinent"), ("video", "group")])
        else:
            self.metrics = YOUTUBE_ANALYTICS_DEFAULT_PROVINCE_METRICS
            self.filters = Filters(many=[("province",)], opt=[("video", "group")])

    def _check_features(self, metrics, dimensions, filters):
        if not metrics:
            raise InvalidRequest(f"expected at least 1 metric, got 0")

        for m in metrics:
            if m not in self.metrics:
                raise InvalidRequest(f"unexpected metric: {m}")

        self.dimensions.verify(dimensions)
        self.filters.verify(filters)


class TimeBasedYouTubeAnalytics(YouTubeAnalytics):
    """A class to retrieve time based analytical data.

    Args:
        service (YouTubeService): The YouTube service to perform the operation on.
        by_province (bool): Whether to get data for provinces or countries. Defaults to False.

    Attributes:
        dimensions (Dimensions): An object for dimension verification.
        metrics (tuple[str, ...]): A tuple containing all valid metrics.
        filters (Filters): An object for filter verification.
    """

    def __init__(self, service, by_province=False):
        super().__init__(service)
        self.dimensions = Dimensions(req=[("day", "month")])
        self.by_province = by_province

    @property
    def by_province(self):
        """A Boolean shortcut to change the list of allowed metrics, dimensions, and filters by changing whether the data is fetched by province."""
        return self._by_province

    @by_province.setter
    def by_province(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"expected bool for by_province, got {type(value).__name__}")

        self._by_province = value
        if not value:
            self.metrics = YOUTUBE_ANALYTICS_DEFAULT_METRICS
            self.filters = Filters(opt=[("country", "continent", "subContinent"), ("video", "group")])
        else:
            self.metrics = YOUTUBE_ANALYTICS_DEFAULT_PROVINCE_METRICS
            self.filters = Filters(many=[("province",)], opt=[("video", "group")])

    def _check_features(self, metrics, dimensions, filters):
        if not metrics:
            raise InvalidRequest(f"expected at least 1 metric, got 0")

        for m in metrics:
            if m not in self.metrics:
                raise InvalidRequest(f"unexpected metric: {m}")

        self.dimensions.verify(dimensions)
        self.filters.verify(filters)


class GeographicYouTubeAnalytics(YouTubeAnalytics):
    """A class to retrieve user geography analytical data.

    Args:
        service (YouTubeService): The YouTube service to perform the operation on.
        by_province (bool): Whether to get data for provinces or countries. Defaults to False.

    Attributes:
        dimensions (Dimensions): An object for dimension verification.
        metrics (tuple[str, ...]): A tuple containing all valid metrics.
        filters (Filters): An object for filter verification.
    """

    def __init__(self, service, by_province=False):
        super().__init__(service)
        self.by_province = by_province

    @property
    def by_province(self):
        """A Boolean shortcut to change the list of allowed metrics, dimensions, and filters by changing whether the data is fetched by province."""
        return self._by_province

    @by_province.setter
    def by_province(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"expected bool for by_province, got {type(value).__name__}")

        self._by_province = value
        if not value:
            self.dimensions = Dimensions(req=[("country",)])
            self.metrics = YOUTUBE_ANALYTICS_DEFAULT_METRICS
            self.filters = Filters(opt=[("continent", "subContinent"), ("video", "group")])
        else:
            self.dimensions = Dimensions(req=[("province",)])
            self.metrics = YOUTUBE_ANALYTICS_DEFAULT_PROVINCE_METRICS
            self.filters = Filters(many=[("country",)], opt=[("video", "group")])

    def _check_features(self, metrics, dimensions, filters):
        if not metrics:
            raise InvalidRequest(f"expected at least 1 metric, got 0")

        for m in metrics:
            if m not in self.metrics:
                raise InvalidRequest(f"unexpected metric: {m}")

        self.dimensions.verify(dimensions)
        self.filters.verify(filters)


class BasicPlaylistYouTubeAnalytics(YouTubeAnalytics):
    """A class to retrieve basic user activity data within playlists.

    Args:
        service (YouTubeService): The YouTube service to perform the operation on.
        by_province (bool): Whether to get data for provinces or countries. Defaults to False.

    Attributes:
        dimensions (Dimensions): An object for dimension verification.
        metrics (tuple[str, ...]): A tuple containing all valid metrics.
        filters (Filters): An object for filter verification.
    """

    __slots__ = ("service", "dimensions", "metrics", "filters")

    def __init__(self, service):
        super().__init__(service)
        self.dimensions = Dimensions(none=True)
        self.metrics = YOUTUBE_ANALYTICS_DEFAULT_PLAYLIST_METRICS
        self.filters = Filters(
            req=[("isCurated",)],
            opt=[
                ("country", "province", "continent", "subContinent"),
                ("playlist", "group"),
                ("subscribedStatus", "youtubeProduct"),
            ],
        )

    def _check_features(self, metrics, dimensions, filters):
        if not metrics:
            raise InvalidRequest(f"expected at least 1 metric, got 0")

        for m in metrics:
            if m not in self.metrics:
                raise InvalidRequest(f"unexpected metric: {m}")

        filters.update({"isCurated": "1"})
        self.dimensions.verify(dimensions)
        self.filters.verify(filters)


class TimeBasedPlaylistYouTubeAnalytics(YouTubeAnalytics):
    """A class to retrieve time based analytical data within playlists.

    Args:
        service (YouTubeService): The YouTube service to perform the operation on.
        by_province (bool): Whether to get data for provinces or countries. Defaults to False.

    Attributes:
        dimensions (Dimensions): An object for dimension verification.
        metrics (tuple[str, ...]): A tuple containing all valid metrics.
        filters (Filters): An object for filter verification.
    """

    __slots__ = ("service", "dimensions", "metrics", "filters")

    def __init__(self, service):
        super().__init__(service)
        self.dimensions = Dimensions(req=[("day", "month")])
        self.metrics = YOUTUBE_ANALYTICS_DEFAULT_PLAYLIST_METRICS
        self.filters = Filters(
            req=[("isCurated",)],
            opt=[
                ("country", "province", "continent", "subContinent"),
                ("playlist", "group"),
                ("subscribedStatus", "youtubeProduct"),
            ],
        )

    def _check_features(self, metrics, dimensions, filters):
        if not metrics:
            raise InvalidRequest(f"expected at least 1 metric, got 0")

        for m in metrics:
            if m not in self.metrics:
                raise InvalidRequest(f"unexpected metric: {m}")

        filters.update({"isCurated": "1"})
        self.dimensions.verify(dimensions)
        self.filters.verify(filters)


class GeographicPlaylistYouTubeAnalytics(YouTubeAnalytics):
    """A class to retrieve geographic analytical data within playlists.

    Args:
        service (YouTubeService): The YouTube service to perform the operation on.
        by_province (bool): Whether to get data for provinces or countries. Defaults to False.

    Attributes:
        dimensions (Dimensions): An object for dimension verification.
        metrics (tuple[str, ...]): A tuple containing all valid metrics.
        filters (Filters): An object for filter verification.
    """

    __slots__ = ("service", "dimensions", "metrics", "filters")

    def __init__(self, service):
        super().__init__(service)
        self.dimensions = Dimensions(req=[("country",)])
        self.metrics = YOUTUBE_ANALYTICS_DEFAULT_PLAYLIST_METRICS
        self.filters = Filters(
            req=[("isCurated",)],
            opt=[
                ("country", "province", "continent", "subContinent"),
                ("playlist", "group"),
                ("subscribedStatus", "youtubeProduct"),
            ],
        )

    def _check_features(self, metrics, dimensions, filters):
        if not metrics:
            raise InvalidRequest(f"expected at least 1 metric, got 0")

        for m in metrics:
            if m not in self.metrics:
                raise InvalidRequest(f"unexpected metric: {m}")

        filters.update({"isCurated": "1"})
        self.dimensions.verify(dimensions)
        self.filters.verify(filters)
