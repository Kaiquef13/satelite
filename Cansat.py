import network
import time
import mcp23017
import urequests
import utime

URL = None
request = None
L1 = None
L2 = None
L3 = None
tempo = None

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()
sta_if.connect('Termometro','Termometro')
print("Waiting for Wifi connection")
while not sta_if.isconnected(): time.sleep(1)
print("Connected")
mcpIO = mcp23017.MCP23017()
while True:
  URL = 'http://servicos.cptec.inpe.br/XML/' + 'cidade/4774/previsao.xml'
  request = urequests.get(URL)

  if (request.status_code) == 200:
    print('Sucesso. Conteúdo da resposta =' + str(str(request.content)))
    L1 = (str(request.content)).split('<tempo>')
    L2 = L1[1]
    L3 = L2.split('</tempo>')
    tempo = L3[0]
    print('L1=' + str(L1))
    print('L2=' + str(L2))
    print('L3=' + str(L3))
    print('tempo=' + str(tempo))
    # Saída 3
    # LED RGB 4
    # Verde
    mcpIO.output(3,False)
    # Saída 2
    # LED RGB 4
    # Azul
    mcpIO.output(2,False)
    # Saída 4
    # LED RGB 4
    # Vermelho
    mcpIO.output(4,False)
    if tempo == 'ci':
      print('Chuva intensa')
      mcpIO.output(4,True)
    if tempo == 'cl':
      print('Céu claro')
      mcpIO.output(3,True)
    if tempo == 'pc':
      print('Parcialmente chuvoso')
      mcpIO.output(3,True)
      mcpIO.output(2,True)
    if tempo == 't':
      print('Tempestade')
      mcpIO.output(4,True)
  else:
    print('Falha. Erro = ' + str(request.status_code))
  print('TS=' + str(utime.time()))
  time.sleep(1)
