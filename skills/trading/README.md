# Trading / Inversiones

## `claude-trading-skills/` (tradermonty · MIT)
Toolkit de 64 skills para inversores/traders. Incluye screeners que le gustaron a Matías:
- **VCP** (Minervini), **CANSLIM** (O'Neil), **FinViz**, **value-dividend** (P/E<20, P/B<2, yield≥3%),
  **stockbee momentum**, sector rotation, market breadth, etc.
- 5 skills funcionan **sin API pagada** (usan CSVs públicos del autor).
- El resto usa **Financial Modeling Prep** (free tier: 250 req/día). Algunas usan Alpaca (portafolio) o FinViz Elite (opcional).
- Vendorizado como referencia/base. Revisado por seguridad (McAfee real-time + escaneo de patrones + dominios de red → limpio).

## Pendiente: `analisis-inversion` (skill propia)
- **Enfoque elegido:** screener/filtros para TradingView.
- **Base:** el HTML de inversiones que Matías le pidió a un amigo (contiene criterios avanzados).
  Cuando llegue, se fusionan esos criterios con los screeners de `claude-trading-skills`.
- **Estado:** en espera del material del amigo antes de escribir la skill.

## Pendiente: MCP de TradingView
- `atilaahmettaner/tradingview-mcp` — server MCP con data en vivo, indicadores, screeners y backtesting.
- Da el puente real con TradingView (config MCP, no skill). Evaluar cuando arranquemos `analisis-inversion`.
