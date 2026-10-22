'use client';
import Link from 'next/link';
import curso from '../src/data/curso.json';
import { usePlataforma } from './Plataforma.jsx';
import { pctEixo } from '../lib/progressoCalc.js';

// A trilha desenhada como um pipeline: cada eixo é uma estação e o duto enche com o progresso real.
export default function TrilhaPipeline() {
  const { concluidas = new Set() } = usePlataforma() || {};
  return (
    <ol className="pipe">
      {curso.eixos.map((e) => {
        const p = pctEixo(concluidas, e);
        const estado = p === 100 ? 'done' : p > 0 ? 'on' : '';
        return (
          <li key={e.id} className={`pipe-st ${estado}`} style={{ '--p': p / 100 }}>
            <Link href={`/trilha#eixo-${e.id}`} className="pipe-link">
              <span className="pipe-dot" aria-hidden="true">{e.id}</span>
              <span className="pipe-nome">{e.nome}</span>
              <span className="pipe-meta">{e.modulos.length} disciplinas, {p}% feito</span>
            </Link>
          </li>
        );
      })}
    </ol>
  );
}
