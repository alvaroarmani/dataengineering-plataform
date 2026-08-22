/*
 * Camada de engajamento da plataforma (sem backend).
 * - streak diário (localStorage)
 * - mapa vivo do curso, badges, North Star, "revisar hoje", modo 5-min, desafio da semana
 * Estrutura do curso espelha progresso.json (mantenha os dois em sincronia).
 * O estado de conclusão vive no localStorage; edite progresso.json para versionar (build-in-public).
 */
(function () {
  "use strict";

  var LS = {
    streak: "de_streak",
    lastVisit: "de_last_visit",
    best: "de_streak_best",
    done: "de_modulos_concluidos", // JSON array de ids
  };

  var CURSO = [
    { eixo: 1, nome: "Fundamentos", modulos: [
      ["M01", "Fundamentos de Eng. de Dados"], ["M02", "Linux, Git e Ambiente"],
      ["M03", "Python para Eng. de Dados"], ["M04", "SQL e Bancos Relacionais"] ] },
    { eixo: 2, nome: "Data Warehousing e Modelagem", modulos: [
      ["M05", "Modelagem Dimensional"], ["M06", "Data Warehousing + BigQuery"],
      ["M07", "Transformação com dbt"] ] },
    { eixo: 3, nome: "Pipelines e Orquestração", modulos: [
      ["M08", "Ingestão e Integração"], ["M09", "Orquestração com Airflow"],
      ["M10", "Docker avançado"] ] },
    { eixo: 4, nome: "Escala, Qualidade e Governança", modulos: [
      ["M11", "Spark + Lakehouse"], ["M12", "Qualidade e Observabilidade"],
      ["M13", "DataOps, CI/CD e IaC"], ["M14", "Governança e LGPD"] ] },
    { eixo: 5, nome: "Carreira e Integração", modulos: [
      ["M15", "Carreira e Entrevistas"], ["TCC", "TCC — Data Warehouse"] ] },
  ];

  var DESAFIOS = [
    "SQL: escreva uma query com window function que traga o top-3 por categoria.",
    "Python: implemente um leitor de CSV que valide tipos e reporte linhas inválidas.",
    "DuckDB: agregue um Parquet de >1M linhas e meça o tempo.",
    "Modelagem: desenhe um star schema para um e-commerce (fato vendas + 3 dimensões).",
    "Docker: escreva um docker-compose com Postgres + um serviço que o consome.",
    "dbt: crie um modelo com testes not_null e unique e gere a doc.",
    "Airflow: escreva uma DAG idempotente que reprocessa um dia sem duplicar dados.",
  ];

  function hoje() { return new Date().toISOString().slice(0, 10); }
  function ler(k, def) { try { var v = localStorage.getItem(k); return v === null ? def : v; } catch (e) { return def; } }
  function gravar(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function getDone() { try { return JSON.parse(ler(LS.done, "[]")); } catch (e) { return []; } }
  function setDone(a) { gravar(LS.done, JSON.stringify(a)); }

  // --- Streak: incrementa 1x/dia; zera se pular mais de 1 dia ---
  function pingStreak() {
    var last = ler(LS.lastVisit, "");
    var d = hoje();
    if (last === d) return; // já contou hoje
    var streak = parseInt(ler(LS.streak, "0"), 10) || 0;
    if (last) {
      var diff = Math.round((new Date(d) - new Date(last)) / 86400000);
      streak = diff === 1 ? streak + 1 : 1;
    } else {
      streak = 1;
    }
    gravar(LS.streak, String(streak));
    gravar(LS.lastVisit, d);
    var best = parseInt(ler(LS.best, "0"), 10) || 0;
    if (streak > best) gravar(LS.best, String(streak));
  }

  function totalModulos() { return CURSO.reduce(function (n, e) { return n + e.modulos.length; }, 0); }

  function badges(done, streak) {
    var b = [];
    if (done.length >= 1) b.push("🥇 Primeiro módulo");
    if (done.length >= 4) b.push("🧱 Eixo 1 completo");
    if (done.length >= totalModulos()) b.push("🎓 Curso completo");
    if (streak >= 7) b.push("🔥 7 dias seguidos");
    if (streak >= 30) b.push("🚀 30 dias seguidos");
    if (done.indexOf("TCC") >= 0) b.push("🏆 TCC entregue");
    return b.length ? b : ["— conclua um módulo para ganhar seu primeiro badge"];
  }

  function render() {
    var host = document.getElementById("mapa-curso");
    if (!host) return; // só renderiza no dashboard

    var done = getDone();
    var streak = parseInt(ler(LS.streak, "0"), 10) || 0;
    var best = parseInt(ler(LS.best, "0"), 10) || 0;
    var total = totalModulos();
    var pct = Math.round((done.length / total) * 100);
    var faltamTCC = total - done.length;
    var desafio = DESAFIOS[(new Date().getWeek ? new Date().getWeek() : Math.floor(Date.now() / 6048e5)) % DESAFIOS.length];

    var h = "";
    h += '<div class="de-cards">';
    h += card("🔥 Streak", streak + " dia(s)", "recorde: " + best);
    h += card("📈 Progresso", pct + "%", done.length + "/" + total + " módulos");
    h += card("🎯 North Star", faltamTCC + " p/ o TCC", "faltam para você estar pronto");
    h += "</div>";

    // Barra de progresso geral
    h += '<div class="de-barra"><span style="width:' + pct + '%"></span></div>';

    // Mapa por eixo
    h += '<div class="de-mapa">';
    CURSO.forEach(function (e) {
      h += '<div class="de-eixo"><h4>Eixo ' + e.eixo + " — " + e.nome + "</h4><div class='de-mods'>";
      e.modulos.forEach(function (m) {
        var on = done.indexOf(m[0]) >= 0;
        h += '<button class="de-mod ' + (on ? "on" : "") + '" data-id="' + m[0] + '" title="' + m[1] + '">' +
             (on ? "✅ " : "⬜ ") + m[0] + "</button>";
      });
      h += "</div></div>";
    });
    h += "</div>";

    h += '<p class="de-hint">Clique num módulo para marcar/desmarcar como concluído (salvo no seu navegador).</p>';

    // Badges
    h += "<h4>Conquistas</h4><div class='de-badges'>";
    badges(done, streak).forEach(function (t) { h += '<span class="de-badge">' + t + "</span>"; });
    h += "</div>";

    // Revisar hoje + 5-min + desafio
    h += "<h4>Revisar hoje (revisão espaçada)</h4>";
    h += done.length ? "<p>Revise os flashcards dos módulos concluídos: <strong>" + done.join(", ") + "</strong>.</p>"
                     : "<p>Sem módulos concluídos ainda — comece pelo M01.</p>";
    h += '<p><strong>Modo 5-min hoje:</strong> abra os flashcards de um módulo concluído e faça 5 cards. Mantém o streak sem esforço.</p>';
    h += "<h4>Desafio da semana</h4><p>" + desafio + "</p>";

    host.innerHTML = h;

    // handlers
    Array.prototype.forEach.call(host.querySelectorAll(".de-mod"), function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-id");
        var d = getDone();
        var i = d.indexOf(id);
        if (i >= 0) d.splice(i, 1); else d.push(id);
        setDone(d);
        render();
      });
    });
  }

  function card(titulo, valor, sub) {
    return '<div class="de-card"><div class="de-card-t">' + titulo + '</div><div class="de-card-v">' +
      valor + '</div><div class="de-card-s">' + sub + "</div></div>";
  }

  // Semana do ano (para o desafio)
  Date.prototype.getWeek = function () {
    var d = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate()));
    var dayNum = (d.getUTCDay() + 6) % 7;
    d.setUTCDate(d.getUTCDate() - dayNum + 3);
    var firstThursday = d.getTime();
    d.setUTCMonth(0, 1);
    if (d.getUTCDay() !== 4) d.setUTCMonth(0, 1 + ((4 - d.getUTCDay()) + 7) % 7);
    return 1 + Math.ceil((firstThursday - d) / 6048e5);
  };

  function init() {
    pingStreak();
    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
