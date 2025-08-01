# import sqlite3
# from logs_voto.logging import setup_logger

# logger = setup_logger()


# class Voto():
#     def __init__(self):
#         print("*"*30)
#         logger.debug("iniciando o sistema!")
#         print("*"*30)
#         print("""
#                 Seja bem vindo ao sistema de voto!
#               temos as seguintes opções:
#               -Ser um candidato escreva ['01','1', 'candidato']
#               -Ser um Eleitor escreva ['02','2', 'eleitor']
#               obs:
#                 lembrando também que um candidato ou eleitor têm o direito de votar para cada candidato
#                 cada candidato pode votar para si ou para um outro!
              
              

#         """)
#         self.eleitor()
#         # escolha=input(str("Qual vai escolher? testando apenas o eleitor:")).strip().lower()
#         # escolha_c=['01','1', 'candidato']
#         # escolha_e=['02','2', 'eleitor']
#         # if  escolha in escolha_c:
#         #     print("candidato seja bem vindo!")
#         #     #self.candidato
#         # elif escolha in escolha_e:
#         #     print("eleitor seja bem vindo!")
#         #     self.eleitor()
        


        

        
#     def conexao(self):
#         con = sqlite3.connect("eleicoes.db")
#         logger.info("criando conexões!")
#         return con

#     # candidato
#     def candidato(self):
#         logger.debug("criando as conexões")
#         con = self.conexao()
#         logger.warning("criando ou editando a tabela candidatos")
#         con.execute("""
#             CREATE TABLE IF NOT EXISTS CANDIDATOS (
#                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                 NOME TEXT NOT NULL,
#                 TELEFONE INTEGER,
#                 PARTIDO TEXT,
#                 EMAIL TEXT
#             );
#         """)
#         logger.info("salvar a sessão")
#         con.commit()
#         logger.info("# Alistamento de Candidatos")
#         logger.info("alistamentos de votos") 
#         con.close()
#         logger.warning("fechando todas as conexões com a base de dados")
#     def alistar(self):
#         logger.debug("conectando ao base de dados")
#         con = self.conexao()
#         nome=input("Nome:").capitalize()
#         telf=int(input("telf:"))
#         partido=input("partido:").upper()
#         email=input("email:").lower()

#         try:
#             con.execute("INSERT INTO CANDIDATOS (NOME, TELEFONE,PARTIDO,EMAIL) VALUES (?,?,?,?)",(nome, telf, partido, email))
#             con.commit()
#             logger.info("✅ Candidatos cadastrado com sucesso!")

#         except Exception as e:
#             logger.error("❌ Erro ao cadastrar:")
#             logger.exception(e)
#             # print("❌ Erro ao cadastrar:", e)
#         finally:
#             con.close()
#             logger.warning("fechando as conexoes")
#     def mostrar_candidatos(self):
#         logger.debug("conectando ao base de dados")
#         con=self.conexao()
#         cursor=con.cursor()
#         logger.info("pegando todos os usuários de candidatos")
#         cursor.execute("Select * from CANDIDATOS")
#         candidatos=cursor.fetchall()
#         print("Aqui estão todos os candidatos disponíveis 👇:")
#         if not candidatos:
#             print("🚫 Nenhum candidato ainda cadastrado!")
#         else:
#             print("\n 📝 lista de candidatos:")
#             print("ID| NOME | TELEFONE | PARTIDO | EMAIL")
#             for c in candidatos:
#                 print(f"{c[0]}| {c[1]} |{c[2]}|{c[3]}|{c[4]}")
#         logger.warning("fechando a conexão com à base de dados")
#         con.close()
#     def votar(self):
#         logger.debug("criando conexão com a base de dados")
#         con = self.conexao()
#         logger.warning("criando a tabela votos")
#         con.execute("""
#             CREATE TABLE IF NOT EXISTS VOTOS(
#                 ID INTEGER PRIMARY KEY AUTOINCREMENT, 
#                 ELEITOR TEXT,
#                 ELEITO TEXT);
#         """)

#         self.mostrar_candidatos()
#         cursor = con.cursor()

#         logger.info("🔎 Buscando todos os candidatos")
#         cursor.execute("SELECT NOME FROM CANDIDATOS")
#         candidatos = [row[0] for row in cursor.fetchall()]

#         logger.info("🔎 Buscando todos os votos")
#         cursor.execute("SELECT ELEITOR FROM VOTOS")
#         eleitores_ja_votaram = [row[0] for row in cursor.fetchall()]
        
#         logger.info("🔎 Buscando todos os eleitores")
#         cursor.execute("SELECT NOME FROM ELEITORES")
#         eleitores=[row[0] for row in cursor.fetchall()]

#         eleito = input("Para quem vai votar?\n:").capitalize()
#         eleitor = input("Quem vai votar?\n:").capitalize()

#         if eleito not in candidatos:
#             logger.error(f"❌ Candidato '{eleito}' não está na base de dados!")
#             print("❌ Candidato não encontrado!")
#             con.close()
#             return

#         if eleitor in eleitores_ja_votaram:
#             logger.warning(f"⚠️\n Eleitor '{eleitor}' já votou.")
#             print("⚠️\nVocê já votou. Não é possível votar novamente.")
#             con.close()
#             return
#         if eleitor not in eleitores:
#             logger.error(f"❌ eleitor '{eleitor}' não está na base de dados!")
#             print("Eleitor não encontrado!")
#             con.close()
#             return


#         try:
#             cursor.execute("INSERT INTO VOTOS (ELEITOR, ELEITO) VALUES (?, ?)", (eleitor, eleito))
#             con.commit()
#             logger.info(f"✅ Voto registrado com sucesso: {eleitor} votou em {eleito}.")
#             print("✅ Voto registrado com sucesso!")
#         except Exception as e:
#             logger.error("❌ Erro ao tentar registrar o voto.")
#             logger.exception(e)
#         finally:
#             logger.warning("⚠️ Fechando a conexão com a base de dados.")
#             con.close()

     
        

        
#     ## eleitor
#     def eleitor(self):

#         logger.info("Criando conexões")
#         con=self.conexao()
#         con.execute("""
#             CREATE TABLE IF NOT EXISTS ELEITORES (
#                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                 NOME TEXT NOT NULL,
#                 TELEFONE INTEGER,
#                 BI TEXT
#             );
#         """)
#         logger.info("salvar as sessões")
#         con.commit()
#         self.alistar_e()
#         self.votar()
#         logger.warning("fechar as conexões")     
#         con.close()
#     def alistar_e(self):
#         con=self.conexao()
#         nome=input("nome_eleitor:").strip().capitalize()
#         telf=input("telf:").strip().capitalize()
#         bi=input("BI:").strip().upper()
#         try:
#             con.execute("INSERT INTO ELEITORES (NOME, TELEFONE, BI) VALUES(?,?,?)",(nome, telf, bi))
#             logger.info("✅ eleitor cadastrado com sucesso!")
#             con.commit()
#         except Exception as e:
#             logger.error("❌ Erro ao cadastrar:")
#             logger.exception(e)
#         finally:
#             logger.warning("fechado as conex")
#             con.close()
    




        




# j=Voto()

    





        


