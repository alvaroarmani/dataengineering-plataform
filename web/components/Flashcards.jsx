'use client';
import { useState } from 'react';

export default function Flashcards({ cards = [] }) {
  const [i, setI] = useState(0);
  const [flip, setFlip] = useState(false);
  if (!cards.length) return null;

  const virar = () => setFlip((f) => !f);
  const ir = (d) => { setI((x) => (x + d + cards.length) % cards.length); setFlip(false); };
  const card = cards[i];
  const pct = ((i + 1) / cards.length) * 100;

  return (
    <div className="fc">
      <div className="fc-top">
        <span className="fc-count">Cartão <b>{i + 1}</b> de {cards.length}</span>
        <div className="fc-bar"><span className="fc-fill" style={{ width: pct + '%' }} /></div>
      </div>

      <div
        className={'fc-card' + (flip ? ' flipped' : '')}
        role="button" tabIndex={0}
        onClick={virar}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); virar(); } }}
        aria-label="Clique para virar o cartão"
      >
        <div className="fc-inner">
          <div className="fc-face fc-front">
            <span className="fc-tag">Pergunta</span>
            <p className="fc-text">{card.p}</p>
            <span className="fc-hint">clique para revelar ↻</span>
          </div>
          <div className="fc-face fc-back">
            <span className="fc-tag fc-tag-r">Resposta</span>
            <p className="fc-text">{card.r}</p>
          </div>
        </div>
      </div>

      <div className="fc-nav">
        <button className="btn btn-s" type="button" onClick={() => ir(-1)}>← Anterior</button>
        <button className="btn btn-s" type="button" onClick={virar}>Virar ↻</button>
        <button className="btn btn-p" type="button" onClick={() => ir(1)}>Próximo →</button>
      </div>
    </div>
  );
}
