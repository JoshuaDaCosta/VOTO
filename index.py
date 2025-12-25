import sqlite3
from logs_voto.logging import setup_logger
from time import sleep
from crypto import encrypt_user, decrypt_user, hash_user
from collections import Counter

logger = setup_logger()


class Voto():

    def conexao(self):
        con = sqlite3.connect("voto.db")
        return con

    # ---------------- CANDIDATO ----------------
    def candidato(self):
        con = self.conexao()
        con.execute("""
            CREATE TABLE IF NOT EXISTS CANDIDATOS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT,
                TELEFONE TEXT,
                PARTIDO TEXT,
                EMAIL TEXT
            );
        """)
        con.commit()
        con.close()

    def alistar(self, nome, telf, email, partido):
        con = self.conexao()
        cursor = con.cursor()

        nome_e = encrypt_user(nome)
        telf_e = encrypt_user(str(telf))
        email_e = encrypt_user(email)
        partido_e = encrypt_user(partido)

        cursor.execute("SELECT NOME FROM CANDIDATOS")
        existentes = [row[0] for row in cursor.fetchall()]

        if nome_e not in existentes:
            cursor.execute("""
                INSERT INTO CANDIDATOS (NOME, TELEFONE, PARTIDO, EMAIL)
                VALUES (?, ?, ?, ?)
            """, (nome_e, telf_e, partido_e, email_e))
            con.commit()

        con.close()

    def mostrar_candidatos(self):
        con = self.conexao()
        cursor = con.cursor()
        cursor.execute("SELECT ID, NOME FROM CANDIDATOS")
        dados = cursor.fetchall()
        con.close()

        candidatos = []
        for i, nome in dados:
            candidatos.append((i, decrypt_user(nome)))
        return candidatos

    # ---------------- ELEITOR ----------------
    def eleitor(self):
        con = self.conexao()
        con.execute("""
            CREATE TABLE IF NOT EXISTS ELEITORES (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT,
                TELEFONE TEXT,
                BI TEXT,
                LOCALIDADE TEXT
            );
        """)
        con.commit()
        con.close()
    def listar_hash_eleitores(self):
        """
        Retorna uma lista de todos os eleitores já votaram, 
        em formato encryptado (hash), para mostrar no dashboard.
        """
        
        con = self.conexao()
        cursor = con.cursor()
        cursor.execute("SELECT ELEITOR FROM VOTOS")
        eleitores = [row[0] for row in cursor.fetchall()]
        con.close()
        return eleitores

    def alistar_e(self, nome, telf, bi, gps):
        con = self.conexao()
        cursor = con.cursor()

        nome_h = hash_user(nome)
        telf_e = encrypt_user(str(telf))
        bi_h = hash_user(bi)
        gps_e = encrypt_user(gps)

        cursor.execute("SELECT NOME FROM ELEITORES")
        existentes = [row[0] for row in cursor.fetchall()]

        if nome_h not in existentes:
            cursor.execute("""
                INSERT INTO ELEITORES (NOME, TELEFONE, BI, LOCALIDADE)
                VALUES (?, ?, ?, ?)
            """, (nome_h, telf_e, bi_h, gps_e))
            con.commit()

        con.close()
    # 
    def criar_tabela_votos(self):
        con = self.conexao()
        con.execute("""
            CREATE TABLE IF NOT EXISTS VOTOS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ELEITOR TEXT,
                ELEITO TEXT
            );
        """)
        con.commit()
        con.close()

    # ---------------- VOTO ----------------
    def votar(self, eleitor_c, candidato):
        con = self.conexao()
        cursor = con.cursor()

        self.criar_tabela_votos()

        eleitor_h = hash_user(eleitor_c)
        candidato_e = encrypt_user(candidato)

        cursor.execute("SELECT ELEITOR FROM VOTOS")
        ja_votaram = [row[0] for row in cursor.fetchall()]

        if eleitor_h in ja_votaram:
            con.close()
            return

        cursor.execute("""
            INSERT INTO VOTOS (ELEITOR, ELEITO)
            VALUES (?, ?)
        """, (eleitor_h, candidato_e))

        con.commit()
        con.close()

    # ---------------- APURAÇÃO ----------------

    def apurar_votos(self):
        # conecta ao banco
        con = sqlite3.connect("voto.db")
        cursor = con.cursor()

        # pega todos os votos (criptografados)
        cursor.execute("SELECT ELEITO FROM VOTOS")
        votos_encrypted = cursor.fetchall()
        
        # decrypta os votos
        votos_decrypt = []
        for v in votos_encrypted:
            try:
                votos_decrypt.append(decrypt_user(v[0]))
            except Exception as e:
                print(f"Erro ao decryptar voto: {v[0]} - {e}")

        # conta os votos por candidato
        resultado = Counter(votos_decrypt)

        # ordena do maior para o menor
        resultados = dict(sorted(resultado.items(), key=lambda item: item[1], reverse=True))

        con.close()
        return resultados

    