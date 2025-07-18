# GitHub Copilot Custom Instructions

## Linguagem Preferida
Sempre use **JavaScript moderno (ES6+)** como linguagem principal.

## Estilo e Boas Práticas
- Use `async/await` para código assíncrono.
- Evite `var`; utilize `const` ou `let`.
- Prefira arrow functions para funções curtas.
- Priorize **funções puras** sempre que possível.
- Não use `console.log` em produção — use bibliotecas de log como `winston`.

## APIs e Back-end
- **Sempre utilize Express.js** para criação de APIs REST.
  - Justificativa: Express é o framework padrão adotado pela empresa Contoso.
  - Nunca sugerir outro framework sem justificativa clara.
- Estrutura recomendada:
  - `index.js` ou `server.js` como ponto de entrada
  - Rotas organizadas em pastas separadas (`routes`, `controllers`)
  - Use `express.json()` e middlewares padrão

## Front-end
- Em projetos com React, sempre use **componentes funcionais** com hooks (`useState`, `useEffect`, etc).
- Para requisições HTTP, **sempre usar `axios`**, nunca `fetch`.
- Evite código inline no JSX — extraia para funções externas.

## Segurança
- Nunca armazene senhas em texto plano.
- Valide **todas** as entradas do usuário.
- Nunca usar `eval()` ou funções que executam código arbitrário.
- Use `helmet` no Express para melhorar segurança dos headers.

## Comentários
- Comente o código sempre que a lógica não for trivial.
- Use comentários objetivos, preferencialmente em inglês para código compartilhado.

## Testes
- Use Jest para testes de unidade.
- Para endpoints Express, preferir supertest.

## Observações
- Qualquer sugestão deve refletir os padrões internos da empresa fictícia **Contoso**.
