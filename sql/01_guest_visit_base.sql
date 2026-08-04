-- Guest visit base table.
--
-- Collapses raw checks into visits and attaches the fields every downstream analysis needs.
-- Written for DuckDB / Postgres syntax. Adjust the interval literal for other engines.
--
-- Design notes:
--   * Checks opened by the same guest within 6 hours are treated as one visit, which handles
--     a tab that moves from the bar to a table and split checks in a single party.
--   * Business date shifts pre-4am activity to the previous day so late night lands correctly.
--   * Tips and tax are excluded from net sales. They are not revenue to the venue.

CREATE OR REPLACE VIEW guest_visits AS
WITH ordered AS (
    SELECT
        c.guest_id,
        c.venue_id,
        c.check_id,
        c.opened_at,
        c.business_date,
        c.daypart,
        c.channel,
        c.net_sales,
        c.gross_margin,
        c.party_size,
        LAG(c.opened_at) OVER (
            PARTITION BY c.guest_id, c.venue_id
            ORDER BY c.opened_at
        ) AS prev_opened_at
    FROM checks c
    WHERE c.is_void = FALSE
      AND c.guest_id IS NOT NULL
),
flagged AS (
    SELECT
        *,
        CASE
            WHEN prev_opened_at IS NULL THEN 1
            WHEN opened_at - prev_opened_at > INTERVAL 6 HOUR THEN 1
            ELSE 0
        END AS is_new_visit
    FROM ordered
),
numbered AS (
    SELECT
        *,
        SUM(is_new_visit) OVER (
            PARTITION BY guest_id, venue_id
            ORDER BY opened_at
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS visit_seq
    FROM flagged
)
SELECT
    guest_id,
    venue_id,
    visit_seq,
    MIN(opened_at)        AS visit_started_at,
    MIN(business_date)    AS business_date,
    MIN(daypart)          AS daypart,
    MIN(channel)          AS channel,
    MAX(party_size)       AS party_size,
    COUNT(*)              AS checks_in_visit,
    SUM(net_sales)        AS visit_net_sales,
    SUM(gross_margin)     AS visit_gross_margin
FROM numbered
GROUP BY guest_id, venue_id, visit_seq;
