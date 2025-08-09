#!/usr/bin/env python3
import requests

session = requests.Session()
session.post('http://localhost:5000/login', data={'username': 'admin', 'password': 'admin123'})
response = session.get('http://localhost:5000/expenses')
content = response.text

print('PrintExpensesRecord(' in content)
print('function PrintExpensesRecord(' in content)

# البحث عن الوظيفة في المحتوى
import re
matches = re.findall(r'function\s+PrintExpensesRecord\s*\(', content)
print(f"Found {len(matches)} matches for PrintExpensesRecord function")

# البحث عن أي وظيفة تحتوي على PrintExpenses
matches2 = re.findall(r'PrintExpensesRecord', content)
print(f"Found {len(matches2)} total mentions of PrintExpensesRecord")

if matches2:
    print("First few mentions:")
    for i, match in enumerate(matches2[:3]):
        print(f"  {i+1}: {match}")
