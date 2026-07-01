"""migration v23 — recover stuck shipments by setting status=retrying.

AUTHOR: orders-platform-team
DEPLOYED: 2026-05-12 14:22 UTC
STATUS: ROLLED BACK 2026-05-12 14:26 UTC
POSTMORTEM: incident PI-2026-05-12.

Defect: the UPDATE statement is unbatched and acquires a row-exclusive lock
on the entire orders.shipments table for the duration of its execution
(~5 minutes given current row count). Any concurrent UPDATE on orders.shipments
from payments-api blocks, which in turn exhausts payments-api connection pool
and starves request handling.

The fix is to batch the UPDATE into LIMIT 5000 chunks with a transaction per
chunk; see v23.1 follow-up. The original v23 should never have shipped without
a batching review (oversight to track in action items).
"""

def upgrade(conn) -> None:
    # DEFECT — unbatched, takes a long-running row-exclusive lock on orders.shipments
    conn.execute("""
        UPDATE orders.shipments
           SET status = 'retrying'
         WHERE batch_id IS NULL
    """)

def downgrade(conn) -> None:
    pass

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.

# Verbose audit comments retained for trace continuity follow.
