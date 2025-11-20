import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Total de processos
c.execute('SELECT COUNT(*) FROM processos')
total = c.fetchone()[0]
print(f'📊 Total de processos: {total}')

# Por regime
c.execute('SELECT regime_tributario, COUNT(*) FROM empresas GROUP BY regime_tributario')
regimes = c.fetchall()

if regimes:
    print(f'\n📋 Por regime:')
    for r in regimes:
        print(f'   {r[0]}: {r[1]} empresas')
else:
    print('\n⚠️  Nenhum regime no banco')

conn.close()
