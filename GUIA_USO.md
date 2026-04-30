# 📖 Guia Rápido de Uso - Engaja Tube

## 🚀 Início Rápido

### 1️⃣ Instalação (Primeira vez)

**Windows:**
```bash
# Opção 1: Automático
install.bat

# Opção 2: Manual
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
pip3 install -r requirements.txt
```

### 2️⃣ Executar o Programa

```bash
python view.py
```

### 3️⃣ Usar a Interface

1. **Cole o link do vídeo** no campo "Link do vídeo"
   - Exemplo: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

2. **Escolha o número de instâncias**
   - Recomendado: 2-5 instâncias
   - Máximo: 20 instâncias

3. **Clique em "Iniciar Visualizações"**
   - O programa começará a abrir navegadores automaticamente
   - Cada navegador reproduzirá o vídeo

4. **Acompanhe o progresso**
   - **Visualizações totais**: Contador de quantas vezes o vídeo foi iniciado
   - **Status**: Mostra se está executando ou parado
   - **CPU/RAM**: Monitora o uso de recursos do computador

5. **Para parar**
   - Clique no botão "Parar"
   - Todos os navegadores serão fechados automaticamente

## ⚙️ Configurações Recomendadas

### Para Computadores Mais Fracos
- Use 2-3 instâncias
- Ative o modo headless (veja abaixo)
- Feche outros programas

### Para Computadores Potentes
- Use 5-10 instâncias
- Mantenha o modo visual para monitorar

### Ativar Modo Headless (Economizar Recursos)

1. Abra o arquivo `comandos.py` em um editor de texto
2. Encontre a linha (aproximadamente linha 48):
   ```python
   # options.add_argument('--headless')
   ```
3. Remova o `#` para descomentar:
   ```python
   options.add_argument('--headless')
   ```
4. Salve o arquivo

**Vantagem**: Economiza ~40% de recursos (navegadores sem interface gráfica)

## 🎯 Dicas e Truques

### Maximizar Eficiência
1. **Use modo headless** para mais instâncias simultâneas
2. **Monitore os recursos** - se CPU/RAM > 90%, reduza instâncias
3. **Deixe rodar** - o programa recria instâncias automaticamente

### Comportamento do Sistema
- Cada instância assiste o vídeo por **30-120 segundos** (aleatório)
- Quando uma instância termina, **outra é criada automaticamente**
- O sistema **pausa** se CPU ou RAM ultrapassar 90%

### Segurança
- O programa **não coleta dados** pessoais
- Usa apenas **automação de navegador**
- **Não modifica** arquivos do sistema

## 🔧 Solução de Problemas Comuns

### ❌ Erro: "Módulo não encontrado"
**Solução:**
```bash
pip install -r requirements.txt
```

### ❌ Navegador não abre
**Possíveis causas:**
1. Chrome não instalado → Instale o Google Chrome
2. Firewall bloqueando → Permita o Python no firewall
3. Antivírus bloqueando → Adicione exceção

**Solução:**
```bash
# Reinstale as dependências
pip uninstall selenium webdriver-manager
pip install selenium webdriver-manager
```

### ❌ "ChromeDriver não encontrado"
**Solução:**
- O programa baixa automaticamente
- Verifique sua conexão com internet
- Execute como administrador

### ❌ Computador muito lento
**Soluções:**
1. Reduza o número de instâncias para 1-2
2. Ative o modo headless
3. Feche outros programas
4. Verifique se tem RAM suficiente (mínimo 4GB)

### ❌ Vídeo não inicia automaticamente
**Isso é normal!** O programa tenta 3 métodos diferentes:
1. Clicar no botão play
2. Usar teclas de atalho
3. JavaScript

Se nenhum funcionar, o vídeo ainda conta como visualização (página foi carregada).

## 📊 Entendendo os Números

### Contador de Visualizações
- Mostra quantas **instâncias foram criadas**
- Cada instância = 1 tentativa de visualização
- **Não** é o contador oficial do YouTube

### Uso de Recursos
- **CPU**: Processamento do computador
- **RAM**: Memória utilizada
- Valores normais: CPU 20-60%, RAM 30-70%

### Instâncias Simultâneas
| Instâncias | RAM Necessária | CPU Necessária | Recomendado Para |
|------------|----------------|----------------|------------------|
| 1-2        | 2GB            | Dual-core      | PC Básico        |
| 3-5        | 4GB            | Quad-core      | PC Médio         |
| 6-10       | 8GB            | 6+ cores       | PC Potente       |
| 11-20      | 16GB+          | 8+ cores       | Workstation      |

## 🎓 Perguntas Frequentes

### ❓ As visualizações contam no YouTube?
O YouTube tem algoritmos sofisticados de detecção. Este projeto é **apenas educacional**.

### ❓ Posso usar em vídeos ao vivo?
Sim, funciona com qualquer link do YouTube (vídeos normais ou lives).

### ❓ Quanto tempo devo deixar rodando?
Você decide! O programa roda indefinidamente até você clicar em "Parar".

### ❓ Consome muita internet?
Sim, cada instância carrega o vídeo. Recomendado ter internet ilimitada.

### ❓ É seguro?
O código é open-source e você pode revisar. Não coleta dados nem modifica o sistema.

### ❓ Posso usar múltiplos vídeos?
Não simultaneamente. Você precisa parar e iniciar com novo link.

### ❓ Funciona em Mac/Linux?
Sim! Basta ter Python e Chrome instalados.

## 📞 Suporte

Se encontrar problemas:
1. Verifique a seção "Solução de Problemas" acima
2. Leia o README.md completo
3. Abra uma issue no GitHub

## ⚠️ Lembrete Legal

Este software é **apenas para fins educacionais**. O uso para manipular métricas pode violar os Termos de Serviço do YouTube. Use com responsabilidade e por sua conta e risco.

---

**Desenvolvido para estudo de Python e automação web** 🐍
