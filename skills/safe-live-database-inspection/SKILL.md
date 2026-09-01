---
name: safe-live-database-inspection
description: Inspect application-owned SQLite state safely without bypassing the supported write surface.
compatibility: Requires Python 3 with sqlite3 and filesystem access to the same disposable desktop workspace as the application.
---

Use SQLite from the shell for inspection, not as an unsupported mutation path.

1. Locate the database used by the running application and check for `-wal` and `-shm` companions.
2. Create a consistent snapshot with SQLite's backup API before querying. Do not copy only the main file while the app
   is live; that can omit committed WAL state or produce inconsistent evidence.
3. Open the snapshot read-only, inspect the schema first, and make bounded queries that select only fields needed for
   the task. Avoid dumping secrets or unrelated user data.
4. Make requested changes through the application's supported UI or API unless the task explicitly authorizes direct
   database maintenance and you understand its invariants.
5. Reinspect a fresh snapshot after the application change. A successful shell query does not prove the application
   accepted or persisted the mutation.

A minimal snapshot command using only Python's standard library is:

```bash
python -c 'import sqlite3,sys; s=sqlite3.connect(sys.argv[1]); d=sqlite3.connect(sys.argv[2]); s.backup(d); d.close(); s.close()' SOURCE.db SNAPSHOT.db
```
