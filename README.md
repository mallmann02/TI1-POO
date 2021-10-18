## Atributos da classe Abstrata Conta Bancária
  - Nome Cliente
  - CPF
  - Saldo
  - Numero Conta (ID)

### Outros atributos:
  - Taxa de rendimento
  - Tipo de risco
  - Cheque especial

## Métodos da classe Abstrata Conta Bancária:
  - consultaSaldo(): Retorna o saldo atual da conta
  - saque(): Realiza um saque na conta (decrementa o saldo)
  - deposito(): Realiza um deposito na conta (incrementa o saldo)
  - rendimento(): Contrato implementado nas classes filhas
### Funções Genéricas:
  - saque_verboso: Mostra os atributos de uma conta, realiza um saque e mostra o saldo.
  - status_contas: Mostra quantas contas de cada tipo foram criadas e ao todo também.

# Forma de uso:
  Existe um arquivo app.py que executa as operações dentro das classes com base em instruções que são interpretadas de um arquivo de texto.
  - Para usar, basta executar o comando a seguir na linha de comando: # python3 ./app.py ./Individuos/<nome_do_arquivo>.txt ./Individuos/<nome_do_arquivo2>.txt ...

  Obs: A pasta indivíduos já esta criada, deve-se apenas colocar os arquivos de texto.

  Quando rodar este comando, o programa tentará ler as instruções nos arquivos passados como argumento e gerará dois arquivos para cada um dos arquivos referentes aos indivíduos: <individuo>.log e <individuo>.saida.

  O arquivo .log conterá possíveis erros dentro da execução do programa e o saída conterá as informações de cada conta criada após a execução.