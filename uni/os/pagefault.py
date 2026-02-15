from collections import deque, Counter

def fifo(pages, frames_count):
    frames = deque()
    hits, misses = 0, 0

    print("\nFIFO PAGE REPLACEMENT")
    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            misses += 1
            status = "Miss"
            if len(frames) < frames_count:
                frames.append(page)
            else:
                frames.popleft()
                frames.append(page)
        print(f"Step {i+1}: Page {page} -> {status}, Frames: {list(frames)}")
    return hits, misses

def lru(pages, frames_count):
    frames = []
    hits, misses = 0, 0
    recent = []

    print("\nLRU PAGE REPLACEMENT")
    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            misses += 1
            status = "Miss"
            if len(frames) < frames_count:
                frames.append(page)
            else:
                # Remove least recently used
                lru_page = recent.pop(0)
                frames.remove(lru_page)
                frames.append(page)
        if page in recent:
            recent.remove(page)
        recent.append(page)
        print(f"Step {i+1}: Page {page} -> {status}, Frames: {frames}")
    return hits, misses

def mru(pages, frames_count):
    frames = []
    hits, misses = 0, 0
    recent = []

    print("\nMRU PAGE REPLACEMENT")
    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            misses += 1
            status = "Miss"
            if len(frames) < frames_count:
                frames.append(page)
            else:
                # Remove most recently used
                mru_page = recent[-1]
                frames.remove(mru_page)
                frames.append(page)
        if page in recent:
            recent.remove(page)
        recent.append(page)
        print(f"Step {i+1}: Page {page} -> {status}, Frames: {frames}")
    return hits, misses

def lfu(pages, frames_count):
    frames = []
    freq = Counter()
    hits, misses = 0, 0

    print("\nLFU PAGE REPLACEMENT")
    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            misses += 1
            status = "Miss"
            if len(frames) < frames_count:
                frames.append(page)
            else:
                # Remove least frequently used
                lfu_page = min(frames, key=lambda x: freq[x])
                frames.remove(lfu_page)
                frames.append(page)
        freq[page] += 1
        print(f"Step {i+1}: Page {page} -> {status}, Frames: {frames}, Freq: {dict(freq)}")
    return hits, misses

def mfu(pages, frames_count):
    frames = []
    freq = Counter()
    hits, misses = 0, 0

    print("\nMFU PAGE REPLACEMENT")
    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            misses += 1
            status = "Miss"
            if len(frames) < frames_count:
                frames.append(page)
            else:
                # Remove most frequently used
                mfu_page = max(frames, key=lambda x: freq[x])
                frames.remove(mfu_page)
                frames.append(page)
        freq[page] += 1
        print(f"Step {i+1}: Page {page} -> {status}, Frames: {frames}, Freq: {dict(freq)}")
    return hits, misses

def opt(pages, frames_count):
    frames = []
    hits, misses = 0, 0

    print("\nOPTIMAL PAGE REPLACEMENT")
    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            misses += 1
            status = "Miss"
            if len(frames) < frames_count:
                frames.append(page)
            else:
                # Remove page which is not used for the longest future
                future = pages[i+1:]
                indices = {}
                for f in frames:
                    if f in future:
                        indices[f] = future.index(f)
                    else:
                        indices[f] = float('inf')
                to_remove = max(indices, key=indices.get)
                frames.remove(to_remove)
                frames.append(page)
        print(f"Step {i+1}: Page {page} -> {status}, Frames: {frames}")
    return hits, misses
def run_simulation(pages, frames_count, algorithm):
    algo_map = {
        "FIFO": fifo,
        "LRU": lru,
        "MRU": mru,
        "LFU": lfu,
        "MFU": mfu,
        "OPT": opt
    }

    if algorithm.upper() == "ALL":
        for name, algo in algo_map.items():
            hits, misses = algo(pages, frames_count)
            print(f"\n{name} -> Total Hits: {hits}, Total Misses: {misses}, Page Fault Rate: {misses/len(pages):.2f}")
            print("-" * 60)
    else:
        algo = algo_map.get(algorithm.upper())
        if not algo:
            print("Algorithm not found! Choose from FIFO, LRU, MRU, LFU, MFU, OPT, ALL.")
            return
        hits, misses = algo(pages, frames_count)
        print(f"\nTotal Hits: {hits}, Total Misses: {misses}, Page Fault Rate: {misses/len(pages):.2f}")

# Example usage
if __name__ == "__main__":
    pages = list(map(int, input("Enter page reference string (space separated): ").split()))
    frames_count = int(input("Enter number of frames: "))
    algorithm = input("Enter algorithm (FIFO, LRU, MRU, LFU, MFU, OPT, ALL): ")

    run_simulation(pages, frames_count, algorithm)
