# Pacote Serviço

Principais dependências:

![pyver](https://img.shields.io/badge/python-3.5%2B-blue)

Pacote para criar serviço baseado em thread, executa um micro serviço por meio de threads.

## Projetos relacionados

- Sem dependência de outro projeto.

## Variáveis de Ambiente Necessárias

- Não se aplica.

## Como configurar o Pacote em Serviço

### Instalação

Comando:

```sh
pip install lins_servico
```

### Importação

- **Thread**: Classe que será usada para executar uma função em loop por um determinado tempo.
- **thread_loop**: Decorator responsável por encapsular a thread e executa-la em um contexto.

Código:

```python
from lins_servico.thread import Thread
from lins_servico.decorators import thread_loop
```

## Utilização

### 1) Criação da thread

#### Exemplo:

Código:

```python
stop_time_interval_thread01 = {
    'thread_name': 'thread01', # Nome significativo para identificar a thread.
    'inicio': '10:25', # Inicio da pausa da thread.
    'fim': '10:48' # Fim da pausa da thread.
}

thread01 = Thread(
    interval=5,
    execute=minha_funcao,
    stop_time_interval=stop_time_interval_thread01, # Opcional: caso necessite pausar a execucao da thread por um intervalo de tempo.
    param1='valor1', param2=222, param3='valor3', ..., param100='valor100'
)
```

#### Parâmetros:

A classe Thread possui 3 parâmetros, sendo ***interval*** e ***execute*** obrigatórios.

- interval (***inteiro***) [***obrigatório***] -> intervalo de tempo em segundos que você quer que seja executado a função.
- execute (***referência da função***) [***obrigatório***] -> nome da função (def) que você deseja executar, ***sem aspas***.
- stop_time_interval [***opcional***] -> parâmetro caso necessite pausar a execucao da thread por um intervalo de tempo.
- \*args [***opcional***] -> parâmetros da função que se deseja executar, separados por vírgula.

Os parâmetros em ****args*** podem ter qualquer nome e ser de qualquer tipo de dado, porém devem ser nomeados. Além disso podem ter a quantidade de ***zero*** até o ***número desejado*** de parâmetros.

#### 2) Utilização no Programa Principal 

- O decorator ***@thread_loop(*** sleep_time ***)*** deve englobar a função (def) que irá encapsular as Thread(s) e no final retornar a(s) Thread(s) em uma lista.
  
- **Somente a(s) Thread(s) retornadas na lista vão ser executada(s).**

Exemplo:

```python
def diga_uma_palavra(msg):
    print(msg)

def diga_um_numero(msg):
    print(msg)


@thread_loop(1)
def executa_servico():
    threads = []
    
    stop_time_interval_thread01 = {
        'thread_name': 'thread01',
        'inicio': '10:25',
        'fim': '10:48'
    }
    
    thread01 = Thread(
        interval=5,
        execute=diga_uma_palavra,
        stop_time_interval=stop_time_interval_thread01,
        msg='ola'
    )
    threads.append(thread01)

    thread02 = Thread(
        interval=3,
        execute=diga_um_numero,
        msg=123
    )
    threads.append(thread02)

    return threads


if __name__ == "__main__":
    executa_servico()
```

### 3) Tratamento de erros

- O Threads esta encapsulada com um ***try / except*** que faz o log do erro do tipo critical com o traceback completo, ela passa este erro para a camada do decorator ***thread_loop(sleep_time)*** que aguarda o próximo ciclo ***sleep_time*** para ser executado novamente, isto é, o serviço não vai parar, a menos que seja utilizado a sequência de teclas **CTRL+C**, neste caso o serviço irá finalizar a(s) Thread(s) em andamento e depois finalizar.
  
- Para finalizar o serviço **forçadamente**, basta utilizar a sequência de teclas **CTRL+C** duas vezes.

- Caso necessite tratar algum erro na funcao que a ***Thread*** chama ou qualquer outra funcao interna, bastar utilizar o comando ***try / except*** e gerar um raise com a classe de erro e a mensagem personalizada, se desejar. Este erro será capturado na camada da ***Thread*** e repassado para a camada do ***decorator***.

Exemplo:

```python
def divisao(a, b):
    try
        resultado = a / b
    except:
        raise Exception('Minha mensagem de erro personalizada.')
```

Neste caso se ***b*** for igual a zero, haverá uma except que será capturada tratada e repassada para as camadas superiores.