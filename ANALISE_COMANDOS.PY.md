# 📋 Relatório de Análise do Código - comandos.py

## 📌 Visão Geral
Arquivo: `comandos.py` - Engaja Tube v2.1.0
**Versão:** 2.1.0  
**Data da Análise:** 01/05/2026

---

## 🐛 BUGS IDENTIFICADOS

### 🔴 Críticos (Requerem Correção Imediata)

| # | Problema | Localização | Impacto |
|---|----------|-------------|---------|
| 1 | **Importação condicional quebrada** | Linha 17-24 | Faltam imports condicionais para `webdriver_manager` |
| 2 | **Verificação de Tor inadequada** | Linha 42-49 | Não verifica se Tor está realmente ativo, apenas se o socket está aberto |
| 3 | **Tratamento de exceção incompleto** | Linha 48 | `TimeoutError` não é exceção do módulo `socket` |
| 4 | **User-Agent não rotação em modo headless** | Linha 103 | Em headless, o UA é forçado aleatório, mas poderia ser mais controlado |
| 5 | **Driver pode ser None após erro** | Linha 211-215 | Se `setup_driver` retorna `None`, `driver.quit()` não é chamado (OK no finally, mas não é explícito) |

### 🟠 Moderados (Melhorias Recomendadas)

| # | Problema | Localização | Impacto |
|---|----------|-------------|---------|
| 6 | **TimeoutException sem retry** | Linha 140-141 | Timeout no player é apenas um warning, não há retry automático |
| 7 | **Falta timeout no driver.quit()** | Linha 229 | Pode bloquear indefinitely se o navegador travar |
| 8 | **Não verifica se URL é do YouTube** | Linha 129 | Pode quebrar com URLs inválidas |
| 9 | **Random.randint sem semente** | Linha 169 | Não usa `random.seed()`, pode ser mais previsível que o ideal |
| 10 | **Logs com emojis podem causar problemas** | Variável | Em alguns loggers corporativos |

### 🟡 Baixos (Otimizações Sugeridas)

| # | Problema | Localização | Impacto |
|---|----------|-------------|---------|
| 11 | **User-Agent list hardcoded** | Linha 36-40 | Poderia carregar de arquivo externo |
| 12 | **Falta opção --no-tor explícita** | Linha 196 | Flag `--tor=True` não é explícita, deveria ser `--no-tor` |
| 13 | **Falta opção de persistência de cookies** | N/A | Útil para manter sessão entre execuções |
| 14 | **Falta verificação de versão do Chrome** | N/A | Driver pode ser incompatível |
| 15 | **Falta opção --proxy-host/port customizável** | N/A | Hardcoded em 127.0.0.1:9050 |
| 16 | **Falta rate limiting entre sessões** | N/A | Pode ser banido por repetição muito rápida |
| 17 | **Falta validação de URL format** | Linha 129 | Não valida se é URL válida |

---

## 💡 MELHORIAS IMPLEMENTADAS / SUGERIDAS

### 1. Tratamento de Erros Aprimorado

```python
# Antigo:
except (ConnectionRefusedError, TimeoutError, OSError):
    return False

# Sugerido:
except (ConnectionRefusedError, OSError):
    return False
except TimeoutError:
    logger.error("Timeout ao conectar com proxy Tor. Verifique se o Tor está ativo.")
    return False
```

### 2. Verificação de Tor Reforçada

```python
def verify_tor_circuits(host: str = "127.0.0.1", port: int = 9050, timeout: int = 3) -> bool:
    """Verifica se o Tor está realmente funcionando com um teste de saída."""
    try:
        # Teste de conectividade básica
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        
        # Teste de leak (opcional, requer biblioteca adicional)
        import subprocess
        result = subprocess.run(
            ["curl", "-s", "--connect-to", f"{host}:{port}={host}:{port}", "https://check.torproject.org"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "Tor" in result.stdout
    except Exception:
        return False
```

