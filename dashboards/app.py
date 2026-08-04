"""Operator dashboard (Streamlit).

The audience is a general manager with ten minutes before service, not an analyst. That constraint
drives every design decision here:

* One screen answers one question. No tabs full of charts nobody reads.
* Every number is paired with what to do about it.
* Anything uncertain is labeled uncertain rather than rendered as a precise-looking figure.

Run with:  streamlit run dashboards/app.py
"""

from __future__ import annotations

import streamlit as st

PAGES = (
    "This week",
    "Guests and segments",
    "Loyalty economics",
    "Campaign results",
    "Menu and margin",
    "Demand forecast",
)


def page_this_week() -> None:
    """Single-screen weekly summary: sales vs forecast, covers, average check, top movers."""
    raise NotImplementedError


def page_guests() -> None:
    """Segment sizes, share of sales by segment, and who is lapsing this week."""
    raise NotImplementedError


def page_loyalty() -> None:
    """Enrollment, liability, breakage, and measured incremental lift against holdout."""
    raise NotImplementedError


def page_campaigns() -> None:
    """Campaign scorecard: incremental visits, incremental margin, cost per incremental visit."""
    raise NotImplementedError


def page_menu() -> None:
    """Menu engineering quadrants with the recommended action per item."""
    raise NotImplementedError


def page_forecast() -> None:
    """Covers and sales forecast by daypart with intervals, plus suggested labor hours."""
    raise NotImplementedError


def main() -> None:
    st.set_page_config(page_title="Venue analytics", layout="wide")
    st.sidebar.title("Venue analytics")
    choice = st.sidebar.radio("View", PAGES)
    st.header(choice)
    st.info("Not implemented yet. See docs/ROADMAP.md for build order.")


if __name__ == "__main__":
    main()
