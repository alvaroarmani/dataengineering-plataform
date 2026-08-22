'use client';
import { useEffect, useState } from 'react';

const KEY = 'de_diario';

export default function Diario() {
  const [entradas, setEntradas] = useState([]);
  const [f, setF] = useState({ f1: '', f2: '', f3: '', f4: '' });

  useEffect(() => { try { setEntradas(JSON.parse(localStorage.getItem(KEY) || '[]')); } catch {} }, []);
  const salvar = (arr) => { setEntradas(arr); try { localStorage.setItem(KEY, JSON.stringify(arr)); } catch {} };

  const add = (e) => {
    e.preventDefault();
    if (!f.f1 && !f.f2 && !f.f3 && !f.f4) return;
    const data = new Date().toISOString().slice(0, 10);
    salvar([{ data, ...f }, ...entradas]);
    setF({ f1: '', f2: '', f3: '', f4: '' });
  };
  const remover = (i) => salvar(entradas.filter((_, k) => k !== i));
  const copiar = () => {
    const txt = entradas.map((e) => `### ${e.data}\n- Estudei/construí: ${e.f1 || ''}\n- Ensinaria assim: ${e.f2 || ''}\n- Travei em / dúvida: ${e.f3 || ''}\n- Próximo passo: ${e.f4 || ''}`).join('\n\n');
    try { navigator.clipboard.writeText(txt); } catch { alert(txt); }
  };

  const ta = (id, label, rows = 2) => (
    <div>
      <label className="lbl" htmlFor={id}>{label}</label>
      <textarea id={id} rows={rows} value={f[id]} onChange={(e) => setF({ ...f, [id]: e.target.value })}
        style={{ width: '100%', marginTop: 6, padding: '10px 12px', border: '1px solid var(--border)', borderRadius: 10, background: 'var(--bg)', color: 'var(--ink)', fontFamily: 'var(--man)', fontSize: 15, resize: 'vertical' }} />
    </div>
  );

  return (
    <main className="wrap" style={{ paddingTop: 32, paddingBottom: 48, maxWidth: 820 }}>
      <h1 style={{ fontSize: 28 }}>Diário de aprendizado</h1>
      <p className="muted" style={{ fontSize: 16, margin: '8px 0 0' }}>Metacognição faz parte do método. Escreva 3 linhas por sessão — ajuda a reter e vira matéria-prima para entrevistas.</p>

      <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', background: 'var(--gold-bg)', border: '1px solid var(--border)', borderRadius: 12, padding: '14px 16px', margin: '18px 0' }}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" strokeWidth="2" style={{ flexShrink: 0, marginTop: 2 }}><circle cx="12" cy="12" r="9" /><path d="M12 8v5M12 16h.01" /></svg>
        <p style={{ margin: 0, fontSize: 13.5 }}>As anotações ficam salvas <strong>no seu navegador</strong>. Para versionar (build-in-public), use <strong>Copiar tudo</strong> e cole no <code>diario.md</code> do repositório.</p>
      </div>

      <form className="card" onSubmit={add} style={{ padding: 20, display: 'flex', flexDirection: 'column', gap: 14 }}>
        {ta('f1', 'O que estudei / construí hoje?')}
        {ta('f2', 'O que eu ensinaria disso? (teste de Feynman)')}
        <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: 14 }}>
          {ta('f3', 'Onde travei / dúvida')}
          {ta('f4', 'Próximo passo')}
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          <button type="submit" className="btn btn-p">Salvar entrada</button>
          <button type="button" className="btn btn-s" onClick={copiar}>Copiar tudo</button>
        </div>
      </form>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', margin: '28px 0 10px' }}>
        <h2 style={{ fontSize: 20 }}>Entradas</h2>
        <span className="muted" style={{ fontSize: 14 }}>{entradas.length} {entradas.length === 1 ? 'entrada' : 'entradas'}</span>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        {entradas.length === 0 && <div className="muted" style={{ fontSize: 14 }}>Nenhuma entrada ainda — registre sua primeira sessão acima.</div>}
        {entradas.map((e, i) => (
          <div key={i} className="card" style={{ padding: '16px 18px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'var(--sora)', fontWeight: 600 }}>{e.data}</span>
              <button onClick={() => remover(i)} style={{ background: 'none', border: 0, color: 'var(--muted)', cursor: 'pointer', fontSize: 13 }}>remover</button>
            </div>
            <div style={{ fontSize: 14, lineHeight: 1.5 }}>
              {e.f1 && <div style={{ marginTop: 6 }}><strong>Estudei:</strong> {e.f1}</div>}
              {e.f2 && <div style={{ marginTop: 6 }}><strong>Ensinaria:</strong> {e.f2}</div>}
              {e.f3 && <div style={{ marginTop: 6 }}><strong>Travei:</strong> {e.f3}</div>}
              {e.f4 && <div style={{ marginTop: 6 }}><strong>Próximo:</strong> {e.f4}</div>}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
