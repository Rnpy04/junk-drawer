class FunctionalDependency:
    def __init__(self, left, right):
        self.left = set(left)
        self.right = set(right)
    
    def __str__(self):
        return f"{''.join(sorted(self.left))} -> {''.join(sorted(self.right))}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return self.left == other.left and self.right == other.right
    
    def __hash__(self):
        return hash((frozenset(self.left), frozenset(self.right)))


class MultivaluedDependency:
    def __init__(self, left, right):
        self.left = set(left)
        self.right = set(right)
    
    def __str__(self):
        return f"{''.join(sorted(self.left))} ->> {''.join(sorted(self.right))}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return self.left == other.left and self.right == other.right
    
    def __hash__(self):
        return hash((frozenset(self.left), frozenset(self.right)))


def attribute_closure(attributes, fds, mvds=None):
    closure = set(attributes)
    changed = True
    mvds = mvds or []

    while changed:
        changed = False
        for fd in fds:
            if fd.left.issubset(closure) and not fd.right.issubset(closure):
                closure.update(fd.right)
                changed = True
        for mvd in mvds:
            if mvd.left.issubset(closure) and not mvd.right.issubset(closure):
                closure.update(mvd.right)
                changed = True
    return closure


def is_superkey(attributes, relation, fds, mvds=None):
    return attribute_closure(attributes, fds, mvds) == set(relation)


def find_candidate_keys(relation, fds, mvds=None):
    from itertools import combinations
    all_attrs = set(relation)
    mvds = mvds or []
    candidate_keys = []

    for r in range(1, len(all_attrs)+1):
        for combo in combinations(all_attrs, r):
            attrs = set(combo)
            if is_superkey(attrs, relation, fds, mvds):
                minimal = True
                for key in candidate_keys:
                    if key.issubset(attrs):
                        minimal = False
                        break
                if minimal:
                    candidate_keys = [k for k in candidate_keys if not attrs.issubset(k)]
                    candidate_keys.append(attrs)
    return candidate_keys


def project_fds(fds, attrs):
    return [fd for fd in fds if fd.left.issubset(attrs) and fd.right.issubset(attrs)]


def project_mvds(mvds, attrs):
    return [mvd for mvd in mvds if mvd.left.issubset(attrs) and mvd.right.issubset(attrs)]


def decompose_to_4nf(relation, fds, mvds):
    result = [set(relation)]
    done = False

    while not done:
        done = True
        for i, r in enumerate(result):
            rel_mvds = project_mvds(mvds, r)
            for mvd in rel_mvds:
                if mvd.left & mvd.right:
                    continue  # trivial MVD
                # check if left is superkey for this Ri
                if not is_superkey(mvd.left, r, project_fds(fds, r), project_mvds(mvds, r)):
                    # decomposition needed
                    Ri = result.pop(i)
                    R1 = Ri - mvd.right
                    R2 = mvd.left | mvd.right
                    result.append(R1)
                    result.append(R2)
                    done = False
                    break
            if not done:
                break
    return result



def print_decomposition(relations):
    for i, r in enumerate(relations, 1):
        print(f"  R{i}: {''.join(sorted(r))}")


if __name__ == "__main__":
    print("Enter relation attributes (e.g., ABCD):")
    relation = input().strip().upper()

    fds = []
    print("Enter Functional Dependencies (format AB-C, empty line to finish):")
    while True:
        line = input().strip()
        if not line:
            break
        if '-' in line:
            left, right = line.split("-")
            fds.append(FunctionalDependency(left.strip(), right.strip()))

    mvds = []
    print("Enter Multivalued Dependencies (format AB->>CD, empty line to finish):")
    while True:
        line = input().strip()
        if not line:
            break
        if '->>' in line:
            left, right = line.split("->>")
            mvds.append(MultivaluedDependency(left.strip(), right.strip()))

    print("\nAll Functional Dependencies:")
    for fd in fds:
        print(f"  {fd}")
    print("\nAll Multivalued Dependencies:")
    for mvd in mvds:
        print(f"  {mvd}")

    keys = find_candidate_keys(relation, fds, mvds)
    print("\nCandidate Keys:")
    for i, key in enumerate(keys, 1):
        print(f"  K{i}: {''.join(sorted(key))}")

    decomposition = decompose_to_4nf(relation, fds, mvds)
    print("\n4NF Decomposition:")
    print_decomposition(decomposition)
