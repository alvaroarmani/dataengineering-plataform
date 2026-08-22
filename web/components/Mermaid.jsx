'use client';
import { useEffect } from 'react';

// Renderiza no cliente os blocos <pre class="mermaid"> vindos do HTML compilado.
export default function Mermaid() {
  useEffect(() => {
    const nodes = document.querySelectorAll('pre.mermaid:not([data-processed])');
    if (!nodes.length) return;
    let cancelado = false;
    (async () => {
      const mermaid = (await import('mermaid')).default;
      if (cancelado) return;
      const root = document.documentElement;
      const dark = root.getAttribute('data-theme') === 'dark' ||
        (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
      mermaid.initialize({ startOnLoad: false, theme: dark ? 'dark' : 'default', securityLevel: 'loose', fontFamily: 'Manrope, system-ui, sans-serif' });
      try { await mermaid.run({ nodes }); } catch (e) { /* diagrama inválido: ignora */ }
    })();
    return () => { cancelado = true; };
  }, []);
  return null;
}
