// Converte a sintaxe MyST usada no curso para o que o Astro (remark-directive) entende.
// - ```{mermaid} ... ```            -> <pre class="mermaid">…</pre>
// - :::{admonition} T / :class: C   -> :::admon[T]{.C}
// - :::{dropdown} T                 -> :::dropdown[T]
// - links relativos p/ .md/.ipynb   -> vira texto puro (evita 404 no shell atual)
// Mantém o resto intacto.

function escHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function neutralizarLinks(linha) {
  return linha.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (m, texto, alvo) => {
    if (/^https?:/i.test(alvo) || alvo.startsWith('#')) return m; // externos e âncoras ok
    return texto; // relativos a arquivos do curso: só o texto
  });
}

export function preprocessMyst(md) {
  const linhas = md.split(/\r?\n/);
  const out = [];
  let i = 0;
  while (i < linhas.length) {
    const linha = linhas[i];

    // Bloco mermaid
    const mMermaid = linha.match(/^```\{mermaid\}\s*$/);
    if (mMermaid) {
      const buf = [];
      i++;
      while (i < linhas.length && !/^```\s*$/.test(linhas[i])) { buf.push(linhas[i]); i++; }
      i++; // pula o ``` de fechamento
      out.push('<pre class="mermaid">' + escHtml(buf.join('\n')) + '</pre>');
      continue;
    }

    // Outros blocos de código: passa direto sem tocar
    const mCode = linha.match(/^```/);
    if (mCode) {
      out.push(linha); i++;
      while (i < linhas.length && !/^```\s*$/.test(linhas[i])) { out.push(linhas[i]); i++; }
      if (i < linhas.length) { out.push(linhas[i]); i++; }
      continue;
    }

    // Admonition (tolera indentação, p.ex. dentro de listas)
    const mAdmon = linha.match(/^(\s*):::\{admonition\}\s*(.*)$/);
    if (mAdmon) {
      const indent = mAdmon[1];
      const titulo = mAdmon[2].trim();
      let cls = 'note';
      if (i + 1 < linhas.length) {
        const mCls = linhas[i + 1].match(/^\s*:class:\s*(\S+)/);
        if (mCls) { cls = mCls[1]; i++; }
      }
      out.push(`${indent}:::admon[${titulo}]{.${cls}}`);
      i++;
      continue;
    }

    // Dropdown (tolera indentação)
    const mDrop = linha.match(/^(\s*):::\{dropdown\}\s*(.*)$/);
    if (mDrop) {
      out.push(`${mDrop[1]}:::dropdown[${mDrop[2].trim()}]`);
      i++;
      continue;
    }

    out.push(neutralizarLinks(linha));
    i++;
  }
  return out.join('\n');
}
