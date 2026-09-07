async function fetchJson(path) {
  const response = await fetch(path, { cache: 'no-store' });
  if (!response.ok) throw new Error(`${path} returned ${response.status}`);
  return response.json();
}

function card(title, body, badge) {
  const el = document.createElement('article');
  el.className = 'card';
  el.innerHTML = `${badge ? `<span class="badge">${badge}</span>` : ''}<h3>${title}</h3><p>${body}</p>`;
  return el;
}

function fillList(id, items, ordered = false) {
  const target = document.getElementById(id);
  target.innerHTML = '';
  for (const item of items) {
    const li = document.createElement('li');
    li.textContent = item;
    target.appendChild(li);
  }
}

async function boot() {
  const renderStatus = document.getElementById('render-status');
  const supabaseStatus = document.getElementById('supabase-status');
  try {
    const data = await fetchJson('/api/ape');
    renderStatus.textContent = 'live';

    document.title = data.project.title;
    fillList('deployment', data.deployment_steps, true);
    fillList('outputs', data.playbook_outputs);

    const competencies = document.getElementById('competency-cards');
    competencies.innerHTML = '';
    for (const item of data.competencies) {
      competencies.appendChild(card(item.label, item.demo_proof, 'APE Agreement'));
    }

    const evidence = document.getElementById('evidence-cards');
    evidence.innerHTML = '';
    for (const item of data.evidence) {
      evidence.appendChild(card(item.source, `${item.claim} Leadership use: ${item.leadership_use}`, 'Evidence'));
    }

    const refs = document.getElementById('references');
    refs.innerHTML = '';
    for (const ref of data.references) {
      const li = document.createElement('li');
      li.textContent = ref;
      refs.appendChild(li);
    }

    try {
      const edge = await fetchJson(data.project.supabase_edge_url);
      supabaseStatus.textContent = edge.status === 'ok' ? 'live' : 'reachable';
    } catch (error) {
      supabaseStatus.textContent = 'schema loaded';
    }
  } catch (error) {
    renderStatus.textContent = 'needs redeploy';
    supabaseStatus.textContent = 'schema loaded';
    console.error(error);
  }
}

boot();
