const $ = (id) => document.getElementById(id);

function showResult(id, value, error = false) {
  const el = $(id);
  el.classList.remove('hidden');
  el.classList.toggle('error', error);
  el.textContent = value;
}

async function request(url, options = {}) {
  const response = await fetch(url, { headers: { 'Content-Type': 'application/json' }, ...options });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || 'Request failed.');
  return data;
}

async function askQuestion() {
  try {
    const question = $('question').value.trim();
    if (!question) return showResult('qna-result', 'Enter a question first.', true);
    const data = await request(`/api/qna?question=${encodeURIComponent(question)}`);
    showResult('qna-result', data.answer);
  } catch (e) { showResult('qna-result', e.message, true); }
}

async function explainTopic() {
  try {
    const topic = $('topic').value.trim();
    if (!topic) return showResult('explain-result', 'Enter a topic first.', true);
    const data = await request('/api/explain', { method: 'POST', body: JSON.stringify({ topic }) });
    showResult('explain-result', data.explanation);
  } catch (e) { showResult('explain-result', e.message, true); }
}

async function summarizeText() {
  try {
    const text = $('summary-text').value.trim();
    if (!text) return showResult('summary-result', 'Paste some text first.', true);
    const data = await request('/api/summarize', { method: 'POST', body: JSON.stringify({ text }) });
    showResult('summary-result', data.summary);
  } catch (e) { showResult('summary-result', e.message, true); }
}

async function generateQuiz() {
  try {
    const text = $('quiz-text').value.trim();
    if (!text) return showResult('quiz-result', 'Enter a topic or passage first.', true);
    const data = await request('/api/quiz', { method: 'POST', body: JSON.stringify({ text }) });
    const html = data.quiz.map((q, i) => `
      <div class="quiz-question">
        <strong>Q${i + 1}. ${escapeHtml(q.question)}</strong>
        ${q.options.map(o => `<label class="quiz-option"><input type="radio" disabled> ${escapeHtml(o)}</label>`).join('')}
        <small>Answer: ${escapeHtml(q.answer)}</small>
      </div>`).join('');
    const el = $('quiz-result');
    el.classList.remove('hidden', 'error');
    el.innerHTML = html;
  } catch (e) { showResult('quiz-result', e.message, true); }
}

async function getLearningPath() {
  try {
    const topic = $('learning-topic').value.trim();
    if (!topic) return showResult('learning-result', 'Enter a topic first.', true);
    const data = await request('/api/learning-path', { method: 'POST', body: JSON.stringify({ topic }) });
    showResult('learning-result', data.recommendations);
  } catch (e) { showResult('learning-result', e.message, true); }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, ch => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', "'":'&#39;', '"':'&quot;' }[ch]));
}
