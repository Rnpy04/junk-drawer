from itertools import permutations

# ----------------- FCFS -----------------
def fcfs(requests, head_start):
    order = []
    head = head_start
    total_movement = 0

    for r in requests:
        order.append(r)
        total_movement += abs(head - r)
        head = r

    return [(order, total_movement)]

# ----------------- SSTF -----------------
def sstf(requests, head_start):
    # Recursive helper to generate all paths in case of tie
    def helper(reqs, head):
        if not reqs:
            return [([], 0)]
        paths = []
        # Find minimum distance
        distances = [abs(head - r) for r in reqs]
        min_dist = min(distances)
        # All candidates at minimum distance
        candidates = [r for r, d in zip(reqs, distances) if d == min_dist]
        for c in candidates:
            remaining = reqs.copy()
            remaining.remove(c)
            subpaths = helper(remaining, c)
            for sp_order, sp_mov in subpaths:
                paths.append(([c]+sp_order, abs(head-c)+sp_mov))
        return paths

    all_paths = helper(requests, head_start)
    # Remove duplicates if any
    unique_paths = []
    seen = set()
    for order, movement in all_paths:
        tup = tuple(order)
        if tup not in seen:
            seen.add(tup)
            unique_paths.append((order, movement))
    return unique_paths

# ----------------- SCAN -----------------
def scan(requests, head_start, disk_size, direction="up"):
    requests = sorted(requests)
    

    if direction == "up":
        up = [r for r in requests if r >= head_start]
        down = [r for r in requests if r < head_start][::-1]
        order = []
        head = head_start
        total_movement = 0

        # move up
        for r in up:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        # move to end
        if down:
            total_movement += abs(head - (disk_size-1))
            head = disk_size-1
            # move down
            for r in down:
                total_movement += abs(head - r)
                head = r
                order.append(r)
        return [(order, total_movement)]
    else:
        down = [r for r in requests if r <= head_start][::-1]
        up = [r for r in requests if r > head_start]
        order = []
        head = head_start
        total_movement = 0

        # move down
        for r in down:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        # move to start
        if up:
            total_movement += abs(head - 0)
            head = 0
            # move up
            for r in up:
                total_movement += abs(head - r)
                head = r
                order.append(r)

        return [(order, total_movement)]


# ----------------- C-SCAN -----------------
def c_scan(requests, head_start, disk_size, direction="up"):
    requests = sorted(requests)
    head = head_start

    if direction == "up":
        up = [r for r in requests if r >= head]
        down = [r for r in requests if r < head]

        order = []
        total_movement = 0

        for r in up:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        if down:
            total_movement += abs(head - (disk_size-1))  # move to end
            head = 0  # jump to start
            total_movement += disk_size-1  # count jump
            for r in down:
                total_movement += abs(head - r)
                head = r
                order.append(r)
        return [(order, total_movement)]

    else:  # direction down
        down = [r for r in requests if r <= head][::-1]
        up = [r for r in requests if r > head]

        order = []
        total_movement = 0
        for r in down:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        if up:
            total_movement += abs(head - 0)  # move to start
            head = disk_size-1  # jump to end
            total_movement += disk_size-1
            for r in up[::-1]:
                total_movement += abs(head - r)
                head = r
                order.append(r)
        return [(order, total_movement)]

# ----------------- LOOK -----------------
def look(requests, head_start, direction="up"):
    requests = sorted(requests)
    if direction == "up":
        up = [r for r in requests if r >= head_start]
        down = [r for r in requests if r < head_start][::-1]
        order = []
        total_movement = 0
        head = head_start
        for r in up:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        for r in down:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        return [(order, total_movement)]
    else:
        down = [r for r in requests if r <= head_start][::-1]
        up = [r for r in requests if r > head_start]
        order = []
        total_movement = 0
        head = head_start
        for r in down:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        for r in up:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        return [(order, total_movement)]

# ----------------- C-LOOK -----------------
def c_look(requests, head_start, direction="up"):
    requests = sorted(requests)
    head = head_start

    if direction == "up":
        up = [r for r in requests if r >= head]
        down = [r for r in requests if r < head]
        order = []
        total_movement = 0
        for r in up:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        if down:
            total_movement += abs(head - down[0])
            head = down[0]
            order.append(head)
            for r in down[1:]:
                total_movement += abs(head - r)
                head = r
                order.append(r)
        return [(order, total_movement)]
    else:
        down = [r for r in requests if r <= head][::-1]
        up = [r for r in requests if r > head]
        order = []
        total_movement = 0
        for r in down:
            total_movement += abs(head - r)
            head = r
            order.append(r)
        if up:
            total_movement += abs(head - up[-1])
            head = up[-1]
            order.append(head)
            for r in up[:-1][::-1]:
                total_movement += abs(head - r)
                head = r
                order.append(r)
        return [(order, total_movement)]

# ----------------- RUN SIMULATION -----------------
def run_disk_simulation(requests, head_start, disk_size):
    algo_map = {
        "FCFS": fcfs,
        "SSTF": sstf,
        "SCAN": scan,
        "C-SCAN": c_scan,
        "LOOK": look,
        "C-LOOK": c_look
    }

    for name, algo in algo_map.items():
            print(f"\n{name}:")
            if name in ["SCAN", "C-SCAN", "LOOK", "C-LOOK"]:
                # two directions
                for dir in ["up", "down"]:
                    paths = algo(requests, head_start, disk_size,dir) if "AN" in name else algo(requests, head_start, dir)
                    for order, movement in paths:
                        print(f"  Direction {dir}: Order: {order}, Total Head Movement: {movement}")
            else:
                paths = algo(requests, head_start)
                for order, movement in paths:
                    print(f"  Order: {order}, Total Head Movement: {movement}")
            print("-"*60)

# ----------------- MAIN -----------------
if __name__ == "__main__":
    requests = list(map(int, input("Enter disk requests (space separated): ").split()))
    head_start = int(input("Enter initial head position: "))
    disk_size = int(input("Enter disk size (max cylinder number + 1): "))

    run_disk_simulation(requests, head_start, disk_size)
