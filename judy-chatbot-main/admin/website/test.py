from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from config.connection import open_connection


con = open_connection()
cur = con.cursor()

requette = '''
    INSERT INTO admin (id, nom, prenom, email, mot_de_passe)
    VALUES (%s, %s, %s, %s, %s)
'''

cur.execute(requette, [1, 'admin', 'admin', 'admin@gmail.com', generate_password_hash('adminadmin')])
con.commit()

#print(generate_password_hash('adminadmin'))

#print(check_password_hash('pbkdf2:sha256:150000$eLKMtfMu$9e1d4f4af05977dce52ecf5f36996dfbd13e7c5d083a9e5a32bd8b7d0244c8d1', 'adminadmin'))

# pbkdf2:sha256:150000$qsv7kqpz$eabe64102684dc1d7c6e52023c289998f00df87011bfc7c623dbdd695b46d412
# pbkdf2:sha256:150000$eLKMtfMu$9e1d4f4af05977dce52ecf5f36996dfbd13e7c5d083a9e5a32bd8b7d0244c8d1