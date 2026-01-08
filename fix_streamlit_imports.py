#!/usr/bin/env python3
"""
Diagnostic script for Streamlit Cloud import issues
This will help identify why the 'contexts' module isn't being found
"""

import os
import sys

def check_structure(base_path='.'):
    """Check if all necessary __init__.py files exist"""
    
    required_init_files = [
        'contexts/__init__.py',
        'contexts/discovery/__init__.py',
        'contexts/discovery/application/__init__.py',
        'contexts/discovery/application/use_cases/__init__.py',
        'contexts/discovery/domain/__init__.py',
        'contexts/discovery/domain/entities/__init__.py',
        'contexts/discovery/domain/repositories/__init__.py',
        'contexts/discovery/domain/value_objects/__init__.py',
        'contexts/discovery/infrastructure/__init__.py',
        'contexts/discovery/infrastructure/data/__init__.py',
        'contexts/discovery/infrastructure/repositories/__init__.py',
        'contexts/reporting/__init__.py',
        'contexts/reporting/application/__init__.py',
        'contexts/reporting/application/use_cases/__init__.py',
        'contexts/reporting/domain/__init__.py',
        'contexts/reporting/domain/entities/__init__.py',
        'contexts/reporting/domain/services/__init__.py',
        'contexts/reporting/infrastructure/__init__.py',
        'contexts/reporting/infrastructure/repositories/__init__.py',
        'contexts/shared_kernel/__init__.py',
        'contexts/shared_kernel/common/__init__.py',
        'presentation/__init__.py',
    ]
    
    print("=" * 60)
    print("CHECKING PROJECT STRUCTURE")
    print("=" * 60)
    
    missing_files = []
    existing_files = []
    
    for file_path in required_init_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ MISSING: {file_path}")
    
    print("\n" + "=" * 60)
    print(f"Summary: {len(existing_files)} found, {len(missing_files)} missing")
    print("=" * 60)
    
    if missing_files:
        print("\n⚠️  MISSING FILES - CREATE THESE:")
        for f in missing_files:
            print(f"   touch {f}")
    
    # Check if key module files exist
    print("\n" + "=" * 60)
    print("CHECKING KEY MODULE FILES")
    print("=" * 60)
    
    key_files = [
        'contexts/discovery/application/use_cases/search_stations_use_case.py',
        'contexts/discovery/domain/entities/operational_station.py',
        'contexts/discovery/infrastructure/repositories/in_memory_station_repository.py',
        'contexts/shared_kernel/common/station_id.py',
        'presentation/app.py',
    ]
    
    for file_path in key_files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ MISSING: {file_path}")
    
    # Check .gitignore
    print("\n" + "=" * 60)
    print("CHECKING .gitignore")
    print("=" * 60)
    
    gitignore_path = os.path.join(base_path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        problematic_patterns = ['__init__.py', 'contexts/', '*.py', 'application/', 'use_cases/']
        issues = []
        
        for pattern in problematic_patterns:
            if pattern in gitignore_content:
                issues.append(pattern)
        
        if issues:
            print("⚠️  WARNING: .gitignore contains patterns that might exclude needed files:")
            for pattern in issues:
                print(f"   - {pattern}")
        else:
            print("✅ .gitignore looks OK")
    else:
        print("❌ No .gitignore found")
    
    return len(missing_files) == 0


def create_missing_init_files(base_path='.'):
    """Create any missing __init__.py files"""
    
    required_init_files = [
        'contexts/__init__.py',
        'contexts/discovery/__init__.py',
        'contexts/discovery/application/__init__.py',
        'contexts/discovery/application/use_cases/__init__.py',
        'contexts/discovery/domain/__init__.py',
        'contexts/discovery/domain/entities/__init__.py',
        'contexts/discovery/domain/repositories/__init__.py',
        'contexts/discovery/domain/value_objects/__init__.py',
        'contexts/discovery/infrastructure/__init__.py',
        'contexts/discovery/infrastructure/data/__init__.py',
        'contexts/discovery/infrastructure/repositories/__init__.py',
        'contexts/reporting/__init__.py',
        'contexts/reporting/application/__init__.py',
        'contexts/reporting/application/use_cases/__init__.py',
        'contexts/reporting/domain/__init__.py',
        'contexts/reporting/domain/entities/__init__.py',
        'contexts/reporting/domain/services/__init__.py',
        'contexts/reporting/infrastructure/__init__.py',
        'contexts/reporting/infrastructure/repositories/__init__.py',
        'contexts/shared_kernel/__init__.py',
        'contexts/shared_kernel/common/__init__.py',
        'presentation/__init__.py',
    ]
    
    print("\n" + "=" * 60)
    print("CREATING MISSING __init__.py FILES")
    print("=" * 60)
    
    created = []
    for file_path in required_init_files:
        full_path = os.path.join(base_path, file_path)
        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write('# Package marker\n')
            created.append(file_path)
            print(f"✅ Created: {file_path}")
    
    if not created:
        print("✅ All __init__.py files already exist")
    else:
        print(f"\n✅ Created {len(created)} __init__.py files")
    
    return created


if __name__ == '__main__':
    # If run with an argument, use that as the base path
    base_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"\nScanning directory: {os.path.abspath(base_path)}\n")
    
    # First check the structure
    all_exist = check_structure(base_path)
    
    # Ask if user wants to create missing files
    if not all_exist:
        print("\n" + "=" * 60)
        response = input("\nCreate missing __init__.py files? (y/n): ")
        if response.lower() == 'y':
            created = create_missing_init_files(base_path)
            if created:
                print("\n✅ Files created! Now run:")
                print("   git add contexts/ presentation/")
                print("   git add **/__init__.py")
                print('   git commit -m "Add missing __init__.py files"')
                print("   git push")
                print("\nThen reboot your Streamlit app!")
