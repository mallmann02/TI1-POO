import sys
from Banco import *

argsList = sys.argv[1:]
count = 1
def takeValue(str):
  return str.split(':')[1].strip()

for arg in argsList:
  readFileName=str(arg).split('/')[2].split('.')[0]
  refArquivo = open(arg, 'r');
  arquivoLogPath='./Individuos/'+str(readFileName)+'.log'
  logArquivo = open(arquivoLogPath, 'a')
  saidaArquivo=open('./Individuos/'+str(readFileName)+'.saida', 'a')
  code_error=0
  contaCorrenteObj=None
  contaInvestimentoObj=None
  contaPoupancaObj=None
  for line in refArquivo:
    if ":" not in line:
      name=line
      if len(name) > 50:
        logArquivo.write('Não será possível criar nenhuma conta para este indivíduo, pois o mesmo possui um nome inválido');
        code_error=1
        break
      continue
    if 'criar' not in line and '->' not in line and 'saldo' not in line:
      locals()[line.split(':')[0]] = line.split(':')[1].strip()
      if len(CPF) != 11:
        logArquivo.write('Não será possível criar nenhuma conta para este indivíduo, pois o mesmo possui um CPF inválido');
        code_error=1
        break
    if 'criar' in line:
      if 'contaCorrente' in line:
        saldoInicial=takeValue(refArquivo.readline())
        id = takeValue(refArquivo.readline())
        limite=takeValue(refArquivo.readline())
        try:
          contaCorrenteObj = ContaCorrente(id, name, CPF, int(saldoInicial), int(limite))
        except Exception as e:
          logArquivo.write(e.__str__()+'\n'+'\n')
      if 'contaPoupanca' in line:
        saldoInicial=takeValue(refArquivo.readline())
        id = takeValue(refArquivo.readline())
        taxaDeRendimento=takeValue(refArquivo.readline())
        try:
          contaPoupancaObj = ContaPoupanca(id, name, CPF, int(saldoInicial), float(taxaDeRendimento))
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
      if 'contaInvestimento' in line:
        saldoInicial=takeValue(refArquivo.readline())
        id = takeValue(refArquivo.readline())
        tipoRisco=takeValue(refArquivo.readline())
        try:
          contaInvestimentoObj = ContaInvestimento(id, name, CPF, int(saldoInicial), tipoRisco)
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
    if 'sacar' in line:
      numero = [int(s) for s in line.split() if s.isdigit()] #extrair o numero
      if 'contaInvestimento' in line:
        try:
          contaInvestimentoObj.saque(Moeda(numero[0]))
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
      if 'contaPoupanca' in line:
        try:
          contaPoupancaObj.saque(Moeda(numero[0]))
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
      if 'contaCorrente' in line:
        saque_verboso(contaCorrenteObj, Moeda(numero[0]))
    if 'depositar' in line:
      numero = [int(s) for s in line.split() if s.isdigit()] #extrair o numero
      if 'contaInvestimento' in line:
        try:
          contaInvestimentoObj.deposito(Moeda(numero[0]))
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
      if 'contaPoupanca' in line:
        try:
          contaPoupancaObj.deposito(Moeda(numero[0]))
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
      if 'contaCorrente' in line:
        try:
          contaCorrenteObj.deposito(Moeda(numero[0]))
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
    if 'saldo' in line:
      if 'contaInvestimento' in line:
        try:
          contaInvestimentoObj.consultaSaldo()
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
      if 'contaPoupanca' in line:
        try:
          contaPoupancaObj.consultaSaldo()
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
      if 'contaCorrente' in line:
        try:
          contaCorrenteObj.consultaSaldo()
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
    if 'rendimento' in line:
      dias = [int(s) for s in line.split() if s.isdigit()]
      if 'contaInvestimento' in line:
        try:
          contaInvestimentoObj.rendimento(dias[0])
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
      if 'contaPoupanca' in line:
        try:
          contaPoupancaObj.rendimento(dias[0])
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
      if 'contaCorrente' in line:
        try:
          contaCorrenteObj.rendimento(dias[0])
        except Exception as e:
          logArquivo.write(e.__str__()+'\n')
  if code_error != 1:
    try:
      saidaArquivo.write('Dados Conta Corrente: '+str(contaCorrenteObj.__dict__)+'\n')
      saidaArquivo.write('Balanço final: R$ %.2f'%int(contaCorrenteObj._saldo.valor)+'\n\n')
    except Exception as e:
      logArquivo.write(str(e)+'\n');
    try:
      saidaArquivo.write('Dados Conta Poupanca: '+str(contaPoupancaObj.__dict__)+'\n')
      saidaArquivo.write('Balanço final: R$ %.2f'%int(contaPoupancaObj._saldo.valor)+'\n\n')
    except Exception as e:
      logArquivo.write(str(e)+'\n');
    try:
      saidaArquivo.write('Dados Conta Investimento: '+str(contaInvestimentoObj.__dict__)+'\n')
      saidaArquivo.write('Balanço final: R$ %.2f'%int(contaInvestimentoObj._saldo.valor)+'\n\n')
    except Exception as e:
      logArquivo.write(str(e)+'\n');
    del contaCorrenteObj
    del contaPoupancaObj
    del contaInvestimentoObj
  refArquivo.close()
  logArquivo.close()
  saidaArquivo.close()
  count += 1