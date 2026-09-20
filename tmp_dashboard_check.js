
    const $ = (selector) => document.querySelector(selector);
    const watchlistKey = "financeanalytics-watchlist";
    const alertsKey = "financeanalytics-alerts";
    const state = { results: [] };

    const stripAnsi = (text) => String(text ?? "").replace(/\u001b\[[0-9;]*m/g, "");
    const formatScore = (value) => value == null ? "N/A" : `${Number(value).toFixed(1)}/100`;
    const formatValue = (value) => {
      if (value == null) return "N/A";
      if (typeof value === "number") {
        if (Math.abs(value) >= 1000000000) return `${(value / 1000000000).toFixed(2)} Mdâ‚¬`;
        if (Math.abs(value) >= 1000000) return `${(value / 1000000).toFixed(2)} Mâ‚¬`;
        return value.toFixed(2);
      }
      if (Array.isArray(value)) return value.map(formatValue).join(" â€“ ");
      if (typeof value === "object") {
        if (typeof value.ratio === "number") return `${value.ratio.toFixed(2)} : 1`;
        if (typeof value.ratio === "string") return `${Number(value.ratio).toFixed(2)} : 1`;
        if (typeof value.reward === "number" && typeof value.risk === "number") return `${(value.reward / value.risk).toFixed(2)} : 1`;
        return "N/A";
      }
      return stripAnsi(value);
    };
    const formatPct = (value) => value == null ? "N/A" : `${Number(value).toFixed(1)}%`;
    const formatText = (value) => stripAnsi(value ?? "");
    const safeTicker = (value) => (value || "").trim().toUpperCase();

    function parseTickers(value) {
      return value.split(",").map(item => item.trim()).filter(Boolean).map(safeTicker);
    }
    function scoreBar(name, value) {
      return `<div class="bar-line"><span>${name}</span><div class="bar"><i style="width:${Math.max(0, Math.min(100, value || 0))}%"></i></div><strong>${formatScore(value)}</strong></div>`;
    }

    function getWatchlist() {
      try { return JSON.parse(localStorage.getItem(watchlistKey) || "[]"); } catch { return []; }
    }
    function setWatchlist(items) {
      localStorage.setItem(watchlistKey, JSON.stringify(items));
    }
    function getAlerts() {
      try { return JSON.parse(localStorage.getItem(alertsKey) || "[]"); } catch { return []; }
    }
    function setAlerts(items) {
      localStorage.setItem(alertsKey, JSON.stringify(items));
    }

    function parseComparableValue(rawValue) {
      if (rawValue == null || rawValue === "") return null;
      const text = String(rawValue).trim();
      const normalized = text.replace(/\s+/g, "").replace(/\u00a0/g, "");
      if (!normalized) return null;
      const cleaned = normalized.replace(/[$â‚¬Â£]/g, "").replace(/%/g, "");
      const asNumber = Number(cleaned.replace(/x$/i, "").replace(",", "."));
      if (!Number.isFinite(asNumber)) return null;
      return asNumber;
    }

    function formatComparableValue(rawValue) {
      const value = parseComparableValue(rawValue);
      if (value == null) return "N/A";
      const text = String(rawValue).trim();
      if (/x$/i.test(text)) return `${value.toFixed(2)}x`;
      if (/%$/.test(text)) return `${value.toFixed(1)}%`;
      return Number(value).toFixed(2);
    }

    function getComparableMetrics(result) {
      const metricMap = {};
      const relevantCategories = ["Valorisation", "RentabilitÃ©", "LiquiditÃ©", "SolvabilitÃ©", "Risque & MarchÃ©"];
      for (const category of relevantCategories) {
        const rows = result?.fundamental?.[category] || [];
        for (const row of rows) {
          const label = String(row["Indicateur"] || "").trim();
          if (!label) continue;
          const lower = label.toLowerCase();
          if (/(prix|capitalisation|market cap|valeur marchande)/i.test(lower)) continue;
          metricMap[label] = row["Valeur"];
        }
      }
      return metricMap;
    }

    function buildComparison(results) {
      if (!results || results.length < 2) return "";
      const [left, right] = results.slice(0, 2);
      const leftMetrics = getComparableMetrics(left);
      const rightMetrics = getComparableMetrics(right);
      const labels = Object.keys(leftMetrics).filter((label) => Object.prototype.hasOwnProperty.call(rightMetrics, label));
      const preferredOrder = [
        "Forward P/E",
        "Trailing PE",
        "Price to Book",
        "PEG Ratio",
        "Dividend Yield",
        "ROE",
        "ROA",
        "EBITDA Margin",
        "Operating Margin",
        "Net Margin",
        "Current Ratio",
        "Quick Ratio",
        "Debt to Equity",
        "Gross Margin",
      ];

      const orderedLabels = [...new Set([...preferredOrder.filter((label) => labels.includes(label)), ...labels])].slice(0, 10);
      const rows = orderedLabels.map((label) => {
        const a = leftMetrics[label];
        const b = rightMetrics[label];
        const aNum = parseComparableValue(a);
        const bNum = parseComparableValue(b);
        if (aNum == null || bNum == null) return "";
        const delta = bNum - aNum;
        const deltaLabel = `${delta >= 0 ? "+" : ""}${Number(delta).toFixed(2)}`;
        const suffix = /x$/i.test(String(a)) || /x$/i.test(String(b)) ? "x" : /%$/.test(String(a)) || /%$/.test(String(b)) ? "%" : "";
        return `<div class="comparison-row"><span class="label">${label}</span><div class="value">${formatComparableValue(a)} <small>vs</small> ${formatComparableValue(b)}</div><span class="delta">Î” ${deltaLabel}${suffix}</span></div>`;
      }).filter(Boolean).join("");

      if (!rows) {
        return `<div class="panel"><div class="panel-head"><h2>Comparaison entre ${left.ticker} et ${right.ticker}</h2><span class="tag">Valeurs comparables</span></div><div class="empty">Aucun indicateur financier directement comparable n'a Ã©tÃ© trouvÃ© pour ces deux titres.</div></div>`;
      }

      return `<div class="panel"><div class="panel-head"><h2>Comparaison entre ${left.ticker} et ${right.ticker}</h2><span class="tag">Valeurs comparables</span></div><div class="comparison-grid">${rows}</div></div>`;
    }

    function sectorSummary(results) {
      if (!results || !results.length) return "";
      const bySector = {};
      for (const result of results) {
        const sector = result.sector || "Autre";
        if (!bySector[sector]) bySector[sector] = { total: 0, count: 0 };
        bySector[sector].total += Number(result.scores.global || 0);
        bySector[sector].count += 1;
      }
      const rows = Object.entries(bySector).map(([sector, stats]) => {
        const avg = stats.total / stats.count;
        return `<div class="comparison-row"><span class="label">${sector}</span><div class="value">${formatScore(avg)}</div><span class="delta">${stats.count} titre(s)</span></div>`;
      }).join("");
      return `<div class="panel"><div class="panel-head"><h2>Benchmark sectoriel</h2><span class="tag">Comparatif</span></div><div class="comparison-grid">${rows}</div></div>`;
    }

    function screenerTable(results) {
      const minScore = Number($('#screenerMinScore')?.value || 60);
      const minMarketCap = Number($('#screenerMinCap')?.value || 0) * 1000000;
      const matches = results.filter((item) => {
        const score = Number(item.scores.global || 0);
        const marketCap = Number(item.market_cap || 0);
        return score >= minScore && marketCap >= minMarketCap;
      });
      if (!matches.length) {
        return '<div class="empty">Aucun titre ne correspond aux filtres du scanner.</div>';
      }
      return `<div class="table-wrap"><table><thead><tr><th>Ticker</th><th>Secteur</th><th>Score</th><th>Prix</th><th>Cap. boursiÃ¨re</th></tr></thead><tbody>${matches.map((item) => `<tr><td>${item.ticker}</td><td>${item.sector || "â€”"}</td><td><span class="score-pill">${formatScore(item.scores.global)}</span></td><td>${formatValue(item.price)}</td><td>${formatValue(item.market_cap)}</td></tr>`).join("")}</tbody></table></div>`;
    }

    function renderCompanyPanel(result) {
      const s = result.scores || {};
      const fib = result.fibonacci || {};
      const fa = fib.analysis || {};
      const perf = result.performance || {};
      const fundamentalRows = Object.entries(result.fundamental || {}).flatMap(([category, rows]) => rows.map(row => `<tr><td>${category}</td><td>${row.Indicateur || "â€”"}</td><td>${row.Valeur || "â€”"}</td><td><span class="score-pill">${row["Note (/10)"]}/10</span></td></tr>`)).join("");
      const technicalRows = (result.technical || []).map(row => `<tr><td>${row.Indicateur || "â€”"}</td><td>${formatValue(row.Valeur)}</td><td><span class="score-pill">${row["Note (/10)"]}/10</span></td><td>${row.InterprÃ©tation || "â€”"}</td></tr>`).join("");
      const perfGrid = [
        ["1M", perf["1M"]],
        ["3M", perf["3M"]],
        ["1Y", perf["1Y"]],
      ].map(([label, value]) => `<div class="metric"><small>${label}</small><strong>${formatPct(value)}</strong></div>`).join("");

      return `<div class="panel"><div class="panel-head"><h2>${formatText(result.company || result.ticker)}</h2><div style="display:flex;align-items:center;gap:8px"><span class="tag">${result.ticker}</span><button class="secondary" data-ticker="${result.ticker}" data-company="${result.company || result.ticker}" style="height:28px;padding:0 10px;">Ajouter Ã  la veille</button></div></div><div class="layout"><div><div class="panel" style="padding:16px;margin:0 0 18px"><h2 style="margin-bottom:10px">SynthÃ¨se</h2><div class="comparison-grid"><div class="comparison-row"><span class="label">Score global</span><div class="value">${formatScore(s.global)}</div></div><div class="comparison-row"><span class="label">Score fondamental</span><div class="value">${formatScore(s.fundamental)}</div></div><div class="comparison-row"><span class="label">Score technique</span><div class="value">${formatScore(s.technical)}</div></div><div class="comparison-row"><span class="label">Prix</span><div class="value">${formatValue(result.price)}</div></div></div></div><div class="panel" style="padding:16px;margin:0 0 18px"><h2 style="margin-bottom:10px">Performance</h2><div class="fib-grid">${perfGrid}</div></div><div class="panel" style="padding:16px;margin:0"><div class="panel-head"><h2>Indicateurs fondamentaux</h2></div><div class="table-wrap"><table><thead><tr><th>CatÃ©gorie</th><th>Indicateur</th><th>Valeur</th><th>Note</th></tr></thead><tbody>${fundamentalRows || "<tr><td colspan=4>Aucune donnÃ©e disponible</td></tr>"}</tbody></table></div></div></div><div><div class="panel" style="padding:16px;margin:0 0 18px"><h2 style="margin-bottom:10px">Lecture technique</h2><div class="table-wrap"><table><thead><tr><th>Indicateur</th><th>Valeur</th><th>Note</th><th>Lecture</th></tr></thead><tbody>${technicalRows || "<tr><td colspan=4>Aucune donnÃ©e disponible</td></tr>"}</tbody></table></div></div><div class="panel" style="padding:16px;margin:0"><h2 style="margin-bottom:10px">Zones clÃ©s & Fibonacci</h2><div class="fib-grid">${[["Support",fa.support],["RÃ©sistance",fa.resistance],["Stop-loss",fa.stop_loss],["Zone d'entrÃ©e",Array.isArray(fa.entry_zone) ? fa.entry_zone.map(formatValue).join(" â€“ ") : fa.entry_zone],["Ratio R/R",fa.risk_reward]].map(([label,value]) => `<div class="metric"><small>${label}</small><strong>${formatValue(value)}</strong></div>`).join("")}</div><p class="subtitle" style="margin-top:15px">${formatText(fa.interpretation || "Analyse Fibonacci non disponible.")}</p></div></div></div></div>`;
    }

    function renderWatchlist() {
      const items = getWatchlist();
      if (!items.length) return `<div class="empty">Aucun titre dans votre veille pour le moment.</div>`;
      return `<div class="watchlist">${items.map(item => `<span class="watch-item">${item.ticker} <strong>${formatScore(item.score)}</strong></span>`).join("")}</div>`;
    }

    function renderAlertsPanel() {
      const items = getAlerts();
      if (!items.length) return `<div class="empty">Aucune alerte active.</div>`;
      return `<div class="alert-list">${items.map(item => `<span class="alert-item">${item.ticker} â‰¥ ${formatScore(item.score)}</span>`).join("")}</div>`;
    }

    function render(results) {
      state.results = results || [];
      if (!state.results.length) {
        $("#content").innerHTML = '<div class="panel empty">Aucune donnÃ©e Ã  afficher.</div>';
        return;
      }

      const bestScore = [...state.results].sort((a, b) => (b.scores.global || 0) - (a.scores.global || 0))[0];
      const avgScore = state.results.reduce((sum, item) => sum + (item.scores.global || 0), 0) / state.results.length;
      $("#overview").innerHTML = [
        ["Titres suivis", state.results.length, state.results.length > 1 ? "Comparaison active" : "Focus sur 1 titre"],
        ["Mieux notÃ©", bestScore ? bestScore.ticker : "â€”", bestScore ? `${formatText(bestScore.company || bestScore.ticker)}` : "Aucune donnÃ©e"],
        ["Score moyen", formatScore(avgScore), "Moyenne des notes globales"],
        ["Recommandation", state.results.some(r => r.recommendation) ? state.results.map(r => `${r.ticker}: ${formatText(r.recommendation || "N/A")}`).join(" â€¢ ") : "Aucune", "Vue de synthÃ¨se"],
      ].map(([label, value, note]) => `<div class="card"><div class="card-label">${label}</div><div class="card-value">${value}</div><div class="card-change">${note}</div></div>`).join("");

      const comparison = buildComparison(state.results);
      const sector = sectorSummary(state.results);
      const details = state.results.map(renderCompanyPanel).join("");
      const screener = `
        <div class="panel" id="screenerPanel">
          <div class="panel-head"><h2>Scanner de valeur</h2><span class="tag">Filtres</span></div>
          <div class="filter-grid">
            <div class="field"><label for="screenerMinScore">Score global min</label><input id="screenerMinScore" type="number" min="0" max="100" value="60"></div>
            <div class="field"><label for="screenerMinCap">Cap. min (Mâ‚¬)</label><input id="screenerMinCap" type="number" min="0" value="0"></div>
          </div>
          <div id="screenerResults" style="margin-top:14px;">${screenerTable(state.results)}</div>
        </div>
      `;

      $("#content").innerHTML = `${comparison}${sector}${screener}${details}<div class="panel"><h2>Veille personnalisÃ©e</h2><div id="watchlist-content">${renderWatchlist()}</div></div><div class="panel"><h2>Alertes automatiques</h2><div class="filter-grid"><div class="field"><label for="alertThreshold">Score de dÃ©clenchement</label><input id="alertThreshold" type="number" min="0" max="100" value="75"></div></div><button class="primary" id="addAlert" type="button" style="margin-top:12px;">CrÃ©er une alerte</button><div id="alertList" style="margin-top:18px;">${renderAlertsPanel()}</div></div>`;

      $("#content").querySelectorAll("[data-ticker]").forEach((button) => {
        button.addEventListener("click", () => {
          const ticker = button.dataset.ticker;
          const company = button.dataset.company;
          const existing = getWatchlist();
          const match = existing.find(item => item.ticker === ticker);
          const next = match ? existing : [...existing, { ticker, company, score: state.results.find(item => item.ticker === ticker)?.scores?.global ?? null }];
          setWatchlist(next);
          button.textContent = "AjoutÃ©";
          button.disabled = true;
          const watchlistContent = document.getElementById("watchlist-content");
          if (watchlistContent) watchlistContent.innerHTML = renderWatchlist();
        });
      });

      $('#addAlert')?.addEventListener('click', () => {
        const threshold = Number($('#alertThreshold')?.value || 75);
        const items = getAlerts();
        const ticker = state.results[0]?.ticker || 'TICKER';
        const next = [...items.filter(item => item.ticker !== ticker), { ticker, score: threshold }];
        setAlerts(next);
        $('#alertList').innerHTML = renderAlertsPanel();
      });

      $('#screenerMinScore')?.addEventListener('input', () => {
        if (document.getElementById('screenerResults')) {
          document.getElementById('screenerResults').innerHTML = screenerTable(state.results);
        }
      });
      $('#screenerMinCap')?.addEventListener('input', () => {
        if (document.getElementById('screenerResults')) {
          document.getElementById('screenerResults').innerHTML = screenerTable(state.results);
        }
      });
    }

    function exportCsv() {
      if (!state.results.length) return;
      const rows = [
        ["Ticker", "Entreprise", "Secteur", "Score global", "Score fondamental", "Score technique", "Prix", "Cap. boursiÃ¨re"],
        ...state.results.map((result) => [result.ticker, result.company || "", result.sector || "", result.scores.global ?? "", result.scores.fundamental ?? "", result.scores.technical ?? "", result.price ?? "", result.market_cap ?? ""]),
      ];
      const csv = rows.map((row) => row.map(value => `"${String(value).replace(/"/g, '""')}"`).join(",")).join("\n");
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "financeanalytics-export.csv";
      link.click();
      URL.revokeObjectURL(url);
    }

    async function analyze() {
      const button = $("#analyze");
      const tickers = [...new Set(parseTickers($("#tickers").value).concat(parseTickers($("#compareTicker").value)))];
      button.disabled = true; button.textContent = "Analyse en coursâ€¦"; $("#message").innerHTML = "";
      try {
        if (!tickers.length) throw new Error("Ajoutez au moins un ticker.");
        const response = await fetch("/api/analyze", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({tickers}) });
        const data = await response.json(); if (!response.ok) throw new Error(data.error || "La requÃªte a Ã©chouÃ©.");
        $("#message").innerHTML = `<div class="success">âœ… Analyse terminÃ©e pour ${(data.results || []).length} valeur(s).</div>`;
        if (data.errors && data.errors.length) $("#message").innerHTML += data.errors.map(error => `<div class="error">${formatText(error.ticker)}: ${formatText(error.message)}</div>`).join("");
        if (data.results && data.results.length) render(data.results);
      } catch (error) { $("#message").innerHTML = `<div class="error">${formatText(error.message)}</div>`; }
      finally { button.disabled = false; button.textContent = "Lancer l'analyse  â†’"; }
    }

    $("#analyze").addEventListener("click", analyze);
    $("#exportCsv").addEventListener("click", exportCsv);
    $("#printPdf").addEventListener("click", () => window.print());
    $("#tickers").addEventListener("keydown", event => { if (event.key === "Enter") analyze(); });
    $("#compareTicker").addEventListener("keydown", event => { if (event.key === "Enter") analyze(); });
  
