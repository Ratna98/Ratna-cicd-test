#!/usr/bin/env python3
"""
Simple generator: read input JSON and create .tf per node into output/
Usage:
  python generator/generator.py examples/example2_multiple_targets.json
"""
import json
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE = Path(__file__).resolve().parents[1]
MAP_FILE = BASE / "generator_map" / "service_map.json"
TEMPLATES_DIR = BASE / "templates"
OUT_DIR = BASE / "output"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=select_autoescape([]))

def load_map():
    with open(MAP_FILE, 'r') as f:
        return json.load(f)

def find_node(nodes, node_id):
    for n in nodes:
        if n.get('id') == node_id:
            return n
    return None

def build_bucket_arn(bucket, objects=False):
    return f"arn:aws:s3:::{bucket}{'/*' if objects else ''}"

def gather_permissions(nodes, edges, mapping):
    perms = {}
    wires = []
    for e in edges:
        ops = e.get('operation', [])
        src = e.get('sourceId'); tgt = e.get('targetId')
        src_node = find_node(nodes, src); tgt_node = find_node(nodes, tgt)
        if not src_node or not tgt_node: continue
        src_type = src_node['service']['serviceshortname']; tgt_type = tgt_node['service']['serviceshortname']
        for op in ops:
            if op == 'events' and src_type == 'awss3' and tgt_type == 'awslambda':
                wires.append({'type':'s3_to_lambda','source':src,'target':tgt,'bucket': src_node['service'].get('bucket','my-bucket')})
                continue
            tgt_map = mapping.get(tgt_type, {})
            actions = tgt_map.get('permission_templates', {}).get(op, [])
            if not actions:
                src_map = mapping.get(src_type, {})
                actions = src_map.get('permission_templates', {}).get(op, [])
            if not actions: continue
            resource = '*'
            if tgt_type == 'awss3':
                resource = build_bucket_arn(tgt_node['service'].get('bucket','my-bucket'), objects=(op in ('read','write')))
            elif tgt_type == 'awslambda':
                fn = tgt_node['service'].get('function_name', tgt_node['id'])
                resource = f"arn:aws:lambda:*:*:function:{fn}"
            principal = src
            lst = perms.setdefault(principal, [])
            for a in actions:
                lst.append({'action': a, 'resource': resource, 'edge': e})
    return perms, wires

def render(node, map_entry, perms_for_node, wires):
    tpl = env.get_template('resource.tf.j2')
    return tpl.render(node=node, map_entry=map_entry, perms=perms_for_node, wires=wires)

def main():
    if len(sys.argv) < 2:
        print('Usage: python generator/generator.py <input_json>')
        sys.exit(1)
    data = json.load(open(sys.argv[1]))
    nodes = data.get('nodes', []); edges = data.get('edges', [])
    mapping = load_map()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    perms, wires = gather_permissions(nodes, edges, mapping)
    for n in nodes:
        node_id = n['id']
        map_entry = mapping.get(n['service']['serviceshortname'], {})
        perms_for_node = perms.get(node_id, [])
        content = render(n, map_entry, perms_for_node, wires)
        fname = f"{n['service'].get('serviceid',0)}_{node_id}.tf"
        (OUT_DIR / fname).write_text(content)
        print('Generated', OUT_DIR / fname)
    (OUT_DIR / 'generation_summary.json').write_text(json.dumps({'perms': perms, 'wires': wires}, indent=2))
    print('Done.')

if __name__ == '__main__':
    main()
