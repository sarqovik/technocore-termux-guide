#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path

REPO = Path.home() / "technocore-termux-guide"
AGENT = Path.home() / "technocore-did-gameplay" / "technocore_agent.py"
PROOF = REPO / "proof.json"

ROOM = "hx-did-gameplay"
ARTIFACT_URL = "https://github.com/sarqovik/technocore-termux-guide"


def run(cmd, cwd=None):
    try:
        p = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=30
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def check_proof():
    if not PROOF.exists():
        return False, "proof.json tidak ditemukan", None

    try:
        data = json.loads(PROOF.read_text())
        did = data.get("did")
        commit = data.get("commit")

        if not did or not commit:
            return False, "DID/commit tidak lengkap", None

        code, out, err = run(
            ["python", str(AGENT), "verify-proof", str(PROOF)]
        )

        if code == 0 and "valid proof" in out.lower():
            return True, "VALID", did

        return False, (out or err or "proof tidak valid"), did

    except Exception as e:
        return False, f"error membaca proof: {e}", None


def check_git():
    code, commit, err = run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO
    )

    if code != 0:
        return False, "bukan Git repository"

    code, status, err = run(
        ["git", "status", "--porcelain"],
        cwd=REPO
    )

    clean = code == 0 and not status

    code, remote, err = run(
        ["git", "remote", "get-url", "origin"],
        cwd=REPO
    )

    remote_ok = "sarqovik/technocore-termux-guide" in remote

    if clean and remote_ok:
        return True, f"commit {commit}, clean & origin OK"

    if not clean:
        return False, f"working tree masih berubah (commit {commit})"

    return False, f"origin tidak sesuai (commit {commit})"


def check_room(did):
    code, out, err = run(
        ["python", str(AGENT), "read", ROOM]
    )

    if code != 0:
        return False, "gagal membaca room"

    try:
        data = json.loads(out)
        messages = data.get("messages", [])

        matches = [
            m for m in messages
            if m.get("from") == did
            and ARTIFACT_URL in m.get("text", "")
        ]

        if matches:
            latest = matches[-1]
            return True, f"POSTED (seq {latest.get('seq')})"

        return False, "belum ditemukan"

    except Exception as e:
        return False, f"JSON room error: {e}"


def main():
    print()
    print("========================================")
    print("   TECHN0CORE DID GAMEPLAY STATUS")
    print("========================================")
    print()

    proof_ok, proof_msg, did = check_proof()

    if did:
        print(f"DID: {did}")
    else:
        print("DID: tidak ditemukan")

    print()

    print(
        f"1. DID / Proof       "
        f"{'✅ VALID' if proof_ok else '❌ ERROR'}"
    )
    print(f"   {proof_msg}")

    git_ok, git_msg = check_git()
    print(
        f"2. GitHub repository "
        f"{'✅ READY' if git_ok else '❌ CHECK'}"
    )
    print(f"   {git_msg}")

    if did:
        room_ok, room_msg = check_room(did)
        print(
            f"3. Contribution     "
            f"{'✅ POSTED' if room_ok else '❌ NOT FOUND'}"
        )
        print(f"   room: {ROOM} — {room_msg}")
    else:
        print("3. Contribution     ❌ TIDAK BISA DICEK")

    print()
    print("Artifact:")
    print(f"   {ARTIFACT_URL}")
    print()

    if proof_ok and git_ok and did:
        print("STATUS: ✅ CONTRIBUTION CHECK COMPLETE")
    else:
        print("STATUS: ⚠️ MASIH ADA YANG PERLU DICEK")

    print()


if __name__ == "__main__":
    main()
