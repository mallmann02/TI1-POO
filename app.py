import sys
from Banco import *

argsList = sys.argv[1:]
count = 1
def takeValue(str):
  return str.split(':')[1].strip()

for arg in argsList:
  refArquivo = open(arg, 'r');
  arquivoLogPath='./Individuos/'+ str(count)+'.log'
  logArquivo = open(arquivoLogPath, 'a')
  saidaArquivo=open('./Individuos/'+str(count)+'.saida', 'a')
  for line in refArquivo:
    if ":" not in line:
      name=line
      continue
    if 'criar' not in line and '->' not in line and 'saldo' not in line:
      locals()[line.split(':')[0]] = line.split(':')[1].strip()
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
  saidaArquivo.write('Dados Conta Corrente: '+str(contaCorrenteObj.__dict__)+'\n')
  saidaArquivo.write('Dados Conta Poupanca: '+str(contaPoupancaObj.__dict__)+'\n')
  saidaArquivo.write('Dados Conta Investimento: '+str(contaInvestimentoObj.__dict__)+'\n')
  del contaCorrenteObj
  del contaPoupancaObj
  del contaInvestimentoObj
  refArquivo.close()
  logArquivo.close()
  saidaArquivo.close()
  count += 1