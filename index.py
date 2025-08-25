import sqlite3
from logs_voto.logging import setup_logger
from time import sleep

logger = setup_logger()


class Voto():
    def __init__(self):
        print("*"*80)
        logger.debug("iniciando o sistema!")
        print("*"*80)
        sleep(2)
        
        while True:
            print("""
                Seja bem vindo ao sistema de voto!
              temos as seguintes opções:
              -Ser um candidato escreva ['01','1', 'candidato']
              -Ser um Eleitor escreva ['02','2', 'eleitor']
              -Votar escreva ['03,'3','votar']
              -para parar 🚫 digite ["stop"] ou ["fim"]
              obs:
                lembrando também que um candidato ou eleitor têm o direito de votar para cada candidato
                cada candidato pode votar para si ou para um outro!
              
              

            """)
            print("\n")
            escolha=input(str("Qual vai escolher?")).strip().lower()
            print("*"*30)
            escolha_c=['01','1', 'candidato']
            escolha_e=['02','2', 'eleitor']
            escolha_v=['03','3','votar']
            escolha_p=['fim', 'stop']
                    
            if  escolha in escolha_c:
                sleep(2)
                print("candidato seja bem vindo!")
                self.candidato()
            elif escolha in escolha_e:
                sleep(2)
                print("eleitor seja bem vindo!")
                self.eleitor()
            elif escolha in escolha_v:
                sleep(2)                
                self.votar()
                sleep(10)
            if escolha in escolha_p:
                sleep(3)
                logger.info("🖐🏿✨ obrigado por participar. Vá com Deus !")
                break
          
    def conexao(self):
        sleep(2)
        con = sqlite3.connect("voto.db")
        logger.info("criando conexões!")
        sleep(2)
        return con

    # candidato
    def candidato(self):
        logger.debug("criando as conexões")
        con = self.conexao()
        sleep(1)
        logger.warning("criando ou editando a tabela candidatos")
        con.execute("""
            CREATE TABLE IF NOT EXISTS CANDIDATOS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT NOT NULL,
                TELEFONE INTEGER,
                PARTIDO TEXT,
                EMAIL TEXT
            );
        """)
        logger.info("salvar a sessão")
        con.commit()
        sleep(1)
        logger.info("# Alistamento de Candidatos")
        self.alistar()
        sleep(1)
        
        con.close()
        logger.warning("fechando todas as conexões com a base de dados")
        sleep(1)

    def alistar(self):
        sleep(1)
        logger.debug("conectando ao base de dados")
        con = self.conexao()
        sleep(1)
        nome=input("Nome COMPLETO:").strip().upper()
        telf=int(input("telf:"))
        partido=input("partido:").upper()
        email=input("email:").lower()
        sleep(1)
        logger.info("Buscando nomes de candidatos")
        cursor=con.cursor()
        cursor.execute("select NOME from CANDIDATOS")
        candidatos_nomes=[row[0] for row in cursor.fetchall()]

        if nome not in candidatos_nomes:
            try:
                
                con.execute("INSERT INTO CANDIDATOS (NOME, TELEFONE,PARTIDO,EMAIL) VALUES (?,?,?,?)",(nome, telf, partido, email))
                con.commit()
                sleep(1)
                logger.info("✅ Candidatos cadastrado com sucesso!")

            except Exception as e:
                sleep(1)
                logger.error("❌ Erro ao cadastrar:")
                logger.exception(e)
                # print("❌ Erro ao cadastrar:", e)
            finally:
                sleep(1)
                con.close()
                logger.warning("fechando as conexoes")
        else:
            sleep(1)
            logger.error("🚫 Não vai ser inserido este nome porque já está na base de dados!")
    def mostrar_candidatos(self):
        sleep(1)
        logger.debug("conectando ao base de dados")
        con=self.conexao()
        cursor=con.cursor()
        sleep(1)
        logger.info("pegando todos os usuários de candidatos")
        cursor.execute("Select * from CANDIDATOS")
        candidatos=cursor.fetchall()
        sleep(1)
        print("\n")
        print("*"*30)
        print("Aqui estão todos os candidatos disponíveis 👇:")
        if not candidatos:
            print("🚫 Nenhum candidato ainda cadastrado!")
        else:
            sleep(1)
            print("\n")
            print("\n 📝 lista de candidatos:")
            print("ID| NOME | TELEFONE | PARTIDO | EMAIL")
            for c in candidatos:
                sleep(3)
                print(f"{c[0]}| {c[1]} |{c[2]}|{c[3]}|{c[4]}")
        sleep(1)
        print("\n"*2)
        print("*"*30)
        logger.warning("fechando a conexão com à base de dados")
        con.close()
    def votar(self):
        sleep(1)
        logger.debug("criando conexão com a base de dados")
        con = self.conexao()
        sleep(1)
        logger.warning("criando a tabela votos")
        con.execute("""
            CREATE TABLE IF NOT EXISTS VOTOS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                ELEITOR TEXT,
                ELEITO TEXT);
        """)
        sleep(1)
        print("*"*30)
        print("\n")
        self.mostrar_candidatos()
        sleep(1)
        print("\n")
        cursor = con.cursor()
       
        logger.info("🔎 Buscando todos os candidatos")
        cursor.execute("SELECT NOME FROM CANDIDATOS")
        candidatos = [row[0] for row in cursor.fetchall()]
        sleep(1) 
        logger.info("🔎 Buscando todos os votos")
        cursor.execute("SELECT ELEITOR FROM VOTOS")
        eleitores_ja_votaram = [row[0] for row in cursor.fetchall()]
        sleep(1)
        logger.info("🔎 Buscando todos os eleitores")
        cursor.execute("SELECT NOME FROM ELEITORES")
        eleitores=[row[0] for row in cursor.fetchall()]
        sleep(1)
        eleito = input("Para quem vai votar?\n:").upper().strip()
        eleitor = input("Quem vai votar?\n:").upper().strip()
        sleep(1)
        if eleito not in candidatos:
            sleep(1)
            logger.error(f"❌ Candidato '{eleito}' não está na base de dados!")
            con.close()
            return

        if eleitor in eleitores_ja_votaram:
            sleep(1)
            logger.warning(f"⚠️\n Eleitor '{eleitor}' já votou.")
            con.close()
            return
        if eleitor not in eleitores:
            sleep(1)
            logger.error(f"❌ eleitor '{eleitor}' não está na base de dados!")
            con.close()
            return


        try:
            cursor.execute("INSERT INTO VOTOS (ELEITOR, ELEITO) VALUES (?, ?)", (eleitor, eleito))
            con.commit()
            sleep(1)
            logger.info(f"✅ Voto registrado com sucesso: {eleitor} votou em {eleito}.")
            print("✅ Voto registrado com sucesso!")
        except Exception as e:
            sleep(1)
            logger.error("❌ Erro ao tentar registrar o voto.")
            logger.exception(e)
        finally:
            sleep(1)
            logger.warning("⚠️ Fechando a conexão com a base de dados.")
            con.close()

    ## eleitor
    def eleitor(self):
        sleep(1)
        logger.info("Criando conexões")
        con=self.conexao()
        sleep(1)
        con.execute("""
            CREATE TABLE IF NOT EXISTS ELEITORES (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT NOT NULL,
                TELEFONE INTEGER,
                BI TEXT
            );
        """)
        logger.info("salvar as sessões")
        con.commit()
        sleep(1)
        self.alistar_e()
        sleep(1)
        logger.warning("fechar as conexões")     
        con.close()
        sleep(1)
    def alistar_e(self):
        sleep(1)
        con=self.conexao()
        sleep(2)
        nome=input("nome_eleitor:").upper().strip()
        telf=input("telf:").strip()
        bi=input("BI:").strip().upper()
        sleep(1)
        cursor=con.cursor()
        cursor.execute("select NOME FROM ELEITORES")
        eleitores=[row[0] for row in cursor.fetchall()]
        sleep(1)
        if nome not in eleitores: 
            try:
                con.execute("INSERT INTO ELEITORES (NOME, TELEFONE, BI) VALUES(?,?,?)",(nome, telf, bi))
                sleep(1)
                logger.info("✅ eleitor cadastrado com sucesso!")
                con.commit()
            except Exception as e:
                sleep(1)
                logger.error("❌ Erro ao cadastrar:")
                logger.exception(e)
            finally:
                sleep(1)
                logger.warning("fechado as conex")
                con.close()
        else:
            sleep(1)
            logger.error("🚫 Não vai ser inserido este nome porque já está na base de dados!")




        




j=Voto()

    





        


