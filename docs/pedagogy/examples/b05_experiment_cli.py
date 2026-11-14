"""B05 hands-on command line experiment. Does not access physical memory."""
import argparse
import json
from b05_frames import FrameAllocator, OutOfFrames

def simulate(frames, operations):
    if len(set(frames)) != len(frames) or any(frame < 0 for frame in frames):
        raise ValueError("frames must be unique nonnegative integers")
    allocator = FrameAllocator(frames)
    trace = []
    for operation in operations:
        if operation == "alloc":
            try:
                frame = allocator.alloc()
                trace.append({"op": "alloc", "frame": frame, "status": "PASS"})
            except OutOfFrames:
                trace.append({"op": "alloc", "status": "EXHAUSTED"})
        elif operation.startswith("free:"):
            try:
                frame = int(operation.split(":", 1)[1])
            except ValueError as exc:
                raise ValueError("free expects an integer frame") from exc
            try:
                allocator.release(frame)
                trace.append({"op": "free", "frame": frame, "status": "PASS"})
            except ValueError:
                trace.append({"op": "free", "frame": frame, "status": "INVALID_FREE"})
        else:
            raise ValueError(f"unknown operation: {operation}")
    return trace

def main(argv=None):
    parser = argparse.ArgumentParser(description="B05 educational frame allocator experiment")
    parser.add_argument("--frames", default="2,4,6", help="comma-separated nonnegative frames")
    parser.add_argument("--ops", default="alloc,alloc,alloc,alloc,free:4,alloc")
    args = parser.parse_args(argv)
    try:
        frames = [int(item) for item in args.frames.split(",") if item]
        operations = [item.strip() for item in args.ops.split(",") if item.strip()]
        result = simulate(frames, operations)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
