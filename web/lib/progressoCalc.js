// Cálculos de progresso a partir de um Set de aula_ids concluídos e do curso.json.
// aula_id = `${modulo.pasta}/${unidade.base}`.

export function idAula(pasta, base) { return `${pasta}/${base}`; }

export function unidadesDoModulo(mod) {
  return mod.unidades.map((u) => idAula(mod.pasta, u.base));
}

export function concluidasNoModulo(concluidas, mod) {
  return unidadesDoModulo(mod).filter((id) => concluidas.has(id)).length;
}

export function pctModulo(concluidas, mod) {
  const total = mod.unidades.length || 1;
  return Math.round((concluidasNoModulo(concluidas, mod) / total) * 100);
}

export function pctEixo(concluidas, eixo) {
  let total = 0, feitas = 0;
  for (const m of eixo.modulos) { total += m.unidades.length; feitas += concluidasNoModulo(concluidas, m); }
  return total ? Math.round((feitas / total) * 100) : 0;
}

export function totais(curso) {
  let total = 0;
  for (const e of curso.eixos) for (const m of e.modulos) total += m.unidades.length;
  return total;
}

export function pctTotal(concluidas, curso) {
  const total = totais(curso) || 1;
  return Math.round((concluidas.size / total) * 100);
}

// Primeira unidade ainda não concluída (para "continuar de onde parei").
export function proximaAula(curso, concluidas) {
  for (const e of curso.eixos)
    for (const m of e.modulos)
      for (const u of m.unidades) {
        const id = idAula(m.pasta, u.base);
        if (!concluidas.has(id)) return { pasta: m.pasta, base: u.base, mod: m, unidade: u, eixo: e };
      }
  return null;
}
