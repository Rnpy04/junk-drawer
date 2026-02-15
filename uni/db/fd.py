class FunctionalDependency:
    def __init__(self, left, right):
        self.left = set(left)
        self.right = set(right)
    
    def __str__(self):
        return f"{''.join(sorted(self.left))} → {''.join(sorted(self.right))}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return self.left == other.left and self.right == other.right
    
    def __hash__(self):
        return hash((frozenset(self.left), frozenset(self.right)))

def attribute_closure(attributes, fds):
    """Compute closure of a set of attributes under given FDs"""
    closure = set(attributes)
    changed = True
    
    while changed:
        changed = False
        for fd in fds:
            if fd.left.issubset(closure) and not fd.right.issubset(closure):
                closure.update(fd.right)
                changed = True
    return closure

def compute_closure_fds(fds):
    """Compute F+ (all FDs implied by given FDs)"""
    F_plus = set(fds)
    all_attributes = set()
    
    # Get all attributes
    for fd in fds:
        all_attributes.update(fd.left)
        all_attributes.update(fd.right)
    
    # Apply reflexivity: If Y ⊆ X, then X → Y
    for i in range(1, len(all_attributes) + 1):
        from itertools import combinations
        for subset in combinations(all_attributes, i):
            X = set(subset)
            for Y in powerset(X):  # all subsets of X
                if Y:
                    F_plus.add(FunctionalDependency(X, set(Y)))
    
    changed = True
    while changed:
        changed = False
        current_fds = list(F_plus)
        
        # Apply augmentation
        for fd in current_fds:
            for attr in all_attributes:
                new_left = fd.left.union({attr})
                new_right = fd.right.union({attr})
                new_fd = FunctionalDependency(new_left, new_right)
                if new_fd not in F_plus:
                    F_plus.add(new_fd)
                    changed = True
        
        # Apply transitivity
        for fd1 in current_fds:
            for fd2 in current_fds:
                if fd1.right == fd2.left:
                    new_fd = FunctionalDependency(fd1.left, fd2.right)
                    if new_fd not in F_plus:
                        F_plus.add(new_fd)
                        changed = True
    
    return F_plus

def powerset(s):
    """Generate all subsets of a set"""
    from itertools import chain, combinations
    s = list(s)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def is_superkey(attributes, all_attrs, fds):
    """Check if a set of attributes is a superkey"""
    closure = attribute_closure(attributes, fds)
    return closure == all_attrs

def find_candidate_keys(relation, fds):
    """Find all candidate keys for a relation"""
    all_attrs = set(relation)
    candidate_keys = []
    
    # Start with single attributes, then combinations
    for length in range(1, len(all_attrs) + 1):
        from itertools import combinations
        for combo in combinations(all_attrs, length):
            attrs = set(combo)
            
            # Check if it's a superkey
            if is_superkey(attrs, all_attrs, fds):
                # Check minimality (no subset is also a superkey)
                is_minimal = True
                for key in candidate_keys:
                    if key.issubset(attrs):
                        is_minimal = False
                        break
                
                # Check if any subset of this combo is already a superkey
                if is_minimal:
                    # Remove non-minimal keys that this new key makes redundant
                    candidate_keys = [k for k in candidate_keys if not attrs.issubset(k)]
                    candidate_keys.append(attrs)
    
    return candidate_keys

def canonical_cover(fds):
    """Compute canonical cover of FDs"""
    # Step 1: Decompose FDs to have single attribute on right side
    G = set()
    for fd in fds:
        for attr in fd.right:
            G.add(FunctionalDependency(fd.left, {attr}))
    
    # Step 2: Remove extraneous attributes from left side
    changed = True
    while changed:
        changed = False
        G_list = list(G)
        
        for fd in G_list:
            if len(fd.left) > 1:
                for attr in list(fd.left):
                    # Check if attr is extraneous
                    remaining = fd.left - {attr}
                    closure_without = attribute_closure(remaining, G)
                    if fd.right.issubset(closure_without):
                        # attr is extraneous
                        new_fd = FunctionalDependency(remaining, fd.right)
                        G.remove(fd)
                        G.add(new_fd)
                        changed = True
                        break
        
        # Step 3: Remove redundant FDs
        G_list = list(G)
        for fd in G_list:
            G_minus = set(G_list)
            G_minus.remove(fd)
            
            closure_without = attribute_closure(fd.left, G_minus)
            if fd.right.issubset(closure_without):
                G.remove(fd)
                changed = True
        merged = {}
        for fd in G:
            key = frozenset(fd.left)
            if key not in merged:
                merged[key] = set()
            merged[key].update(fd.right)

        final_cover = set()
        for left, right in merged.items():
            final_cover.add(FunctionalDependency(set(left), right))

    return final_cover

