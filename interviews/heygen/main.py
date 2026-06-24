"""
Draft-to-Video Processing Challenge

Implement the `optimize_draft` function below.
Then run this file to fetch your test cases, process them, and submit for scoring.

Usage:
    python solution.py
"""

from __future__ import annotations

import itertools
import json
import urllib.request
import urllib.parse
from dataclasses import dataclass, replace
from enum import Enum
from typing import ClassVar

# --- Configuration ---
# The grading server URL (do not modify)
BASE_URL = "https://kilobyte-residency-worshiper.ngrok-free.dev"
# Your email (do not modify — pre-filled by Coderbyte)
EMAIL = "demo@test.com"


# ---------------------------------------------------------------------------
# Data models
#
# The grader speaks JSON (dicts). We parse those dicts into typed models,
# operate on the models, then serialize back. `from_dict` / `to_dict` are the
# only places that touch the wire format, so the optimization logic (step 2)
# can stay in plain typed Python.
# ---------------------------------------------------------------------------


class VisualElementType(str, Enum):
    AVATAR = "avatar"
    SHAPE = "shape"
    IMAGE = "image"
    TEXT = "text"


class InteractivityType(str, Enum):
    LINK = "link"
    JUMP = "jump"


# Position is relative to the canvas: ((x1, y1) bottom-left, (x2, y2) top-right).
# [(0, 0), (1, 1)] covers the entire canvas.
Position = tuple[tuple[float, float], tuple[float, float]]


@dataclass
class Script:
    """What the user types out to be generated into speech audio."""

    text: str
    duration: int

    @classmethod
    def from_dict(cls, d: dict) -> Script:
        return cls(text=d["text"], duration=d["duration"])

    def to_dict(self) -> dict:
        return {"text": self.text, "duration": self.duration}


@dataclass
class VisualElement:
    """Something visible on the canvas during a window of the scene.

    `shape` and `image` elements obscure other visual elements they're on top
    of (higher `z_index` == on top).
    """

    id: str
    type: VisualElementType
    position: Position
    z_index: int
    start_duration: int
    end_duration: int

    @classmethod
    def from_dict(cls, d: dict) -> VisualElement:
        (x1, y1), (x2, y2) = d["position"]
        return cls(
            id=d["id"],
            type=VisualElementType(d["type"]),
            position=((x1, y1), (x2, y2)),
            z_index=d["z_index"],
            start_duration=d["start_duration"],
            end_duration=d["end_duration"],
        )

    def to_dict(self) -> dict:
        (x1, y1), (x2, y2) = self.position
        return {
            "id": self.id,
            "type": self.type.value,
            "position": [[x1, y1], [x2, y2]],
            "z_index": self.z_index,
            "start_duration": self.start_duration,
            "end_duration": self.end_duration,
        }


@dataclass
class InteractiveElement:
    """Base class for interactivities. Only `shape` and `text` visual elements
    can be made interactive. Concrete type is fixed by the subclass."""

    id: str
    visual_element_id: str
    start_duration: int
    end_duration: int

    type: ClassVar[InteractivityType]

    @staticmethod
    def from_dict(d: dict) -> InteractiveElement:
        """Factory that dispatches on the discriminator `type`."""
        t = InteractivityType(d["type"])
        if t is InteractivityType.LINK:
            return LinkInteractiveElement(
                id=d["id"],
                visual_element_id=d["visual_element_id"],
                start_duration=d["start_duration"],
                end_duration=d["end_duration"],
                url=d["url"],
            )
        if t is InteractivityType.JUMP:
            return JumpInteractiveElement(
                id=d["id"],
                visual_element_id=d["visual_element_id"],
                start_duration=d["start_duration"],
                end_duration=d["end_duration"],
                scene_id=d["scene_id"],
                is_blocking=d.get("is_blocking", False),
            )
        raise ValueError(f"Unknown interactivity type: {d['type']!r}")

    def _base_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "visual_element_id": self.visual_element_id,
            "start_duration": self.start_duration,
            "end_duration": self.end_duration,
        }

    def to_dict(self) -> dict:
        raise NotImplementedError


