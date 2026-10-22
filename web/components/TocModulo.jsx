'use client';
import Link from 'next/link';
import { usePlataforma } from './Plataforma.jsx';

const ROTULO = { teoria: 'Teoria', lab: 'Lab no navegador', exercicio: 'Exercício', flashcards: 'Flashcards', recursos: 'Recursos' };

// Unidades do módulo como estações de um duto: cada unidade concluída enche o trecho até a próxima.
export default function TocModulo({ pasta, unidades }) {
  const plat = usePlataforma() || {};
  const feita = (base) => (plat.estaConcluida ? plat.estaConcluida(`${pasta}/${base}`) : false);
  const nFeitas = unidades.filter((u) => feita(u.base)).length;
  const proxima = unidades.find((u) => !feita(u.base));
  const cta = !nFeitas
    ? { href: unidades[0] && `/aula/${pasta}/${unidades[0].base}`, txt: 'Começar o módulo' }
    : proxima
      ? { href: `/aula/${pasta}/${proxima.base}`, txt: 'Continuar de onde parei' }
      : { href: unidades[0] && `/aula/${pasta}/${unidades[0].base}`, txt: 'Revisar o módulo' };

  return (
    <aside className="side-toc" style={{ position: 'sticky', top: 90 }}>
      <div style={{ padding: '0 4px 14px' }}>
        <h2 style={{ fontSize: 16 }}>Conteúdo do módulo</h2>
        <p className="muted" style={{ fontSize: 13.5, margin: '4px 0 14px' }}>
          {nFeitas} de {unidades.length} unidades concluídas{proxima && nFeitas ? `. A próxima é ${proxima.titulo}.` : '.'}
        </p>
        {cta.href && <Link className="btn btn-p" href={cta.href} style={{ width: '100%', justifyContent: 'center' }}>{cta.txt}</Link>}
      </div>
      <ol className="duto" style={{ borderTop: '1px solid var(--border)', paddingTop: 8 }}>
        {unidades.map((u) => {
          const ok = feita(u.base);
          return (
            <li key={u.base} className={`duto-st ${ok ? 'feito' : ''}`} style={{ '--p': ok ? 1 : 0 }}>
              <Link href={`/aula/${pasta}/${u.base}`} className="duto-link" style={{ padding: '9px 10px 9px 44px' }}>
                <span className="duto-no" aria-hidden="true" style={{ top: 14 }} />
                <span className="duto-corpo">
                  <span className="duto-titulo" style={{ fontSize: 14, fontFamily: 'var(--man)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{u.titulo}</span>
                  <span className="duto-meta" style={{ fontSize: 12.5 }}>{ROTULO[u.tipo] || u.tipo}{ok ? ', concluída' : ''}</span>
                </span>
              </Link>
            </li>
          );
        })}
      </ol>
    </aside>
  );
}