def print_results(relation, fds):
    """Print all results in a readable format"""
    print("=" * 60)
    print("RELATION:", ''.join(sorted(relation)))
    print("\nORIGINAL FUNCTIONAL DEPENDENCIES:")
    for fd in fds:
        print(f"  {fd}")
    
    print("\n" + "=" * 60)
    
    # Find all attributes
    all_attrs = set(relation)
    
    # Find candidate keys
    cand_keys = find_candidate_keys(relation, fds)
    print("\nCANDIDATE KEYS:")
    for i, key in enumerate(cand_keys, 1):
        print(f"  K{i}: {''.join(sorted(key))}")
    
    # Compute canonical cover
    cover = canonical_cover(fds)
    print("\nCANONICAL COVER:")
    for fd in sorted(cover, key=lambda x: (len(x.left), sorted(x.left)[0])):
        print(f"  {fd}")
    
    # Compute attribute closures for each attribute
    print("\nATTRIBUTE CLOSURES:")
    for attr in sorted(all_attrs):
        closure = attribute_closure({attr}, fds)
        print(f"  {attr}+ = {''.join(sorted(closure))}")
    
    # Check for each candidate key
    print("\n" + "=" * 60)
    print("SUPERKEY CHECKS:")
    for length in range(1, len(all_attrs) + 1):
        from itertools import combinations
        for combo in combinations(sorted(all_attrs), length):
            attrs = set(combo)
            closure = attribute_closure(attrs, fds)
            is_key = closure == all_attrs
            key_type = "Candidate Key" if attrs in cand_keys else "Superkey" if is_key else "Not Key"
            print(f"  {''.join(sorted(attrs))}+ = {''.join(sorted(closure))} ({key_type})")

def decompose_to_3nf(relation, fds):
    cover = canonical_cover(fds)
    relations = []

    for fd in cover:
        schema = fd.left | fd.right
        if not any(schema.issubset(r) for r in relations):
            relations.append(schema)

    candidate_keys = find_candidate_keys(relation, fds)
    has_key = False
    for r in relations:
        for key in candidate_keys:
            if key.issubset(r):
                has_key = True
                break

    if not has_key:
        relations.append(candidate_keys[0])

    final = []
    for r in relations:
        if not any(r < r2 for r2 in relations):
            final.append(r)

    return final

def is_dependency_preserved(alpha, beta, decomposition, fds):
    result = set(alpha)

    changed = True
    while changed:
        changed = False
        for r in decomposition:
            t = attribute_closure(result & r, fds) & r
            new_result = result | t
            if new_result != result:
                result = new_result
                changed = True

    return set(beta).issubset(result)


def test_all_dependencies_preserved(fds, decomposition):
    for fd in fds:
        if not is_dependency_preserved(fd.left, fd.right, decomposition, fds):
            return False
    return True


def project_fds(fds, attrs):
    return [fd for fd in fds if fd.left.issubset(attrs) and fd.right.issubset(attrs)]


def decompose_to_bcnf(relation, fds):
    result = [set(relation)]
    done = False

    while not done:
        done = True
        for i, r in enumerate(result):
            relevant_fds = project_fds(fds, r)
            for fd in relevant_fds:
                closure = attribute_closure(fd.left, relevant_fds)
                if closure != r:
                    X = fd.left
                    Y = fd.right

                    r1 = X | Y
                    r2 = r - (Y - X)

                    result.pop(i)
                    result.append(r1)
                    result.append(r2)

                    done = False
                    break
            if not done:
                break

    return result

def print_decomposition(name, relations):
    print("\n" + name + " DECOMPOSITION:")
    for i, r in enumerate(relations, 1):
        print(f"  R{i}: {''.join(sorted(r))}")


# Example usage and test cases
if __name__ == "__main__":
    print("\n\n" + "=" * 60)
    print("YOUR OWN EXAMPLE:")
    print("Enter relation attributes (e.g., ABCD): ")
    relation = input().strip().upper()
    
    fds = []
    print("Enter functional dependencies (one per line, format: AB-C, empty line to finish):")
    while True:
        line = input().strip()
        if not line:
            break
        if "-" in line:
            left, right = line.split("-")
            fds.append(FunctionalDependency(left.strip(), right.strip()))
    
    if fds:
        print_results(relation, fds)
        
    three_nf = decompose_to_3nf(set(relation), fds)
    print_decomposition("3NF", three_nf)

    bcnf = decompose_to_bcnf(set(relation), fds)
    print_decomposition("BCNF", bcnf)

    print("\nDEPENDENCY PRESERVATION (BCNF):",
        test_all_dependencies_preserved(fds, bcnf))
