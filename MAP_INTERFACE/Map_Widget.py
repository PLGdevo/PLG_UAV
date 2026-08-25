"""
Map display widget for RIGEL Ground Station.

UI layer: Tkinter-compatible map widget.
Map logic remains in Map_Manager / Map_Provider.
"""

import time
import tkinter as tk

from tkintermapview import TkinterMapView


class MapWidget(TkinterMapView):
    """Concrete map widget mounted into UI.Map_Container."""

    HOME_LAT = 10.8231
    HOME_LON = 106.6297
    HOME_ZOOM = 12

    MIN_ZOOM = 1
    MAX_ZOOM = 19

    def __init__(self, parent, **kwargs):

        # =====================================================
        # MOUSE WHEEL STATE
        # =====================================================

        self._last_wheel_time = 0.0

        # =====================================================
        # INITIALIZE TKINTERMAPVIEW
        # =====================================================

        super().__init__(
            parent,
            corner_radius=0,
            **kwargs,
        )

        # =====================================================
        # INTERNAL OBJECT STORAGE
        # =====================================================

        self._markers = {}
        self._routes = {}
        self._attribution = ""

        # =====================================================
        # INITIAL MAP VIEW
        # =====================================================

        self.set_position(
            self.HOME_LAT,
            self.HOME_LON,
        )

        self.set_zoom(
            self.HOME_ZOOM
        )

        # =====================================================
        # MOUSE WHEEL
        # =====================================================

        # Windows
        self.bind(
            "<MouseWheel>",
            self._on_mousewheel,
            add="+",
        )

        # Linux
        self.bind(
            "<Button-4>",
            self._on_mousewheel,
            add="+",
        )

        self.bind(
            "<Button-5>",
            self._on_mousewheel,
            add="+",
        )

        # =====================================================
        # KEYBOARD ZOOM
        # =====================================================

        self.bind(
            "<KeyPress-plus>",
            lambda event: self._zoom_and_break(1),
        )

        self.bind(
            "<KeyPress-equal>",
            lambda event: self._zoom_and_break(1),
        )

        self.bind(
            "<KeyPress-minus>",
            lambda event: self._zoom_and_break(-1),
        )

        self.bind(
            "<KeyPress-0>",
            lambda event: self._go_home_and_break(),
        )

        # =====================================================
        # FOCUS
        # =====================================================

        self.bind(
            "<Enter>",
            self._on_enter,
            add="+",
        )

    # =========================================================
    # MOUSE
    # =========================================================

    def _on_enter(self, event):
        """
        Give the map keyboard focus when mouse enters.
        """

        try:
            self.focus_set()

        except tk.TclError:
            pass

    def _on_mousewheel(self, event):
        """
        Mouse wheel zoom.

        Normal:
            Wheel UP   -> +1
            Wheel DOWN -> -1

        Ctrl + Wheel:
            Slow   -> ±2
            Medium -> ±2
            Fast   -> ±3

        Returning "break" prevents another
        zoom handler from processing the event.
        """

        # =====================================================
        # DETECT WHEEL DIRECTION
        # =====================================================

        event_num = getattr(
            event,
            "num",
            None,
        )

        event_delta = getattr(
            event,
            "delta",
            0,
        )

        # -----------------------------------------------------
        # Linux
        # -----------------------------------------------------

        if event_num == 4:

            direction = 1
            wheel_amount = 1

        elif event_num == 5:

            direction = -1
            wheel_amount = 1

        # -----------------------------------------------------
        # Windows / macOS
        # -----------------------------------------------------

        elif event_delta > 0:

            direction = 1

            wheel_amount = max(
                1,
                int(
                    abs(event_delta) / 120
                ),
            )

        elif event_delta < 0:

            direction = -1

            wheel_amount = max(
                1,
                int(
                    abs(event_delta) / 120
                ),
            )

        else:

            return "break"

        # =====================================================
        # CHECK CTRL
        # =====================================================

        ctrl_pressed = bool(
            getattr(
                event,
                "state",
                0,
            )
            & 0x0004
        )

        # =====================================================
        # NORMAL WHEEL
        # =====================================================

        if not ctrl_pressed:

            self._last_wheel_time = 0.0

            zoom_step = wheel_amount

            new_zoom = (
                self.zoom
                + direction * zoom_step
            )

            self.set_zoom(
                new_zoom
            )

            return "break"

        # =====================================================
        # CTRL + WHEEL
        # =====================================================

        current_time = time.monotonic()

        if self._last_wheel_time == 0.0:

            delta_time = 999.0

        else:

            delta_time = (
                current_time
                - self._last_wheel_time
            )

        self._last_wheel_time = current_time

        # =====================================================
        # DETERMINE SCROLL SPEED
        # =====================================================

        if delta_time < 0.035:

            # Very fast scrolling
            zoom_step = 3

        elif delta_time < 0.080:

            # Medium scrolling
            zoom_step = 2

        else:

            # Slow scrolling
            zoom_step = 2

        zoom_step *= wheel_amount

        # =====================================================
        # APPLY ZOOM
        # =====================================================

        new_zoom = (
            self.zoom
            + direction * zoom_step
        )

        self.set_zoom(
            new_zoom
        )

        return "break"

    # =========================================================
    # PROVIDER
    # =========================================================

    def set_tile_provider(
        self,
        url,
        attribution="",
        max_zoom=19,
    ):
        """
        Set exactly ONE tile provider.

        Calling this replaces the current tile source.
        """

        self.set_tile_server(
            url,
            max_zoom=max_zoom,
        )

        self._attribution = (
            attribution or ""
        )

    def get_attribution(self):
        return self._attribution

    # =========================================================
    # VIEW
    # =========================================================

    def set_center(
        self,
        lat,
        lon,
    ):
        """
        Set map center.
        """

        self.set_position(
            float(lat),
            float(lon),
        )

    def set_zoom(
        self,
        zoom,
        relative_pointer_x=None,
        relative_pointer_y=None,
        **kwargs,
    ):
        """
        Set zoom level with safety limits.

        Compatible with TkinterMapView's internal
        mouse zoom implementation.

        IMPORTANT:
        During TkinterMapView initialization,
        relative_pointer_x/y can be None.

        In that case they must NOT be passed to
        the parent set_zoom().
        """

        # =====================================================
        # VALIDATE ZOOM
        # =====================================================

        try:

            zoom = int(zoom)

        except (
            TypeError,
            ValueError,
        ):

            zoom = self.HOME_ZOOM

        # =====================================================
        # LIMIT ZOOM
        # =====================================================

        zoom = max(
            self.MIN_ZOOM,
            min(
                self.MAX_ZOOM,
                zoom,
            ),
        )

        # =====================================================
        # NORMAL ZOOM
        # =====================================================

        if (
            relative_pointer_x is None
            or relative_pointer_y is None
        ):

            # Do NOT pass None values to
            # TkinterMapView.
            return super().set_zoom(
                zoom,
                **kwargs,
            )

        # =====================================================
        # MOUSE-POSITION ZOOM
        # =====================================================

        return super().set_zoom(
            zoom,
            relative_pointer_x=relative_pointer_x,
            relative_pointer_y=relative_pointer_y,
            **kwargs,
        )

    def zoom_in(self):
        """
        Zoom in one level.
        """

        self.set_zoom(
            self.zoom + 1
        )

    def zoom_out(self):
        """
        Zoom out one level.
        """

        self.set_zoom(
            self.zoom - 1
        )

    def go_home(self):
        """
        Return to initial RIGEL map position.
        """

        self.set_position(
            self.HOME_LAT,
            self.HOME_LON,
        )

        self.set_zoom(
            self.HOME_ZOOM
        )

    def center_uav(
        self,
        lat,
        lon,
        zoom=None,
    ):
        """
        Center map on UAV position.
        """

        self.set_position(
            float(lat),
            float(lon),
        )

        if zoom is not None:

            self.set_zoom(
                zoom
            )

    # =========================================================
    # KEYBOARD HELPERS
    # =========================================================

    def _zoom_and_break(
        self,
        direction,
    ):
        """
        Keyboard zoom helper.
        """

        if direction > 0:

            self.zoom_in()

        else:

            self.zoom_out()

        return "break"

    def _go_home_and_break(
        self,
    ):
        """
        Keyboard Home helper.
        """

        self.go_home()

        return "break"

    # =========================================================
    # MARKER
    # =========================================================

    def add_marker(
        self,
        lat,
        lon,
        marker_id,
    ):
        """
        Add a marker to the map.

        Existing marker with the same ID
        will be removed first.
        """

        self.remove_marker(
            marker_id
        )

        marker = self.set_marker(
            float(lat),
            float(lon),
            text=str(marker_id),
        )

        self._markers[
            marker_id
        ] = marker

        return marker

    def update_marker(
        self,
        marker_id,
        lat,
        lon,
    ):
        """
        Update an existing marker.

        If marker does not exist,
        it will be created.
        """

        marker = self._markers.get(
            marker_id
        )

        if marker is None:

            return self.add_marker(
                lat,
                lon,
                marker_id,
            )

        marker.set_position(
            float(lat),
            float(lon),
        )

        return marker

    def remove_marker(
        self,
        marker_id,
    ):
        """
        Remove marker from map.
        """

        marker = self._markers.pop(
            marker_id,
            None,
        )

        if marker is not None:

            marker.delete()

    # =========================================================
    # ROUTE
    # =========================================================

    def draw_route(
        self,
        points,
        route_id="MISSION",
    ):
        """
        Draw route from a list of:

            [(latitude, longitude), ...]
        """

        self.clear_route(
            route_id
        )

        if len(points) < 2:

            return None

        path = self.set_path(
            [
                (
                    float(lat),
                    float(lon),
                )
                for lat, lon in points
            ]
        )

        self._routes[
            route_id
        ] = path

        return path

    def clear_route(
        self,
        route_id="MISSION",
    ):
        """
        Remove route from map.
        """

        path = self._routes.pop(
            route_id,
            None,
        )

        if path is not None:

            path.delete()

    # =========================================================
    # CLEAR MAP OBJECTS
    # =========================================================

    def clear_map_objects(self):
        """
        Remove all markers and routes.
        """

        # -----------------------------------------------------
        # Remove markers
        # -----------------------------------------------------

        for marker_id in list(
            self._markers
        ):

            self.remove_marker(
                marker_id
            )

        # -----------------------------------------------------
        # Remove routes
        # -----------------------------------------------------

        for route_id in list(
            self._routes
        ):

            self.clear_route(
                route_id
            )