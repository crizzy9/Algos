These are the main requirements for the functioning of the system
We need to build the optmize_draft method in a way that incorporates the following aspects

1. Input Validation
2. Identify overlaps based on position, time and zindex
3. Duration Clamping

- if the draft is invalid, return None.
  A draft is invalid if:

- two or more visible interactive elements overlap
- there is any invalid scenes.
- two or more visible elements overlap at the same z-index with temporal intersection
- if the script duration is longer than the scene duration

Otherwise, returned a cleaned draft, removing all unnecessary elements and properly clamping the duration.
Duration clamping - If a visual element / interactivity does not fit in it’s required time duration, clamp it within it’s duration.
If an interactivity is invalid, remove the interactivity.

We must not touch the main method or the visualize_draft method those are for testing only and will be used to the run the code in a separate system

---

To verify everything is working as intended we must need to check the following aspects of the solution

Positive Testing:
For every element removed from a draft, we add one point per second saved per element.
We need to check for every element removed from a draft it is
For every second saved from the draft, we add 10 point per second shaved off the final draft.

Deducting points:

    If the draft is returned when it should not have been - we deduct points based on the duration of the draft returned
    We’ve wasted resources
    If the draft returned removes an element that should be in the final video or you return None when there should have been a draft - we deduct 1000 points.
    We’ve lost user trust.

Your final score is the total difference in points your optimized approach has vs the base case of not doing anything.
