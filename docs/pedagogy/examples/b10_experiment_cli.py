"""B10 in-memory block experiment with explicit data-integrity controls."""
import argparse
import hashlib
import json
from b10_blocks import split_blocks, join_blocks, block_count

def experiment(data, block_size, drop_last=False):
    blocks = split_blocks(data, block_size)
    recovered = join_blocks(blocks[:-1] if drop_last else blocks)
    return {
        "input_bytes": len(data),
        "block_size": block_size,
        "blocks": len(blocks),
        "expected_blocks": block_count(len(data), block_size),
        "input_sha256": hashlib.sha256(data).hexdigest(),
        "recovered_sha256": hashlib.sha256(recovered).hexdigest(),
        "integrity": "PASS" if recovered == data else "FAIL",
        "negative_control": drop_last,
    }

def main(argv=None):
    parser = argparse.ArgumentParser(description="B10 in-memory block integrity experiment")
    parser.add_argument("--text", default="hello from under the hood")
    parser.add_argument("--block-size", type=int, default=8)
    parser.add_argument("--drop-last", action="store_true", help="intentional data loss control")
    args = parser.parse_args(argv)
    try:
        result = experiment(args.text.encode("utf-8"), args.block_size, args.drop_last)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["integrity"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
