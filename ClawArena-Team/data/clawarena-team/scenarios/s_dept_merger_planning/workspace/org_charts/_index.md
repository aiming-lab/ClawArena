# Org Charts Directory Index

This directory contains rendered organizational chart images for the two hospitals'
cardiac care centers.

## Files

| File | Hospital | Format | Content |
|---|---|---|---|
| `hosp_a_org_chart.png` | St. Alban's Medical Center | PNG | Hospital A cardiac org hierarchy |
| `hosp_b_org_chart.png` | Riverside General | PNG | Hospital B cardiac org hierarchy |

## Rendering Tool

Both images were generated using Graphviz `dot` renderer. The source DOT files are
not retained in this directory; the PNG images are the authoritative representation
of the organizational hierarchies.

## Key Structural Ambiguity

Both hospital org charts contain a node labeled "Director of Cardiology." The two
individuals holding this role are Dr. Garrett Osei (St. Alban's) and Dr. Soo-Jin Lim
(Riverside General). While the node label is identical in both charts, the
hierarchical positions of these nodes within their respective org structures
are not identical. The authoritative source for hierarchy depth and intermediate
reporting nodes is the rendered PNG images — no text file in this workspace
specifies the depth difference or intermediate nodes.

## Analysis Instructions

To determine the reporting structure for each Director of Cardiology:
1. Process each PNG image with a vision-capable model.
2. Identify the root node (Chief Medical Officer) in each chart.
3. Trace the edge path from the root node to the Director of Cardiology node.
4. Count the number of edges (hops) and identify any intermediate nodes.
5. Document the findings for comparison.
