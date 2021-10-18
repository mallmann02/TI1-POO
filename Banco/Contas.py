from abc import ABCMeta, abstractmethod

class Moeda:
  def __init__(self, valor=0):
    self.valor = valor
      
  def __add__(self,outro):
    if isinstance(outro, float):
        novo_valor=self.valor+outro
    else:
        novo_valor=self.valor+outro.valor
    return novo_valor

  def __sub__(self,outro):
    if isinstance(outro, float):
        novo_valor=self.valor-outro
    else:
        novo_valor=self.valor-outro.valor
    return novo_valor

  def __iadd__(self, outro):
    if isinstance(outro, float) or isinstance(outro, int):
      novo_valor=self.valor+outro
    else:
      novo_valor=self.valor+outro.valor
    return novo_valor
  
  def __isub__(self, outro):
    if isinstance(outro, float) or isinstance(outro, int):
      novo_valor=self.valor-outro
    else:
      novo_valor=self.valor-outro.valor
    return novo_valor
  
  def __mul__(self, outro):
    if isinstance(outro, float) or isinstance(outro, int):
      novo_valor=self.valor*outro
    else:
      novo_valor=self.valor*outro.valor
    return novo_valor
  
  def __gt__(self, outro):
    if isinstance(outro, float) or isinstance(outro, int):
      return self.valor > outro
    else:
      return self.valor > outro.valor
  
  def __lt__(self, outro):
    if isinstance(outro, float) or isinstance(outro, int):
      return self.valor < outro
    else:
      return self.valor < outro.valor

  def __str__(self):
    return str(self.valor)

class ErroCredencialInvalida(Exception):
  def __init__(self,valor, credencial):
    self.valor=valor
    self.credencial=credencial
  def __str__(self):
    return "Este valor não é válido: " + str(self.valor) + " para a credencial " + self.credencial

class ErroSaqueInvalido(Exception):
  def __init__(self, valor):
    self.valor = valor

  def __str__(self):
    if self.valor < 0:
      return 'Não é possível sacar um valor negativo'
    return 'O valor de saque é maior que o saldo'

class ErroDepositoInvalido(Exception):
  def __init__(self, valor):
    self.valor = valor

  def __str__(self):
    return 'Não é possível depositar um valor negativo'


def status_conta():
  print('Numero total de contas criadas: ', ContaBancaria.numeroContas);
  print('Numero total de contas poupanca criadas: ', ContaBancaria.numeroContaPoupanca);
  print('Numero total de contas investimento criadas: ', ContaBancaria.numeroContaInvestimento);
  print('Numero total de contas corrente criadas: ', ContaBancaria.numeroContaCorrente);

def saque_verboso(objeto, valor):
  try:
    print(objeto.__dict__)
  except Exception as e:
    pass
  try:
    objeto.saque(valor)
  except Exception as e:
    pass
  try:
    objeto.consultaSaldo()
  except Exception as e:
    pass

class ContaBancaria(metaclass=ABCMeta):
  numeroContas=0
  numeroContaCorrente=0
  numeroContaInvestimento=0
  numeroContaPoupanca=0
  def __init__(self, numeroConta, nomeCliente, cpf, saldo):
    self._nomeCliente = nomeCliente;
    self._numeroConta = numeroConta;
    self._cpf = cpf;
    self._saldo = Moeda(saldo);
    if len(str(cpf)) != 11:
      raise ErroCredencialInvalida(cpf, 'CPF')
    elif len(str(numeroConta)) != 4:
      raise ErroCredencialInvalida(numeroConta, 'Número da conta')
    elif not isinstance(nomeCliente, str) or len(nomeCliente) > 50:
      raise ErroCredencialInvalida(nomeCliente, 'Nome do cliente')
    elif saldo < 0:
      raise ErroCredencialInvalida(saldo, 'Saldo')
    ContaBancaria.numeroContas +=1
    
  @property
  @abstractmethod
  def nomeCliente(self): pass
  @property
  @abstractmethod
  def numeroConta(self): pass
  @property
  @abstractmethod
  def cpf(self): pass
  @property
  @abstractmethod
  def saldo(self): pass

  def __getattr__(self, atributo):
    print("Atributo ou método não existente:", atributo)
    return self.metodo_desconhecido
  
  def metodo_desconhecido(self):
    return -1

  def statusContas(self):
    print(str(self.numeroContas))

  def deposito(self, valorDeposito):
    self._saldo = Moeda(self._saldo)
    if valorDeposito < 0:
      raise ErroDepositoInvalido(valorDeposito);
    self._saldo += valorDeposito;
  
  @abstractmethod
  def rendimento(self, dias): pass
  
  def consultaSaldo(self):
    print('Seu saldo é: R$ %.2f' % self._saldo)
  
  def saque(self, valorSaque):
    if valorSaque > self._saldo or valorSaque < 0:
      raise ErroSaqueInvalido(valorSaque)
    self._saldo -= valorSaque;

  @nomeCliente.setter
  @abstractmethod
  def nomeCliente(self, valor): pass

  @numeroConta.setter
  @abstractmethod
  def numeroConta(self, valor): pass

  @cpf.setter
  @abstractmethod
  def cpf(self, valor): pass

  @saldo.setter
  @abstractmethod
  def saldo(self, valor): pass

  @abstractmethod
  def __str__(self): pass

  def __enter__(self):
    return self
  
  def __exit__(self, type, value, traceback):
    del self._saldo
    del self._nomeCliente
    del self._numeroConta
    del self._cpf
    
