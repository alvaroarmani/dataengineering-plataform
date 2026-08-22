// Plugin remark: transforma diretivas de container do curso em HTML estilizado.
//   :::admon[Título]{.seealso}  -> <div class="admon admon-seealso"><p class="admon-title">…</p>…</div>
//   :::dropdown[Título]         -> <details class="dropdown"><summary>…</summary>…</details>
import { visit } from 'unist-util-visit';

function pegarLabelETexto(node) {
  // remark-directive coloca o [rótulo] como primeiro filho com data.directiveLabel
  const idx = node.children.findIndex((c) => c.data && c.data.directiveLabel);
  let titulo = '';
  let resto = node.children;
  if (idx !== -1) {
    const label = node.children[idx];
    titulo = (label.children || []).map((c) => c.value || '').join('');
    resto = node.children.filter((_, k) => k !== idx);
  }
  return { titulo, resto };
}

export function remarkCurso() {
  return (tree) => {
    visit(tree, (node) => {
      if (node.type !== 'containerDirective') return;

      if (node.name === 'admon') {
        const { titulo, resto } = pegarLabelETexto(node);
        const cls = (node.attributes && node.attributes.class) || 'note';
        node.data = node.data || {};
        node.data.hName = 'div';
        node.data.hProperties = { className: ['admon', 'admon-' + cls] };
        const tituloNode = {
          type: 'paragraph',
          data: { hName: 'p', hProperties: { className: ['admon-title'] } },
          children: [{ type: 'text', value: titulo }],
        };
        node.children = [tituloNode, ...resto];
        return;
      }

      if (node.name === 'dropdown') {
        const { titulo, resto } = pegarLabelETexto(node);
        node.data = node.data || {};
        node.data.hName = 'details';
        node.data.hProperties = { className: ['dropdown'] };
        const summaryNode = {
          type: 'paragraph',
          data: { hName: 'summary' },
          children: [{ type: 'text', value: titulo }],
        };
        node.children = [summaryNode, ...resto];
        return;
      }
    });
  };
}