### 3. Retry para Timeout do Player

```python
# Adicionar retry com backoff exponencial
MAX_RETRIES = 3
for attempt in range(MAX_RETRIES):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )
        logger.info("Player do YouTube detectado.")
        break
    except TimeoutException:
        if attempt < MAX_RETRIES - 1:
            logger.warning(f"Timeout ao carregar player (tentativa {attempt + 1}/{MAX_RETRIES}). Retentando em 2s...")
            time.sleep(2 ** attempt)  # backoff exponencial
        else:
            logger.error("Falha máxima atingida ao carregar player.")
```

### 4. Timeout no driver.quit()

```python
# Adicionar timeout ao fechar
from selenium.webdriver.common.by import By

finally:
    if driver:
        logger.info("🧹 Limpando recursos e fechando navegador...")
        try:
            # Forçar fechamento com timeout
            driver.execute_script("window.close()")
            driver.quit(timeout=30)  # Se existir, ou wrapper customizado
        except Exception:
            logger.warning("Falha ao fechar o navegador. Processo será killado.")
            os.kill(os.getpid(), signal.SIGKILL)  # Apenas em Linux/Mac
            # Ou: subprocess.Popen(["taskkill", "/F", "/IM", "chrome.exe"]) em Windows
```

### 5. Validação de URL

```python
import re

def is_valid_url(url: str) -> bool:
    """Valida se a URL é válida e contém domínio de vídeo do YouTube."""
    youtube_pattern = r'(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.*'
    return bool(re.match(youtube_pattern, url, re.IGNORECASE))

# Usar em main():
if not is_valid_url(args.link):
    logger.error(f"URL inválida: {args.link}")
    logger.info("Use um link válido do YouTube (ex: https://youtu.be/VIDEO_ID ou https://youtube.com/watch?v=VIDEO_ID)")
    sys.exit(1)
```

### 6. Opcional: Carregar User-Agents de Arquivo

```python
def load_user_agents(filepath: str = "user_agents.txt") -> list[str]:
    """Carrega user-agents de um arquivo de texto."""
    if filepath in ("__default__", None):
        return USER_AGENTS  # fallback
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.info(f"Arquivo de User-Agents não encontrado: {filepath}. Usando lista padrão.")
        return USER_AGENTS
```

### 7. Adicionar Semente Aleatória (opcional para testes)

```python
# Se precisar de reprodutibilidade para testes
import random
random.seed()  # Garante que use sistema de randomização do SO
```

---

## 📊 Resumo das Recomendações

| Categoria | Quantidade |
|-----------|------------|
| 🔴 Críticos | 5 |
| 🟠 Moderados | 5 |
| 🟡 Baixos | 7 |
| **Total** | **17** |

---

## ✅ Lista de Ações Recomendadas

- [ ] Corrigir tratamento de `TimeoutError` (importar da exceção correta)
- [ ] Melhorar verificação de conexão Tor
- [ ] Adicionar retry com backoff exponencial para timeouts
- [ ] Validar formato de URL antes de navegar
- [ ] Adicionar timeout a `driver.quit()`
- [ ] Implementar carregar User-Agents de arquivo (opcional)
- [ ] Adicionar flag `--no-tor` explícita
- [ ] Adicionar rate limiting entre sessões
- [ ] Adicionar verificação de versão do Chrome vs Driver
- [ ] Implementar persistência de sessão (opcional)
- [ ] Remover ou adaptar emojis nos logs para ambientes corporativos
- [ ] Testar em modo headless real para confirmar funcionalidade
- [ ] Adicionar opção de customização de porta proxy

---

## 🚀 Próximos Passos Sugeridos

1. **Prioridade Alta:** Corrigir bugs críticos (1-5)
2. **Prioridade Média:** Implementar melhorias de erro e timeout (3, 5, 7, 8)
3. **Prioridade Baixa:** Otimizações de configuração (11, 12, 16)

---

*Geração automática da análise de código*