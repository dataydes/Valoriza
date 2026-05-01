# Guia de Uso: Simulação de IP e Região

## O que é?
Funcionalidade para simular acesso do YouTube de diferentes regiões/países usando proxies e User-Agents variados.

## Como Usar

### No Aplicativo (Interface Gráfica)

1. Abra o **Engaja Tube**
2. Cole o link do vídeo
3. Escolha o número de instâncias simultâneas
4. Selecione a **Região** desejada no dropdown (Brasil, EUA, Reino Unido, etc.)
5. Clique em **Iniciar Visualizações**

O software usará:
- **User-Agent** específico para a região selecionada
- **Proxy** da região (se configurado)
- Comportamento de navegação realista

### Uso Direto via Terminal

```bash
# Visualização básica
python comandos.py https://youtube.com/watch?v=VIDEO_ID

# Com User-Agent específico
python comandos.py https://youtube.com/watch?v=VIDEO_ID --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Com proxy personalizado
python comandos.py https://youtube.com/watch?v=VIDEO_ID --proxy "http://usuario:senha@proxy:8080"

# Com região específica
python comandos.py https://youtube.com/watch?v=VIDEO_ID --region "EUA" --user-agent "Google Chrome Windows"

# Combinado (proxy + user-agent)
python comandos.py https://youtube.com/watch?v=VIDEO_ID --proxy "http://177.55.67.185:8080" --region "EUA"
```

## Proxies Disponíveis

### O que são proxies?
Proxies são servidores intermediários que fazem o vídeo parecer acessado de outro país.

### Proxies Gratuitos (Lista Básica)

**EUA:**
- `http://177.55.67.185:8080`
- `http://166.62.68.195:8080`
- `http://23.185.202.126:3128`

**Europa:**
- `http://23.185.113.45:8080`
- `http://23.185.22.155:3128`
- `http://185.162.230.159:3128`

**Japão:**
- `http://203.105.134.86:8080`
- `http://103.224.238.24:3128`

**Austrália:**
- `http://45.249.12.127:8080`

**Canadá:**
- `http://45.66.147.248:3128`

### Como Usar Proxies

1. **Encontre um proxy** da região desejada
2. **Substitua** a linha `http://proxy-usuario:senha@proxy-eua:8080` no arquivo `comandos.py` pelo proxy real
3. **Execute** com o comando ou interface gráfica

### Configuração Avançada (Proxy com Autenticação)

Se seu proxy exigir login:
```
http://usuario:senha@ip:porta
```
Exemplo:
```
http://meuusuario:musenha@203.105.134.86:8080
```

## User-Agents por Região

| Região | User-Agent Padrão |
|--------|-------------------|
| EUA | Google Chrome Windows |
| UK | Firefox Windows |
| Alemanha | Chrome Linux |
| Japão | Safari iOS |
| Austrália | Chrome Windows |
| Canadá | Chrome macOS |
| França | Firefox Linux |

## Dicas de Uso

### Para Evitar Bloqueios

1. **Use proxies rotativos** - Não use o mesmo proxy por muito tempo
2. **Váris regiões** - Distribua visualizações entre diferentes países
3. **Comportamento humano** - O software já simula interações naturais
4. **Tempo de visualização** - Entre 30s-2min por vídeo

### Performance

- **Brasil**: Não precisa de proxy (use diretamente)
- **Outras regiões**: Use proxy da região alvo
- **Proxies lentos**: Reduzam o número de instâncias

## Importante

⚠️ **Atenção:**
- Proxies gratuitos podem ter limites de uso
- IP público pode ser detectado pelo YouTube
- Para maior anonimato, use proxies rotativos
- O YouTube detecta alguns comportamentos bot

### Recomendações

1. **Para uso casual**: Use regiões brasileiras
2. **Para diversificação**: Use múltiplas regiões diferentes
3. **Para máxima segurança**: Use sua própria lista de proxies pagos
4. **Rotacione**: Alterne entre regiões para evitar padrões detectáveis

## Exemplos de Comando

```bash
# 1. Visualização direta (Brasil)
python comandos.py https://youtube.com/watch?v=dQw4w9WgXcQ

# 2. Simular acesso dos EUA
python comandos.py https://youtube.com/watch?v=dQw4w9WgXcQ --region "EUA" --user-agent "Google Chrome Windows"

# 3. Simular acesso do Japão com proxy
python comandos.py https://youtube.com/watch?v=dQw4w9WgXcQ --proxy "http://203.105.134.86:8080" --region "Japão"

# 4. Múltiplas visualizações simultâneas
python comandos.py https://youtube.com/watch?v=dQw4w9WgXcQ --region "EUA" --user-agent "Google Chrome Windows" &
python comandos.py https://youtube.com/watch?v=dQw4w9WgXcQ --region "UK" --user-agent "Firefox Windows" &
python comandos.py https://youtube.com/watch?v=dQw4w9WgXcQ --region "DE" --user-agent "Chrome Linux" &
```

## Solução de Problemas

### "Não estou acessando da região correta"
- Verifique se o proxy está funcionando
- Tente outro proxy da mesma região
- Aguarde alguns minutos entre tentativas

### "Visualizações não estão contando"
- Verifique se o vídeo está reproduzindo
- O User-Agent pode estar bloqueado - tente outro
- O proxy pode estar lento ou bloqueado

### "Erro de conexão no proxy"
- O proxy pode estar offline
- Tente outro proxy
- Verifique a sintaxe do proxy (inclua `http://` e `:8080`)

---
**Versão do Software**: 2.0.3
**Última Atualização**: Janeiro 2026