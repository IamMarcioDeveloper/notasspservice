import os as os
import dbDominio as db
import shutil as shutil
from datetime import datetime
from datetime import timedelta
from datetime import date as d

mes_competencia = ('0' + str(d.today().month - 1))[-2:]
ano_competencia = str(d.today().year)
ultimodiames = str(datetime.today() + timedelta(days=-datetime.today().day)).replace('-', '')[0:8]
usuario = os.getlogin()
pastaGeral = fr'\\172.16.7.229\Importar\{ano_competencia}\FISCAL\SERVICOS\Geral\{mes_competencia+ano_competencia}'
pastaDownload = (fr'C:\Users\{usuario}\Downloads')
caminhos = [os.path.join(pastaDownload, nome) for nome in os.listdir(pastaDownload)]
arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
txt = [arq for arq in arquivos if arq.lower().endswith(".txt")]
posicao = 0

for f in os.listdir(pastaGeral):
    os.remove(os.path.join(pastaGeral, f))

for x in txt:
    if txt[posicao].replace(pastaDownload, '')[1:7] == 'NFSe_E':
        ccm = txt[posicao].replace(pastaDownload, '').split('_')[2]
        print(ccm)
        emp = db.consulta(ccm)
        if not emp == 0:
            dest = fr'\\172.16.7.229\Importar\{ano_competencia}\FISCAL\SERVICOS\Prestados\{emp}\{mes_competencia + ano_competencia}'
            if os.path.exists(dest):
                try:
                    os.remove({dest} + txt[posicao].replace(pastaDownload, ''))
                except:
                    pass
                finally:
                    shutil.copy(txt[posicao], dest)
                    shutil.copy(txt[posicao], pastaGeral)
        posicao += 1
    elif txt[posicao].replace(pastaDownload, '').split('_')[0][1:5] == 'NFSe':
        ccm = txt[posicao].replace(pastaDownload, '').split('_')[1]
        print(ccm)
        emp = db.consulta(ccm)
        if not emp == 0:
            dest = fr'\\172.16.7.229\Importar\{ano_competencia}\FISCAL\SERVICOS\Recebidos\{emp}\{mes_competencia + ano_competencia}'
            if os.path.exists(dest):
                try:
                    os.remove({dest}+txt[posicao].replace(pastaDownload,''))
                except:
                    pass
                finally:
                    shutil.copy(txt[posicao], dest)
                    shutil.copy(txt[posicao], pastaGeral)
        posicao += 1
    else:
        if txt[posicao].replace(pastaDownload, '').split('_')[0][1:5] == 'NFTS':
            ccm = txt[posicao].replace(pastaDownload, '').split('_')[1]
            print(ccm)
            emp = db.consulta(ccm)
            if not emp == 0:
                dest = fr'\\172.16.7.229\Importar\{ano_competencia}\FISCAL\SERVICOS\Tomados\{emp}\{mes_competencia + ano_competencia}'
                if os.path.exists(dest):
                    try:
                        os.remove({dest} + txt[posicao].replace(pastaDownload, ''))
                    except:
                        pass
                    finally:
                        shutil.copy(txt[posicao], dest)
                        shutil.copy(txt[posicao], pastaGeral)
            posicao += 1