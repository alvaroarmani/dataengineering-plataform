'use client';
import Link from 'next/link';
import { usePlataforma } from './Plataforma.jsx';

// Módulos de um eixo como estações de um duto; o trecho de cada um enche com as unidades concluídas.
// Recebe só a estrutura (pasta, id, nome, ch, bases das unidades) — não o HTML das aulas.
export default function DutoModulos({ modulos }) {
  const { concluidas = new Set() } = usePlataforma() || {};
  return (
    <ol className="duto">
      {modulos.map((m) => {
        const total = m.bases.length;
        const feitas = m.bases.filter((b) => concluidas.has(`${m.pasta}/${b}`)).length;
        const p = total ? feitas / total : 0;
        const estado = total && feitas === total ? 'feito' : feitas ? 'on' : '';
        return (
          <li key={m.pasta} className={`duto-st ${estado}`} style={{ '--p': p }}>
            <Link href={`/modulo/${m.pasta}`} className="duto-link">
              <span className="duto-no" aria-hidden="true" />
              <span className="duto-corpo">
                <span className="duto-titulo"><span className="codigo">{m.id}</span> {m.nome}</span>
                <span className="duto-meta">{m.ch} horas, {total} unidades</span>
              </span>
              <span className="duto-fim">
                {!m.disponivel ? 'Em breve' : estado === 'feito' ? 'Concluído' : `${Math.round(p * 100)}%`}
              </span>
            </Link>
          </li>
        );
      })}
    </ol>
  );
}
