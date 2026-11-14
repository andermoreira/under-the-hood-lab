"""B06 virtual-address translation experiment, not an MMU emulator."""
import argparse
import json
from b06_paging import PAGE_SIZE, PageFault, translate, write_address

def experiment(entries, requests):
    table = {}
    for page, frame, writable in entries:
        if page < 0 or frame < 0 or page in table:
            raise ValueError("page and frame must be nonnegative; pages unique")
        table[page] = (frame, bool(writable))
    results = []
    for operation, address in requests:
        if operation not in ("read", "write"):
            raise ValueError("operation must be read or write")
        try:
            physical = (translate if operation == "read" else write_address)(address, table)
            results.append({"op": operation, "virtual": address, "physical": physical, "status": "PASS"})
        except (PageFault, ValueError) as exc:
            results.append({"op": operation, "virtual": address, "status": "FAULT", "reason": str(exc)})
    return results

def main(argv=None):
    parser = argparse.ArgumentParser(description="B06 pedagogical paging experiment")
    parser.add_argument("--map", default="2:7:ro,3:9:rw", help="page:frame:ro|rw,...")
    parser.add_argument("--requests", default="read:8197,write:8197,write:12288,read:0")
    args = parser.parse_args(argv)
    try:
        entries = []
        for item in args.map.split(","):
            page, frame, permission = item.split(":")
            if permission not in ("ro", "rw"):
                raise ValueError("permission must be ro or rw")
            entries.append((int(page), int(frame), permission == "rw"))
        requests = []
        for item in args.requests.split(","):
            op, address = item.split(":")
            requests.append((op, int(address)))
        result = experiment(entries, requests)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps({"page_size": PAGE_SIZE, "trace": result}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
