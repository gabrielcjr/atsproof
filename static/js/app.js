/**
 * ATS MatchProof - Client-Side Application Logic
 * Modularized for clean maintainability and performance.
 */

document.addEventListener('DOMContentLoaded', () => {
    const CURRENT_LANG = (document.documentElement.lang || 'en').toLowerCase().startsWith('pt') ? 'pt' : 'en';
    const MAX_BYTES = 200 * 1024; // 200 KB

    const form = document.getElementById('ats-form');
    const submitBtn = document.getElementById('submit-btn');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('resume-input');
    const dropEmptyState = document.getElementById('drop-empty-state');
    const dropSelectedState = document.getElementById('drop-selected-state');
    const fileNameEl = document.getElementById('file-name');
    const fileSizeEl = document.getElementById('file-size');
    const fileErrorEl = document.getElementById('file-error');
    const removeFileBtn = document.getElementById('remove-file-btn');
    const jdTextarea = document.getElementById('job_description');
    const charCounter = document.getElementById('char-counter');
    const clearJdBtn = document.getElementById('clear-jd-btn');
    const loadingEl = document.getElementById('loading');
    const resultsContainer = document.getElementById('results');

    // =========================================================================
    // 1. File Upload & Drag-and-Drop Management
    // =========================================================================

    function showFileError(msg) {
        if (fileErrorEl) {
            fileErrorEl.textContent = msg;
            fileErrorEl.classList.remove('hidden');
        }
    }

    function hideFileError() {
        if (fileErrorEl) {
            fileErrorEl.classList.add('hidden');
        }
    }

    function handleSelectedFile(file) {
        if (!file) return;

        // Verify PDF MIME type or extension
        if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
            showFileError(CURRENT_LANG === 'pt' 
                ? 'Por favor, selecione um arquivo PDF válido.' 
                : 'Please select a valid PDF file.'
            );
            if (fileInput) fileInput.value = '';
            return;
        }

        // Verify 200 KB maximum size limit
        if (file.size > MAX_BYTES) {
            showFileError(CURRENT_LANG === 'pt' 
                ? `Tamanho do arquivo (${(file.size / 1024).toFixed(1)} KB) excede o limite máximo de 200 KB.` 
                : `File size (${(file.size / 1024).toFixed(1)} KB) exceeds the maximum limit of 200 KB.`
            );
            if (fileInput) fileInput.value = '';
            return;
        }

        hideFileError();
        if (dropEmptyState) dropEmptyState.classList.add('hidden');
        if (dropSelectedState) {
            dropSelectedState.classList.remove('hidden');
            dropSelectedState.classList.add('flex');
        }
        if (fileNameEl) fileNameEl.textContent = file.name;
        if (fileSizeEl) fileSizeEl.textContent = (file.size / 1024).toFixed(1) + ' KB';
    }

    if (fileInput) {
        fileInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                handleSelectedFile(this.files[0]);
            }
        });
    }

    if (dropZone) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add('border-indigo-500', 'bg-slate-900/80');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove('border-indigo-500', 'bg-slate-900/80');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt ? dt.files : null;
            if (files && files.length > 0) {
                if (fileInput) fileInput.files = files;
                handleSelectedFile(files[0]);
            }
        });
    }

    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            if (fileInput) fileInput.value = '';
            if (dropSelectedState) {
                dropSelectedState.classList.add('hidden');
                dropSelectedState.classList.remove('flex');
            }
            if (dropEmptyState) dropEmptyState.classList.remove('hidden');
            hideFileError();
        });
    }

    // =========================================================================
    // 2. Job Description Character Counter & Clear Action
    // =========================================================================

    if (jdTextarea && charCounter) {
        const maxLimit = (jdTextarea.maxLength && jdTextarea.maxLength > 0) ? jdTextarea.maxLength : 7000;
        jdTextarea.addEventListener('input', function () {
            const label = CURRENT_LANG === 'pt' ? 'carac.' : 'chars';
            charCounter.textContent = `${this.value.length} / ${maxLimit} ${label}`;
        });
    }

    if (clearJdBtn && jdTextarea && charCounter) {
        const maxLimit = (jdTextarea.maxLength && jdTextarea.maxLength > 0) ? jdTextarea.maxLength : 7000;
        clearJdBtn.addEventListener('click', function () {
            jdTextarea.value = '';
            const label = CURRENT_LANG === 'pt' ? 'carac.' : 'chars';
            charCounter.textContent = `0 / ${maxLimit} ${label}`;
        });
    }

    // =========================================================================
    // 3. Direct Async Submission Handler
    // =========================================================================

    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            hideFileError();

            if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
                showFileError(CURRENT_LANG === 'pt' 
                    ? 'Por favor, selecione ou arraste um currículo em PDF primeiro.' 
                    : 'Please select or drop a PDF resume file first.'
                );
                if (dropZone) dropZone.scrollIntoView({ behavior: 'smooth', block: 'center' });
                return;
            }

            const jdVal = (jdTextarea ? jdTextarea.value : '').trim();
            if (!jdVal) {
                alert(CURRENT_LANG === 'pt' 
                    ? 'Por favor, cole a descrição da vaga antes de rodar a análise.' 
                    : 'Please paste the Job Description before running the ATS analysis.'
                );
                if (jdTextarea) jdTextarea.focus();
                return;
            }

            // Visual loading state
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('opacity-70', 'cursor-wait');
            }

            if (loadingEl) {
                loadingEl.style.display = 'flex';
                loadingEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            if (resultsContainer) {
                resultsContainer.innerHTML = '';
            }

            try {
                const formData = new FormData(form);
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'HX-Request': 'true'
                    }
                });

                const htmlContent = await response.text();
                if (resultsContainer) {
                    resultsContainer.innerHTML = htmlContent;
                    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            } catch (err) {
                if (resultsContainer) {
                    resultsContainer.innerHTML = `
                        <div class="rounded-2xl bg-rose-950/40 border border-rose-500/30 p-6 backdrop-blur-md shadow-2xl">
                            <h3 class="text-lg font-bold text-rose-200">${CURRENT_LANG === 'pt' ? 'Falha na Requisição' : 'Request Failed'}</h3>
                            <p class="text-sm text-rose-300 mt-2">${err.message || 'Connection failed'}.</p>
                        </div>
                    `;
                    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            } finally {
                if (loadingEl) {
                    loadingEl.style.display = 'none';
                }
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('opacity-70', 'cursor-wait');
                }
            }
        });
    }
});

