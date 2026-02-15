from graphviz import Digraph

def analyze_schema(schema):
    entities = {}
    relationships = {}

    for table, info in schema.items():
        pks = set(info.get('PK', []))
        fks = info.get('FK', {})
        attrs = set(info.get('Attributes', []))

        # تشخیص M:N relationship
        if fks and pks == set(fks.keys()):
            relationships[table] = {"PK": pks, "FK": fks, "Attributes": attrs}
        else:
            entities[table] = {"PK": pks, "FK": fks, "Attributes": attrs}

    return entities, relationships

def generate_er(schema):
    entities, relationships = analyze_schema(schema)
    dot = Digraph(comment='ER Diagram', format='png')

    # رسم Entity ها
    for ent, info in entities.items():
        label = f"{ent}\nPK: {','.join(info['PK'])}"
        if info['Attributes']:
            label += "\n" + "\n".join(info['Attributes'])
        dot.node(ent, label=label, shape='box', style='filled', color='lightblue')

    # رسم Relationship ها
    for rel, info in relationships.items():
        label = f"{rel}\nPK: {','.join(info['PK'])}"
        if info['Attributes']:
            label += "\n" + "\n".join(info['Attributes'])
        dot.node(rel, label=label, shape='diamond', style='filled', color='lightpink')

        # اتصال Relationship به Entityها با cardinality
        for fk_attr, ref_entity in info['FK'].items():
            dot.edge(ref_entity, rel, label="1")
            dot.edge(rel, ref_entity, label="N")

    # رسم FK های ساده در Entity ها (1:N)
    for ent, info in entities.items():
        for fk_attr, ref_entity in info['FK'].items():
            dot.edge(ref_entity, ent, label="1")
            dot.edge(ent, ref_entity, label="N")

    return dot

# مثال استفاده
schema = {
    "Student": {"PK": ["ID"], "Attributes": ["Name", "Age"]},
    "Course": {"PK": ["CID"], "Attributes": ["Title"]},
    "Enrollment": {"PK": ["SID", "CID"], "Attributes": ["Grade"], "FK": {"SID": "Student", "CID": "Course"}},
    "Professor": {"PK": ["PID"], "Attributes": ["Name"]},
    "Teaches": {"PK": ["PID","CID"], "Attributes": [], "FK": {"PID": "Professor", "CID": "Course"}}
}

dot = generate_er(schema)
dot.render('er_advanced_diagram', view=True)