@dataclass
class LinkInteractiveElement(InteractiveElement):
    """Clicking opens `url` in a new tab. `url` must start with "https://"."""

    type: ClassVar[InteractivityType] = InteractivityType.LINK
    url: str = ""

    def to_dict(self) -> dict:
        return {**self._base_dict(), "url": self.url}


@dataclass
class JumpInteractiveElement(InteractiveElement):
    """Clicking jumps the video to `scene_id`.

    If `is_blocking`, the user cannot continue forward unless they click it —
    which can leave some scenes unreachable.
    """

    type: ClassVar[InteractivityType] = InteractivityType.JUMP
    scene_id: str = ""
    is_blocking: bool = False

    def to_dict(self) -> dict:
        return {
            **self._base_dict(),
            "scene_id": self.scene_id,
            "is_blocking": self.is_blocking,
        }


@dataclass
class Scene:
    """A single segment of video, made of visual + interactive elements."""

    id: str
    script: Script
    visual_elements: list[VisualElement]
    interactivities: list[InteractiveElement]
    duration: int

    def is_valid(self) -> bool:
        """Invalid if the duration is not positive, or the script is longer
        than the scene."""
        return self.duration > 0 and self.script.duration <= self.duration

    @classmethod
    def from_dict(cls, d: dict) -> Scene:
        return cls(
            id=d["id"],
            script=Script.from_dict(d["script"]),
            visual_elements=[
                VisualElement.from_dict(v) for v in d.get("visual_elements", [])
            ],
            interactivities=[
                InteractiveElement.from_dict(i) for i in d.get("interactivities", [])
            ],
            duration=d["duration"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "script": self.script.to_dict(),
            "visual_elements": [v.to_dict() for v in self.visual_elements],
            "interactivities": [i.to_dict() for i in self.interactivities],
            "duration": self.duration,
        }


@dataclass
class Draft:
    """Top-level object representing a video project."""

    id: str
    scenes: list[Scene]

    @classmethod
    def from_dict(cls, d: dict) -> Draft:
        return cls(
            id=d["id"],
            scenes=[Scene.from_dict(s) for s in d.get("scenes", [])],
        )

    def to_dict(self) -> dict:
        return {"id": self.id, "scenes": [s.to_dict() for s in self.scenes]}


# ---------------------------------------------------------------------------
# Optimization
# ---------------------------------------------------------------------------


def optimize_draft(draft: dict) -> dict | None:
    """Optimize a draft by removing all non-renderable elements.

    Parses the incoming dict into typed models, runs the optimization, and
    serializes the result back to a dict (or None if the draft is invalid).
    """
    try:
        model = Draft.from_dict(draft)
    except (ValueError, KeyError):
        return None
    optimized = _optimize(model)
    return optimized.to_dict() if optimized is not None else None


def _optimize(draft: Draft) -> Draft | None:
    """Run the optimization pipeline over typed models.

    Pipeline:
      1. Input validation -> bail out (None) on a structurally invalid scene.
      2. Clean + clamp    -> drop unnecessary elements, clamp the survivors.
      3. Overlap check    -> bail out (None) if what actually renders has an
                             illegal overlap.

    A draft is INVALID (returns None) if any of:
      - a scene is invalid (non-positive duration, or script longer than the
        scene);
      - two visible interactive elements overlap;
      - two visible elements overlap at the same z-index with a temporal
        intersection.
    Otherwise the cleaned, clamped draft is returned.
    """
    # 1. Scene-level validity is independent of the elements and short-circuits.
    if any(not scene.is_valid() for scene in draft.scenes):
        return None

    # 2. Remove unnecessary elements and clamp the survivors. Overlap validity
    #    is about what is *visible*, so we evaluate it on the cleaned result.
    scene_ids = {scene.id for scene in draft.scenes}
    cleaned = Draft(
        id=draft.id,
        scenes=[_clean_scene(scene, scene_ids) for scene in draft.scenes],
    )

    # 3. An illegal overlap among the rendered elements invalidates the draft.
    if any(_scene_has_illegal_overlap(scene) for scene in cleaned.scenes):
        return None

    return cleaned


# --- Overlap detection (aspect #2) -----------------------------------------
#
# Two elements "overlap" when they share BOTH positive canvas area AND a
# positive slice of time. Inequalities are strict, so elements that merely
# touch at an edge (space) or at an endpoint (half-open [start, end) time) do
# not count as overlapping.


def _rects_overlap(a: Position, b: Position) -> bool:
    """True if rectangles ``a`` and ``b`` share positive area."""
    (ax1, ay1), (ax2, ay2) = a
    (bx1, by1), (bx2, by2) = b
    return max(ax1, bx1) < min(ax2, bx2) and max(ay1, by1) < min(ay2, by2)


def _windows_overlap(s1: int, e1: int, s2: int, e2: int) -> bool:
    """True if half-open windows [s1, e1) and [s2, e2) share positive length."""
    return max(s1, s2) < min(e1, e2)


def _visible_window(start: int, end: int, scene_duration: int) -> tuple[int, int] | None:
    """Clamp [start, end) into the scene's [0, scene_duration).

    Returns the clamped window, or None if the element does not render at all
    (its clamped window is empty).
    """
    s, e = max(0, start), min(scene_duration, end)
    return (s, e) if s < e else None


def _scene_has_illegal_overlap(scene: Scene) -> bool:
    """Whether a scene contains an overlap that invalidates the whole draft:

      - two visible interactive elements overlap (condition 1); or
      - two visible visual elements on the SAME z-index overlap (condition 3).

    "Visible" means the element actually renders: its window, clamped to the
    scene, is non-empty (and, for an interactivity, the visual element it
    points at exists). Obscuring is not considered here.
    """
    visuals_by_id = {ve.id: ve for ve in scene.visual_elements}

    # Condition 3: two visible visual elements on the same z-index overlap.
    visible_visuals = [
        (ve, w)
        for ve in scene.visual_elements
        if (w := _visible_window(ve.start_duration, ve.end_duration, scene.duration))
    ]
    for (ve_a, wa), (ve_b, wb) in itertools.combinations(visible_visuals, 2):
        if (
            ve_a.z_index == ve_b.z_index
            and _rects_overlap(ve_a.position, ve_b.position)
            and _windows_overlap(*wa, *wb)
        ):
            return True

    # Condition 1: two visible interactive elements overlap. An interactivity is
    # only visible when BOTH its own window AND its visual element's window are
    # active; the effective window is their intersection.
    visible_interactives = []
    for ie in scene.interactivities:
        ve = visuals_by_id.get(ie.visual_element_id)
        if ve is None:
            continue
        eff_start = max(ie.start_duration, ve.start_duration)
        eff_end = min(ie.end_duration, ve.end_duration)
        if eff_start >= eff_end:
            continue  # never simultaneously visible
        visible_interactives.append((ve.position, (eff_start, eff_end)))
    for (pos_a, wa), (pos_b, wb) in itertools.combinations(visible_interactives, 2):
        if _rects_overlap(pos_a, pos_b) and _windows_overlap(*wa, *wb):
            return True

    return False


# --- Cleaning & clamping (aspect #3) ----------------------------------------
#
# A valid draft is returned with all unnecessary elements removed and every
# remaining element clamped to its scene:
#   - visual elements are clamped to [0, scene.duration); empty ones dropped;
#   - a visual element fully covered (in space, for its whole time window) by a
#     higher-z-index shape/image is dropped as obscured;
#   - interactivities are dropped when invalid (target missing or not a
#     shape/text, bad link url, jump to a missing scene, or empty window) and
#     clamped otherwise.


def _contains(outer: Position, inner: Position) -> bool:
    """True if rectangle ``outer`` fully covers ``inner`` (touching edges OK)."""
    (ox1, oy1), (ox2, oy2) = outer
    (ix1, iy1), (ix2, iy2) = inner
    return ox1 <= ix1 and oy1 <= iy1 and ox2 >= ix2 and oy2 >= iy2


def _is_obscured(target: VisualElement, others: list[VisualElement]) -> bool:
    """True if a higher-z-index shape/image fully covers ``target`` in space for
    the whole of ``target``'s (already clamped) time window.

    ``others`` are the scene's clamped, rendering visual elements. Checking
    against the full set (rather than iteratively) is safe: if the covering
    element is itself obscured, whatever obscures *it* also covers ``target``.
    """
    for other in others:
        if other is target:
            continue
        if (
            other.type in (VisualElementType.SHAPE, VisualElementType.IMAGE)
            and other.z_index > target.z_index
            and _contains(other.position, target.position)
            and other.start_duration <= target.start_duration
            and other.end_duration >= target.end_duration
        ):
            return True
    return False


def _interactivity_target_valid(ie: InteractiveElement, scene_ids: set[str]) -> bool:
    """True if a link points at an https:// url, or a jump targets a real scene."""
    if isinstance(ie, LinkInteractiveElement):
        return ie.url.startswith("https://")
    if isinstance(ie, JumpInteractiveElement):
        return ie.scene_id in scene_ids
    return False


def _clean_scene(scene: Scene, scene_ids: set[str]) -> Scene:
    """Return a copy of ``scene`` with unnecessary elements removed and every
    surviving element clamped to the scene's [0, duration)."""
    # Clamp visual elements; drop ones that don't render at all.
    visuals: list[VisualElement] = []
    for ve in scene.visual_elements:
        window = _visible_window(ve.start_duration, ve.end_duration, scene.duration)
        if window is None:
            continue
        start, end = window
        visuals.append(replace(ve, start_duration=start, end_duration=end))

    # Drop visual elements fully obscured by a higher-z-index shape/image.
    visuals = [ve for ve in visuals if not _is_obscured(ve, visuals)]
    visuals_by_id = {ve.id: ve for ve in visuals}

    # Clean + clamp interactivities.
    interactivities: list[InteractiveElement] = []
    for ie in scene.interactivities:
        target = visuals_by_id.get(ie.visual_element_id)
        if target is None:
            continue  # attached to a missing or removed visual element
        if target.type not in (VisualElementType.SHAPE, VisualElementType.TEXT):
            continue  # only shape and text can be interactive
        if not _interactivity_target_valid(ie, scene_ids):
            continue  # bad link url or jump to a non-existent scene
        window = _visible_window(ie.start_duration, ie.end_duration, scene.duration)
        if window is None:
            continue  # empty / entirely outside the scene
        start, end = window
        # Non-renderable if its window never overlaps its visual element's window.
        if start >= target.end_duration or end <= target.start_duration:
            continue
        interactivities.append(replace(ie, start_duration=start, end_duration=end))

    return replace(scene, visual_elements=visuals, interactivities=interactivities)


def visualize_draft(draft: dict) -> None:
    """POST a draft to the visualizer and print the URL."""
    payload = json.dumps({"email": EMAIL, "draft": draft}).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/visualize",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        url = json.loads(resp.read())["url"]
    print(f"Visualization: {BASE_URL}{url}")


def main():
    # Fetch test cases
    print(f"Fetching test cases for {EMAIL}...")
    query = urllib.parse.urlencode({"email": EMAIL})
    with urllib.request.urlopen(f"{BASE_URL}/tests?{query}") as resp:
        drafts = json.loads(resp.read())["drafts"]
    print(f"Received {len(drafts)} drafts.")

    # # Visualize each draft
    # for i, draft in enumerate(drafts):
    #     print(f"Visualizing draft {i} ({draft['id']})...")
    #     visualize_draft(draft)

    # Process each draft
    results = []
    for i, draft in enumerate(drafts):
        result = optimize_draft(draft)
        results.append(result)
        status = "None" if result is None else "optimized"
        print(f"  Draft {i} ({draft['id']}): {status}")

    # Submit results
    print("Submitting results...")
    payload = json.dumps({"email": EMAIL, "results": results}).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/evaluate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    print(f"\nScore (improvement over baseline): {data['total_score']}")


if __name__ == "__main__":
    main()
