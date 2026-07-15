# Trading / Inversiones

## `claude-trading-skills/` (tradermonty · MIT)
Toolkit de ~60 skills para inversores/traders: screeners **VCP**, **CANSLIM**, **FinViz**,
**value-dividend**, momentum, análisis de sector, breadth, calendarios (earnings/económico),
detección de burbuja, análisis fundamental+técnico de acciones US, y más.
- 5 skills funcionan **sin API pagada** (CSVs públicos). El resto usa Financial Modeling Prep
  (free tier 250 req/día); algunas Alpaca (portafolio) o FinViz Elite (opcional).
- Revisado por seguridad → limpio.

## Pendiente: `analisis-inversion` (skill propia)
- Enfoque **screener/filtros** para TradingView.
- **Base:** el HTML de inversiones que Matías le pidió a un amigo. Cuando llegue, se fusionan sus
  criterios con los screeners de `claude-trading-skills`.
- Evaluar también el MCP `atilaahmettaner/tradingview-mcp` (data en vivo + backtesting).

> Nota: los MCPs de inversión del catálogo de tu amigo (CoinGecko gratis, TradingView, altFINS,
> Dune, CoinMarketCap) son config, no skills — se enganchan al armar `analisis-inversion`.
