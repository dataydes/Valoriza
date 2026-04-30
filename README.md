# Valoriza - Engaja Tube

## 📋 Descrição
Aplicativo desenvolvido em Python para automatizar visualizações de vídeos do YouTube. O sistema gerencia múltiplas instâncias de navegador simultaneamente, com controle de recursos do sistema e contador de visualizações em tempo real.

## ⚠️ Aviso Legal
Este projeto foi criado apenas para fins educacionais e de estudo da linguagem Python. O uso deste software para manipular métricas do YouTube pode violar os Termos de Serviço da plataforma. Use por sua conta e risco.

## ✨ Funcionalidades

- **Interface Gráfica Intuitiva**: Interface Tkinter amigável e fácil de usar
- **Múltiplas Instâncias**: Abre várias janelas do navegador simultaneamente
- **Controle de Recursos**: Monitora CPU e RAM para evitar sobrecarga do sistema
- **Contador de Visualizações**: Acompanha quantas visualizações foram iniciadas
- **Loop Automático**: Mantém as instâncias rodando continuamente até você parar
- **Comportamento Humano**: Simula interações naturais com tempos aleatórios
- **Gerenciamento Inteligente**: Recria instâncias automaticamente quando finalizam

## 🚀 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- Google Chrome instalado
- Windows, Linux ou macOS

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/dataydes/Valoriza.git
cd Valoriza
```

2. **Instale as dependências**

**Windows:**
```bash
pip install -r requirements.txt
```

Ou use o arquivo de instalação automática:
```bash
install.bat
```

**Linux/macOS:**
```bash
pip3 install -r requirements.txt
```

## 📖 Como Usar

1. **Execute o aplicativo**
```bash
python view.py
```

2. **Na interface:**
   - Cole o link do vídeo do YouTube no campo "Link do vídeo"
   - Escolha o número de instâncias simultâneas (recomendado: 2-5)
   - Clique em "Iniciar Visualizações"
   - Acompanhe o contador e o uso de recursos
   - Clique em "Parar" quando quiser encerrar

## 🎯 Melhores Práticas Implementadas

### 1. **Gerenciamento de Recursos**
- Monitoramento em tempo real de CPU e RAM
- Limite automático quando recursos excedem 90%
- Verificação de RAM disponível antes de iniciar

### 2. **Otimização de Performance**
- Modo headless opcional (descomente no código para economizar recursos)
- Áudio silenciado automaticamente
- Logs reduzidos para melhor performance
- Limpeza automática de processos finalizados

### 3. **Comportamento Natural**
- Tempo de visualização aleatório (30-120 segundos)
- Simulação de scroll e interações
- Delays entre criação de instâncias
- Múltiplos métodos para iniciar vídeos

### 4. **Robustez**
- Tratamento de erros em todas as operações
- Múltiplos métodos de fallback para iniciar vídeos
- Finalização segura de processos
- Confirmação antes de sair com processos ativos

### 5. **Interface Amigável**
- Feedback visual do status
- Contador de visualizações em tempo real
- Monitoramento de recursos
- Botões coloridos e intuitivos

## ⚙️ Configurações Avançadas

### Modo Headless (Sem Interface Gráfica do Navegador)
Para economizar recursos, edite `comandos.py` e descomente a linha:
```python
options.add_argument('--headless')
```

### Ajustar Tempo de Visualização
Em `comandos.py`, linha 107, modifique:
```python
tempo_visualizacao = random.randint(30, 120)  # Valores em segundos
```

### Limites de Recursos
Em `view.py`, linha 177, ajuste os limites:
```python
if cpu > 90 or ram > 90:  # Altere os valores conforme necessário
```

## 📊 Especificações Técnicas

### Dependências
- **selenium**: Automação do navegador
- **webdriver-manager**: Gerenciamento automático do ChromeDriver
- **psutil**: Monitoramento de recursos do sistema
- **tkinter**: Interface gráfica (incluído no Python)

### Requisitos de Sistema Recomendados
- **RAM**: Mínimo 4GB (8GB+ recomendado)
- **CPU**: Dual-core ou superior
- **Conexão**: Internet estável

### Consumo Aproximado por Instância
- **RAM**: ~200-300MB
- **CPU**: ~5-10%

## 🔧 Solução de Problemas

### Erro: "ChromeDriver não encontrado"
- O webdriver-manager baixa automaticamente. Verifique sua conexão com a internet.

### Erro: "psutil não instalado"
```bash
pip install psutil
```

### Navegador não abre
- Verifique se o Google Chrome está instalado
- Tente executar como administrador

### Alto uso de recursos
- Reduza o número de instâncias simultâneas
- Ative o modo headless
- Feche outros programas

## 📝 Estrutura do Projeto

```
Valoriza/
│
├── view.py                 # Interface gráfica principal
├── comandos.py            # Script de automação do navegador
├── requirements.txt       # Dependências do projeto
├── install.bat           # Instalador automático (Windows)
├── README.md             # Este arquivo
├── .gitignore           # Arquivos ignorados pelo Git
│
├── src/                 # Recursos (ícones, etc.)
│   └── icon.ico
│
└── IA/                  # Scripts adicionais
    ├── comandosIA.py
    ├── example_usage.py
    └── ...
```

## 🎓 Aprendizados e Técnicas Utilizadas

- **Threading**: Para execução paralela sem travar a interface
- **Subprocess**: Gerenciamento de múltiplos processos
- **Selenium WebDriver**: Automação de navegador
- **Tkinter**: Criação de interface gráfica
- **Monitoramento de Sistema**: Uso de psutil para recursos
- **Tratamento de Exceções**: Código robusto e à prova de falhas
- **Padrões de Projeto**: Orientação a objetos e separação de responsabilidades

## 🚀 Gerar Executável

Para criar um arquivo .exe (Windows):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=src/icon.ico view.py
```

O executável estará em `dist/view.exe`

## 📄 Licença

Este projeto é fornecido "como está" para fins educacionais. Use com responsabilidade.

## 👨‍💻 Autor

Desenvolvido como ferramenta de estudo da linguagem Python.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Nota**: Este software é apenas para fins educacionais. O autor não se responsabiliza pelo uso indevido desta ferramenta.