class ContaCorrente(ContaBancaria):
  def __init__(self, numeroConta, nomeCliente, cpf, saldo, limite):
    self._rendimento = 0.01;
    self._limite = int(limite)
    super().__init__(numeroConta, nomeCliente, cpf, saldo);
    ContaBancaria.numeroContaCorrente += 1
  
  @property
  def nomeCliente(self):
    return self._nomeCliente

  @property
  def numeroConta(self):
    return self._numeroConta

  @property
  def cpf(self):
    return self._cpf

  @property
  def saldo(self):
    return self._saldo

  @nomeCliente.setter
  def nomeCliente(self, valor):
    self._nomeCliente=valor;
  
  @numeroConta.setter
  def numeroConta(self, valor):
    self._numeroConta=valor;
  
  @cpf.setter
  def cpf(self, valor):
    self._cpf=valor;
  
  @saldo.setter
  def saldo(self, valor):
    self._saldo=valor;

  def saque(self, valor):
    valorPosSaque = self._saldo - valor;
    if valorPosSaque > self._limite:
      self._saldo -= valor;
    else:
      raise ErroSaqueInvalido(valor);

  def rendimento(self, dias):
    rendimentoTrintaDias = (self._saldo * self._rendimento)
    rendimentoEmXDias= (dias*rendimentoTrintaDias)/30;
    print('Rendimento em ',dias, 'dias: R$ %.2f' % rendimentoEmXDias);
  
  def __str__(self):
    return "Seu saldo atual é R$"+ str(self.saldo)

class ContaPoupanca(ContaBancaria):
  def __init__(self, numeroConta, nomeCliente, cpf, saldo, taxaDeRendimento):
    self._rendimento = taxaDeRendimento
    super().__init__(numeroConta, nomeCliente, cpf, saldo);
    ContaBancaria.numeroContaPoupanca +=1
  
  @property
  def nomeCliente(self):
    return self._nomeCliente

  @property
  def numeroConta(self):
    return self._numeroConta

  @property
  def cpf(self):
    return self._cpf

  @property
  def saldo(self):
    return self._saldo

  @nomeCliente.setter
  def nomeCliente(self, valor):
    self._nomeCliente=valor;
  
  @numeroConta.setter
  def numeroConta(self, valor):
    self._numeroConta=valor;
  
  @cpf.setter
  def cpf(self, valor):
    self._cpf=valor;
  
  @saldo.setter
  def saldo(self, valor):
    self._saldo=valor;

  def rendimento(self, dias):
    rendimentoTrintaDias = (self._saldo * self._rendimento)
    rendimentoEmXDias= (dias*rendimentoTrintaDias)/30;
    print('Rendimento em', dias, 'dias: R$ %.2f' % rendimentoEmXDias);
  
  def __str__(self):
    return "Seu saldo atual é R$"+ str(self.saldo)

class ContaInvestimento(ContaBancaria):
  def __init__(self, numeroConta, nomeCliente, cpf, saldo, tipoRisco):
    if tipoRisco == 'Baixo':
      self._rendimento = 0.1
    elif tipoRisco == 'Médio':
      self._rendimento = 0.25;
    else:
      self._rendimento = 0.5
    super().__init__(numeroConta, nomeCliente, cpf, saldo);
    ContaBancaria.numeroContaInvestimento +=1
  
  @property
  def nomeCliente(self):
    return self._nomeCliente

  @property
  def numeroConta(self):
    return self._numeroConta

  @property
  def cpf(self):
    return self._cpf

  @property
  def saldo(self):
    return self._saldo

  @nomeCliente.setter
  def nomeCliente(self, valor):
    self._nomeCliente=valor;
  
  @numeroConta.setter
  def numeroConta(self, valor):
    self._numeroConta=valor;
  
  @cpf.setter
  def cpf(self, valor):
    self._cpf=valor;
  
  @saldo.setter
  def saldo(self, valor):
    self._saldo=valor;
  
  def rendimento(self, dias):
    rendimentoTrintaDias = (self._saldo * self._rendimento)
    rendimentoEmXDias= (dias*rendimentoTrintaDias)/30;
    print('Rendimento em',dias,'dias: R$ %.2f' % rendimentoEmXDias);
  
  def __str__(self):
    return "Seu saldo atual é R$"+ str(self.saldo)