// =============================================================================
// 4. Global Utility Functions (Export Report & Copy Bullets)
// =============================================================================

/**
 * Copies an individual optimized bullet point to the clipboard.
 */
function copyBulletText(btn) {
    const isPt = (document.documentElement.lang || 'en').toLowerCase().startsWith('pt');
    const container = btn.closest('div');
    const textEl = container ? container.querySelector('.bullet-text') : null;
    if (textEl) {
        navigator.clipboard.writeText(textEl.textContent.trim()).then(() => {
            const orig = btn.textContent;
            btn.textContent = isPt ? 'Copiado!' : 'Copied!';
            setTimeout(() => { btn.textContent = orig; }, 2000);
        });
    }
}

/**
 * Formats and exports the complete analysis report (Clipboard or TXT Download).
 */
function exportFullReport(btn, mode) {
    const dataEl = document.getElementById('ats-report-data');
    if (!dataEl) return;

    let data;
    try {
        data = JSON.parse(dataEl.textContent);
    } catch (e) {
        console.error('Failed to parse report data', e);
        return;
    }

    const isPt = (document.documentElement.lang || 'en').toLowerCase().startsWith('pt');
    const score = data.match_score || 0;
    const verdict = data.summary_verdict || '';
    const expGap = data.experience_gap_feedback || '';
    const matchedKw = data.matched_keywords || [];
    const missingKw = data.missing_critical_keywords || [];
    const suggestions = data.tailoring_suggestions || [];
    const provider = data.provider || 'ATS MatchProof AI Engine';

    let report = "";
    if (isPt) {
        report += "================================================================================\n";
        report += "RELATÓRIO DE COMPATIBILIDADE ATS - ATS MATCHPROOF\n";
        report += `Data: ${new Date().toLocaleDateString('pt-BR')} ${new Date().toLocaleTimeString('pt-BR')}\n`;
        report += "URL: https://atsproof.website\n";
        report += `Motor de Verificação: ${provider}\n`;
        report += "================================================================================\n\n";
        report += `SCORE DE COMPATIBILIDADE ATS: ${score}%\n\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += "1. VEREDITO ESTRATÉGICO DE RECRUTAMENTO\n";
        report += "--------------------------------------------------------------------------------\n";
        report += `${verdict}\n\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += "2. AVALIAÇÃO DE EXPERIÊNCIA E SENIORIDADE\n";
        report += "--------------------------------------------------------------------------------\n";
        report += `${expGap}\n\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += `3. PALAVRAS-CHAVE ENCONTRADAS (${matchedKw.length})\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += matchedKw.length ? matchedKw.join(', ') + '\n\n' : 'Nenhuma detectada.\n\n';
        report += "--------------------------------------------------------------------------------\n";
        report += `4. PALAVRAS-CHAVE CRÍTICAS AUSENTES (${missingKw.length})\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += missingKw.length ? missingKw.join(', ') + '\n\n' : 'Nenhuma ausente.\n\n';
        report += "--------------------------------------------------------------------------------\n";
        report += "5. OTIMIZAÇÃO DE EXPERIÊNCIAS (GOOGLE XYZ / SUBSTANTIVO DE AÇÃO)\n";
        report += "--------------------------------------------------------------------------------\n";
        suggestions.forEach((item, idx) => {
            report += `\n[Item ${idx + 1}]\n`;
            report += `Original: "${item.original_bullet}"\n`;
            report += `Otimizado (ATS): "${item.suggested_optimized_bullet}"\n`;
        });
        report += "\n================================================================================\n";
        report += "Gerado gratuitamente por ATS MatchProof (https://atsproof.website)\n";
        report += "Processamento 100% privado em memória. Currículos nunca salvos.\n";
        report += "================================================================================\n";
    } else {
        report += "================================================================================\n";
        report += "ATS MATCH VERIFICATION REPORT - ATS MATCHPROOF\n";
        report += `Date: ${new Date().toLocaleDateString('en-US')} ${new Date().toLocaleTimeString('en-US')}\n`;
        report += "URL: https://atsproof.website\n";
        report += `Verification Engine: ${provider}\n`;
        report += "================================================================================\n\n";
        report += `ATS MATCH SCORE: ${score}%\n\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += "1. STRATEGIC RECRUITER VERDICT\n";
        report += "--------------------------------------------------------------------------------\n";
        report += `${verdict}\n\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += "2. EXPERIENCE & SENIORITY ASSESSMENT\n";
        report += "--------------------------------------------------------------------------------\n";
        report += `${expGap}\n\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += `3. MATCHED KEYWORDS (${matchedKw.length})\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += matchedKw.length ? matchedKw.join(', ') + '\n\n' : 'None detected.\n\n';
        report += "--------------------------------------------------------------------------------\n";
        report += `4. MISSING CRITICAL KEYWORDS (${missingKw.length})\n`;
        report += "--------------------------------------------------------------------------------\n";
        report += missingKw.length ? missingKw.join(', ') + '\n\n' : 'None missing.\n\n';
        report += "--------------------------------------------------------------------------------\n";
        report += "5. HIGH-IMPACT BULLET POINT TAILORING (GOOGLE XYZ FORMULA)\n";
        report += "--------------------------------------------------------------------------------\n";
        suggestions.forEach((item, idx) => {
            report += `\n[Item ${idx + 1}]\n`;
            report += `Original: "${item.original_bullet}"\n`;
            report += `Optimized (ATS): "${item.suggested_optimized_bullet}"\n`;
        });
        report += "\n================================================================================\n";
        report += "Generated free at ATS MatchProof (https://atsproof.website)\n";
        report += "100% Privacy-first in-memory analysis. Resumes never stored.\n";
        report += "================================================================================\n";
    }

    if (mode === 'copy') {
        navigator.clipboard.writeText(report).then(() => {
            const labelSpan = btn.querySelector('.btn-label') || btn;
            const origText = labelSpan.textContent;
            labelSpan.textContent = isPt ? 'Relatório Copiado!' : 'Report Copied!';
            btn.classList.add('bg-emerald-600/30', 'text-emerald-300', 'border-emerald-500/50');
            setTimeout(() => {
                labelSpan.textContent = origText;
                btn.classList.remove('bg-emerald-600/30', 'text-emerald-300', 'border-emerald-500/50');
            }, 2500);
        });
    } else if (mode === 'download') {
        const blob = new Blob([report], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = isPt ? `Relatorio_ATS_Match_${score}pct.txt` : `ATS_Match_Report_${score}pct.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}
