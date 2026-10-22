'use client';
import { useEffect } from 'react';

const ehEscuro = () => {
  const t = document.documentElement.getAttribute('data-theme');
  return t === 'dark' || (!t && window.matchMedia('(prefers-color-scheme: dark)').matches);
};

// Renderiza no cliente os blocos <pre class="mermaid"> vindos do HTML compilado,
// e re-renderiza quando o tema muda (o SVG gerado fixa as cores do tema).
export default function Mermaid() {
  useEffect(() => {
    const nodes = [...document.querySelectorAll('pre.mermaid')];
    if (!nodes.length) return;
    // Guarda a fonte do diagrama: o mermaid troca o texto pelo SVG.
    nodes.forEach((n) => { if (!n.dataset.fonte) n.dataset.fonte = n.textContent; });
    let cancelado = false;

    const render = async () => {
      const mermaid = (await import('mermaid')).default;
      if (cancelado) return;
      mermaid.initialize({ startOnLoad: false, theme: ehEscuro() ? 'dark' : 'default', securityLevel: 'loose', fontFamily: 'Manrope, system-ui, sans-serif' });
      nodes.forEach((n) => { n.removeAttribute('data-processed'); n.textContent = n.dataset.fonte; });
      try { await mermaid.run({ nodes }); } catch (e) { /* diagrama inválido: ignora */ }
    };

    render();
    const obs = new MutationObserver(render);
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => { cancelado = true; obs.disconnect(); };
  }, []);
  return null;
}
