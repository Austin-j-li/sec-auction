# Proposed: temporary files off the root disk (not applied)

A proposal for Austin, from the v1.14 upgrade (spec §7.11, audit B13). Nothing here is installed. Install it only at deploy window step 6a (spec §12), and only if Austin approves.

## Why

- The root filesystem holds `/tmp`. It was 97% full on 25 September (audit B13) and 82% full, with 1.7 GB free, at 20:45 UTC the same day. `/home/uctpiaj/work` has over 300 GB free.
- Neither service sets `TMPDIR`, so their temporary files land in `/tmp`:
  - the server writes each edited working copy to a `cockpit-check-*` folder to check it (`workspace.py`, `_payload`);
  - the worker's runner keeps each run's provider state and scratch home in `sec-extraction-state-*` and `sec-extraction-scratch-*` for the whole run (`sandbox/run_model.py`, `worker()`); Claude and Codex sign-ins and the Codex refresh inherit the same environment.
- The extraction sandbox is unaffected: bubblewrap clears the environment, binds the run's scratch folder at `/tmp` and sets `TMPDIR=/tmp` inside (`run_model.py`, `bwrap_base`).

## The change

Two drop-in files, one per service, each with these two lines:

```
[Service]
Environment=TMPDIR=%h/work/tmp
```

- `~/.config/systemd/user/ledger-cockpit.service.d/30-tmpdir.conf`
- `~/.config/systemd/user/ledger-worker.service.d/30-tmpdir.conf`

Drop-ins leave the unit files, and their reference copies in this folder, unchanged. `%h` is the user's home. The nightly backup unit needs no change: it writes to `~/backups/ledger-cockpit/`, not to `TMPDIR`.

## Install (window step 6a, after the deploy patch and before the server restart in step 7)

```bash
mkdir -p ~/work/tmp
for unit in ledger-cockpit ledger-worker; do
  mkdir -p ~/.config/systemd/user/$unit.service.d
  printf '[Service]\nEnvironment=TMPDIR=%%h/work/tmp\n' > ~/.config/systemd/user/$unit.service.d/30-tmpdir.conf
done
cat ~/.config/systemd/user/ledger-*.service.d/30-tmpdir.conf     # each shows Environment=TMPDIR=%h/work/tmp
systemctl --user daemon-reload
systemctl --user show -p Environment ledger-cockpit ledger-worker   # both Environment= lines include TMPDIR=
```

The running processes keep their old environment until the restarts in steps 7 and 9. After step 9:

```bash
for unit in ledger-cockpit ledger-worker; do
  tr '\0' '\n' < /proc/$(systemctl --user show -p MainPID --value $unit)/environ | grep '^TMPDIR='
done
```

At the commit of gate 3a, copy the two installed drop-ins into this folder (`ledger-cockpit.service.d/30-tmpdir.conf`, `ledger-worker.service.d/30-tmpdir.conf`), so that the reference copies match what is installed.

## Rollback

```bash
rm ~/.config/systemd/user/ledger-cockpit.service.d/30-tmpdir.conf ~/.config/systemd/user/ledger-worker.service.d/30-tmpdir.conf
rmdir ~/.config/systemd/user/ledger-worker.service.d
systemctl --user daemon-reload
systemctl --user restart ledger-cockpit.service && systemctl --user restart ledger-worker.service
```

Do not remove `ledger-cockpit.service.d/`: it holds `20-public-origin.conf`.

## Housekeeping

`systemd-tmpfiles` ages out `/tmp` after 10 days but does not clean `~/work/tmp`, which other sessions and tools share. The folders above are removed when their request or run ends; a killed process can leave one behind. Remove leftovers named `cockpit-check-*`, `sec-extraction-state-*` or `sec-extraction-scratch-*` only while no job is running (window step 1's check), and nothing else there.
