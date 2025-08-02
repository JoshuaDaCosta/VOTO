import sqlite3
from logs_voto.logging import setup_logger

logger = setup_logger()


class Voto():
    def __init__(self):
        print("*"*80)
        logger.debug("iniciando o sistema!")
        print("*"*80)
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
        while True:
            

            escolha=input(str("Qual vai escolher?")).strip().lower()
            escolha_c=['01','1', 'candidato']
            escolha_e=['02','2', 'eleitor']
            escolha_v=['03','3','votar']
            escolha_p=['fim', 'stop']
                    
            if  escolha in escolha_c:
                print("candidato seja bem vindo!")
                self.candidato()
            elif escolha in escolha_e:
                print("eleitor seja bem vindo!")
                self.eleitor()
            elif escolha in escolha_v:
                self.votar()
            if escolha in escolha_p:
                break

            
        


        

        
<<<<<<< HEAD
    def conexao(self):
        con = sqlite3.connect("voto.db")
        logger.info("criando conexões!")
        return con
=======
#     def conexao(self):
          
#          BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#         db_path = os.path.join(BASE_DIR, "eleicoes.db")
#         con = sqlite3.connect(db_path)
#         logger.info("criando conexões!")
#         return con
>>>>>>> 00bb96f7555771a86106b7134f5c91dfac43800d

    # candidato
    def candidato(self):
        logger.debug("criando as conexões")
        con = self.conexao()
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
        logger.info("# Alistamento de Candidatos")
        self.alistar()
        
        con.close()
        logger.warning("fechando todas as conexões com a base de dados")
    def alistar(self):
        logger.debug("conectando ao base de dados")
        con = self.conexao()
        nome=input("Nome COMPLETO:").capitalize()
        telf=int(input("telf:"))
        partido=input("partido:").upper()
        email=input("email:").lower()

        cursor=con.cursor()
        cursor.execute("select NOME from CANDIDATOS")
        candidatos_nomes=[row[0] for row in cursor.fetchall()]
        if nome not in candidatos_nomes:
            try:
                
                con.execute("INSERT INTO CANDIDATOS (NOME, TELEFONE,PARTIDO,EMAIL) VALUES (?,?,?,?)",(nome, telf, partido, email))
                con.commit()
                logger.info("✅ Candidatos cadastrado com sucesso!")

            except Exception as e:
                logger.error("❌ Erro ao cadastrar:")
                logger.exception(e)
                # print("❌ Erro ao cadastrar:", e)
            finally:
                con.close()
                logger.warning("fechando as conexoes")
        else:
            logger.error("🚫 Não vai ser inserido este nome porque já está na base de dados!")
    def mostrar_candidatos(self):
        logger.debug("conectando ao base de dados")
        con=self.conexao()
        cursor=con.cursor()
        logger.info("pegando todos os usuários de candidatos")
        cursor.execute("Select * from CANDIDATOS")
        candidatos=cursor.fetchall()
        print("Aqui estão todos os candidatos disponíveis 👇:")
        if not candidatos:
            print("🚫 Nenhum candidato ainda cadastrado!")
        else:
            print("\n 📝 lista de candidatos:")
            print("ID| NOME | TELEFONE | PARTIDO | EMAIL")
            for c in candidatos:
                print(f"{c[0]}| {c[1]} |{c[2]}|{c[3]}|{c[4]}")
        logger.warning("fechando a conexão com à base de dados")
        con.close()
    def votar(self):
        logger.debug("criando conexão com a base de dados")
        con = self.conexao()
        logger.warning("criando a tabela votos")
        con.execute("""
            CREATE TABLE IF NOT EXISTS VOTOS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                ELEITOR TEXT,
                ELEITO TEXT);
        """)

        self.mostrar_candidatos()
        cursor = con.cursor()

        logger.info("🔎 Buscando todos os candidatos")
        cursor.execute("SELECT NOME FROM CANDIDATOS")
        candidatos = [row[0] for row in cursor.fetchall()]

        logger.info("🔎 Buscando todos os votos")
        cursor.execute("SELECT ELEITOR FROM VOTOS")
        eleitores_ja_votaram = [row[0] for row in cursor.fetchall()]
        
        logger.info("🔎 Buscando todos os eleitores")
        cursor.execute("SELECT NOME FROM ELEITORES")
        eleitores=[row[0] for row in cursor.fetchall()]

        eleito = input("Para quem vai votar?\n:").capitalize()
        eleitor = input("Quem vai votar?\n:").capitalize()

        if eleito not in candidatos:
            logger.error(f"❌ Candidato '{eleito}' não está na base de dados!")
            print("❌ Candidato não encontrado!")
            con.close()
            return

        if eleitor in eleitores_ja_votaram:
            logger.warning(f"⚠️\n Eleitor '{eleitor}' já votou.")
            print("⚠️\nVocê já votou. Não é possível votar novamente.")
            con.close()
            return
        if eleitor not in eleitores:
            logger.error(f"❌ eleitor '{eleitor}' não está na base de dados!")
            print("Eleitor não encontrado!")
            con.close()
            return


        try:
            cursor.execute("INSERT INTO VOTOS (ELEITOR, ELEITO) VALUES (?, ?)", (eleitor, eleito))
            con.commit()
            logger.info(f"✅ Voto registrado com sucesso: {eleitor} votou em {eleito}.")
            print("✅ Voto registrado com sucesso!")
        except Exception as e:
            logger.error("❌ Erro ao tentar registrar o voto.")
            logger.exception(e)
        finally:
            logger.warning("⚠️ Fechando a conexão com a base de dados.")
            con.close()


    ## eleitor
    def eleitor(self):

        logger.info("Criando conexões")
        con=self.conexao()
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
        self.alistar_e()
        logger.warning("fechar as conexões")     
        con.close()
    def alistar_e(self):
        con=self.conexao()
        nome=input("nome_eleitor:").strip().capitalize()
        telf=input("telf:").strip().capitalize()
        bi=input("BI:").strip().upper()
        cursor=con.cursor()
        cursor.execute("select NOME FROM ELEITORES")
        eleitores=[row[0] for row in cursor.fetchall()]
        if nome not in eleitores: 
            try:
                con.execute("INSERT INTO ELEITORES (NOME, TELEFONE, BI) VALUES(?,?,?)",(nome, telf, bi))
                logger.info("✅ eleitor cadastrado com sucesso!")
                con.commit()
            except Exception as e:
                logger.error("❌ Erro ao cadastrar:")
                logger.exception(e)
            finally:
                logger.warning("fechado as conex")
                con.close()
        else:
            logger.error("🚫 Não vai ser inserido este nome porque já está na base de dados!")




        




j=Voto()

    





        


