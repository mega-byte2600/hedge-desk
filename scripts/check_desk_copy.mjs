// Checks what internal naming, if any, survives in the SERVED desk page.
import { renderSouls } from '/Users/astra/workspace/projects/hedge-desk/web/multi-agent-desk.mjs';

const html = renderSouls(undefined);
const text = html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');

const internal = ['model families', 'soul', 'deepseek', 'glm', 'gpt', 'claude', 'gemini',
                  'qwen', 'anthropic', 'openai', 'z-ai', 'free agents', 'fixed matrix'];

const visibleLeaks = internal.filter((b) => text.toLowerCase().includes(b.toLowerCase()));
const markupLeaks = internal.filter((b) => html.toLowerCase().includes(b.toLowerCase()));

console.log('VISIBLE-TEXT leaks :', visibleLeaks.length ? visibleLeaks : 'NONE');
console.log('ANY-MARKUP leaks   :', markupLeaks.length ? markupLeaks : 'NONE');
console.log('');
console.log('--- visible copy, first 420 chars ---');
console.log(text.slice(0, 420));
