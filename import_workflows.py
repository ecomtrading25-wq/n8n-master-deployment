#!/usr/bin/env python3
"""
N8N Workflow Import Script
Imports all workflows from the package to n8n instance
"""
import os
import json
import requests
import sys
from pathlib import Path
import time

def import_workflows(n8n_url, api_key, workflows_dir):
    """Import all workflows from directory"""
    
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    # Test connection
    try:
        resp = requests.get(f"{n8n_url}/api/v1/workflows", headers=headers, timeout=5)
        if resp.status_code != 200:
            print(f"✗ Connection failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to n8n: {e}")
        return False
    
    print("✓ Connected to n8n\n")
    
    # Find all workflows
    workflow_files = sorted(Path(workflows_dir).glob("**/*.json"))
    print(f"Found {len(workflow_files)} workflows\n")
    
    imported = {}
    failed = []
    
    for idx, wf_file in enumerate(workflow_files, 1):
        category = wf_file.parent.name
        filename = wf_file.name
        
        print(f"[{idx}/{len(workflow_files)}] Importing {filename}...", end=" ", flush=True)
        
        try:
            with open(wf_file) as f:
                workflow_data = json.load(f)
            
            payload = {
                "name": workflow_data.get("name", wf_file.stem),
                "nodes": workflow_data.get("nodes", []),
                "connections": workflow_data.get("connections", {}),
                "active": False,
                "settings": workflow_data.get("settings", {})
            }
            
            resp = requests.post(
                f"{n8n_url}/api/v1/workflows",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if resp.status_code in [200, 201]:
                result = resp.json()
                wf_id = result.get("id")
                print(f"✓ ID: {wf_id}")
                
                if category not in imported:
                    imported[category] = []
                imported[category].append({"file": filename, "id": wf_id})
            else:
                print(f"✗ Failed ({resp.status_code})")
                failed.append(filename)
        except Exception as e:
            print(f"✗ Error: {e}")
            failed.append(filename)
        
        time.sleep(0.5)
    
    # Summary
    print("\n" + "="*60)
    total = sum(len(v) for v in imported.values())
    print(f"✓ Imported: {total} workflows")
    
    for cat in sorted(imported.keys()):
        print(f"\n{cat}:")
        for wf in imported[cat]:
            print(f"  {wf['file']}: {wf['id']}")
    
    if failed:
        print(f"\n✗ Failed: {len(failed)}")
        for f in failed:
            print(f"  {f}")
    
    # Save mapping
    mapping = {"imported": imported, "failed": failed, "total": total}
    with open("workflow_ids.json", "w") as f:
        json.dump(mapping, f, indent=2)
    
    print(f"\n✓ Saved to: workflow_ids.json")
    return True

if __name__ == "__main__":
    n8n_url = os.getenv("N8N_URL", "http://localhost:5678")
    api_key = os.getenv("N8N_API_KEY", "")
    
    if not api_key:
        print("✗ N8N_API_KEY not set")
        sys.exit(1)
    
    workflows_dir = Path(__file__).parent / "03_WORKFLOWS"
    import_workflows(n8n_url, api_key, workflows_dir)
