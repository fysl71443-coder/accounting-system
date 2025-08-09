#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

session = requests.Session()
login_data = {'username': 'admin', 'password': 'admin123'}
session.post('http://localhost:5000/login', data=login_data)

response = session.get('http://localhost:5000/expenses')
content = response.text

functions = [
    'PrintExpensesRecord',
    'PreviewExpensesRecord', 
    'RegisterExpensesPayment',
    'EditExpensesRecord',
    'DeleteExpensesRecord'
]

print('🔍 فحص وظائف المصروفات:')
for func in functions:
    if f'function {func}(' in content:
        print(f'✅ {func} - موجودة')
    else:
        print(f'❌ {func} - غير موجودة')

buttons = [
    'btnExpensesPrint',
    'btnExpensesPreview',
    'btnExpensesPayment', 
    'btnExpensesEdit',
    'btnExpensesDelete'
]

print('\n🔍 فحص أزرار المصروفات:')
for btn in buttons:
    if f'id="{btn}"' in content:
        print(f'✅ {btn} - موجود')
    else:
        print(f'❌ {btn} - غير موجود')

print('\n🔍 فحص onclick handlers:')
onclick_handlers = [
    'PrintExpensesRecord()',
    'PreviewExpensesRecord()',
    'RegisterExpensesPayment()',
    'EditExpensesRecord()',
    'DeleteExpensesRecord()'
]

for handler in onclick_handlers:
    if handler in content:
        print(f'✅ {handler} - موجود')
    else:
        print(f'❌ {handler} - غير موجود')
