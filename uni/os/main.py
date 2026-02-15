# ===============================
# OS Memory Management Simulator
# ===============================

from collections import deque

# -------------------------------
# 1) Base & Limit Protection
# -------------------------------
def base_limit_protection():
    base = int(input("Enter Base Register value: "))
    limit = int(input("Enter Limit Register value: "))
    address = int(input("Enter Logical Address: "))

    if base <= address < base + limit:
        print("✅ Access Granted")
        physical_address = address
        print(f"Physical Address = {physical_address}")
    else:
        print("❌ TRAP: Memory Protection Fault")


# -------------------------------
# 2) Contiguous Allocation
# -------------------------------
def first_fit(holes, request):
    for i, hole in enumerate(holes):
        if hole >= request:
            holes[i] -= request
            return True
    return False

def best_fit(holes, request):
    best_index = -1
    best_size = float('inf')

    for i, hole in enumerate(holes):
        if request <= hole < best_size:
            best_size = hole
            best_index = i

    if best_index != -1:
        holes[best_index] -= request
        return True
    return False

def worst_fit(holes, request):
    worst_index = -1
    worst_size = -1

    for i, hole in enumerate(holes):
        if hole >= request and hole > worst_size:
            worst_size = hole
            worst_index = i

    if worst_index != -1:
        holes[worst_index] -= request
        return True
    return False

def contiguous_allocation():
    holes = list(map(int, input("Enter hole sizes (space separated): ").split()))
    request = int(input("Enter process size: "))

    print("""
Choose Allocation Algorithm:
1. First Fit
2. Best Fit
3. Worst Fit
""")
    choice = input("Choice: ")

    if choice == "1":
        result = first_fit(holes, request)
    elif choice == "2":
        result = best_fit(holes, request)
    elif choice == "3":
        result = worst_fit(holes, request)
    else:
        print("Invalid choice")
        return

    print("✅ Allocated" if result else "❌ Allocation Failed")
    print("Remaining Holes:", holes)


# -------------------------------
# 3) Paging + Page Table
# -------------------------------
def paging_system():
    page_size = int(input("Enter Page Size: "))
    logical_address = int(input("Enter Logical Address: "))

    page_number = logical_address // page_size
    offset = logical_address % page_size

    print(f"Page Number = {page_number}")
    print(f"Offset = {offset}")

    page_table = {}
    n = int(input("How many page table entries? "))

    for _ in range(n):
        p, f = map(int, input("Page Frame: ").split())
        page_table[p] = f

    if page_number not in page_table:
        print("❌ Page Fault")
        return

    frame = page_table[page_number]
    physical_address = frame * page_size + offset

    print(f"✅ Physical Address = {physical_address}")


# -------------------------------
# 4) TLB (Fully Associative)
# -------------------------------
def tlb_simulator():
    tlb = {}
    size = int(input("TLB size: "))

    while True:
        page = int(input("Enter Page Number (-1 to exit): "))
        if page == -1:
            break

        if page in tlb:
            print(f"✅ TLB HIT → Frame {tlb[page]}")
        else:
            print("❌ TLB MISS")
            frame = int(input("Enter Frame Number: "))
            if len(tlb) >= size:
                removed = next(iter(tlb))
                del tlb[removed]
            tlb[page] = frame


# -------------------------------
# 5) Page Replacement
# -------------------------------
def fifo(pages, frames):
    memory = deque()
    faults = 0

    for page in pages:
        if page not in memory:
            faults += 1
            if len(memory) >= frames:
                memory.popleft()
            memory.append(page)

    return faults

def lru(pages, frames):
    memory = []
    faults = 0

    for page in pages:
        if page not in memory:
            faults += 1
            if len(memory) >= frames:
                memory.pop(0)
        else:
            memory.remove(page)
        memory.append(page)

    return faults

def second_chance(pages, frames):
    memory = deque()
    ref_bits = {}
    pointer = 0
    faults = 0

    for page in pages:
        if page in memory:
            ref_bits[page] = 1
            continue

        faults += 1
        while len(memory) >= frames:
            victim = memory[0]
            if ref_bits[victim] == 0:
                memory.popleft()
                del ref_bits[victim]
                break
            else:
                ref_bits[victim] = 0
                memory.rotate(-1)

        memory.append(page)
        ref_bits[page] = 1

    return faults

def page_replacement():
    pages = list(map(int, input("Enter page reference string: ").split()))
    frames = int(input("Number of frames: "))

    print("""
Choose Algorithm:
1. FIFO
2. LRU
3. Second Chance
""")
    choice = input("Choice: ")

    if choice == "1":
        print("Page Faults:", fifo(pages, frames))
    elif choice == "2":
        print("Page Faults:", lru(pages, frames))
    elif choice == "3":
        print("Page Faults:", second_chance(pages, frames))
    else:
        print("Invalid choice")


# -------------------------------
# MAIN MENU
# -------------------------------
def main():
    while True:
        print("""
====== OS Memory Management Simulator ======
1. Base & Limit Protection
2. Contiguous Allocation
3. Paging
4. TLB Simulation
5. Page Replacement
0. Exit
""")
        choice = input("Select: ")

        if choice == "1":
            base_limit_protection()
        elif choice == "2":
            contiguous_allocation()
        elif choice == "3":
            paging_system()
        elif choice == "4":
            tlb_simulator()
        elif choice == "5":
            page_replacement()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

main()
