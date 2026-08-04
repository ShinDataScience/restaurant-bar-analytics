# Notebooks

Notebooks are for exploration and for explaining a result to a human. Anything that needs to run
on a schedule gets promoted into src/ with tests.

## Naming

    NN_topic_owner.ipynb

Example: 03_loyalty_breakeven_jd.ipynb

## Planned notebooks

| Notebook | Question it answers |
| --- | --- |
| 01_data_profile | What did the POS actually give us, and where are the gaps? |
| 02_rfm_segments | Who are the regulars, and what share of sales do they carry? |
| 03_loyalty_breakeven | What visit lift does the proposed program need to pay for itself? |
| 04_campaign_history | Which past promotions beat their holdout, and by how much? |
| 05_menu_matrix | Which items are stars, plowhorses, puzzles, and dogs? |
| 06_daypart_demand | Where is the unused capacity, and which segment could fill it? |
| 07_offpeak_offer_design | What offer moves Tuesday without discounting Friday? |

## Conventions

- Clear outputs before committing. Notebook diffs are painful enough already.
- No credentials in cells. Read them from the environment.
- Each notebook ends with a short so-what section written for an operator, not an analyst.
  If a notebook cannot produce that section, the analysis is not finished.
