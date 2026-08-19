"""
Internationalization (i18n) dictionary and helper for ATS MatchProof.
Supported languages: English ('en', default) and Portuguese ('pt').
"""
from typing import Dict, Any

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "en": {
        "lang_code": "en",
        "lang_name": "English",
        "title": "Free ATS Resume & Job Matcher | Instant Match Score",
        "meta_description": "100% Free, zero-account ATS Resume & Job Matcher. Compare your resume against any job description with instant AI feedback and score.",
        "badge_free": "100% Free",
        "btn_download_template": "Download Template (.docx)",
        "badge_privacy": "100% Private • Resumes Never Stored",
        "hero_title_prefix": "Beat the ATS. Land More ",
        "hero_title_highlight": "Interviews",
        "hero_title_suffix": ".",
        "hero_subtitle": "Upload your resume PDF and paste the job description. Our dual-engine ATS simulator analyzes skill gaps, keyword matching, and crafts instant bullet point optimizations.",
        
        "upload_col_title": "1. Upload Resume (PDF)",
        "upload_col_limits": "Max {max_pdf_kb}KB • Max {max_pages} pages",
        "dropzone_prompt": "Click to upload or drag and drop",
        "dropzone_subprompt": "Standard PDF files only",
        "dropzone_change_btn": "Remove & Choose Another",
        "upload_security_notice": "Parsed securely in-memory. Never indexed or stored.",
        
        "jd_col_title": "2. Paste Job Description (JD)",
        "jd_col_counter": "{chars} / {max_chars} chars",
        "jd_placeholder": "Paste the target job requirements, qualifications, and responsibilities here...",
        "jd_tip": "Includes keywords, required experience, and tech stack.",
        "jd_clear_btn": "Clear",
        
        "btn_analyze": "Run ATS DeepScan Analysis",
        "btn_analyzing": "Simulating ATS Scanners...",
        
        "loading_step_1": "Reading and verifying text layers...",
        "loading_step_2": "Simulating ATS parser token extraction...",
        "loading_step_3": "Benchmarking skills and experience with Dual-AI...",
        "loading_step_4": "Crafting Google XYZ bullet point optimizations...",
        
        "results_title": "ATS Match Verdict & Analysis",
        "results_subtitle": "Benchmarked against target job requirements and ATS keyword filters.",
        "results_score_label": "ATS Score",
        "score_strong": "Strong Interview Match",
        "score_moderate": "Moderate Match • Needs Tailoring",
        "score_low": "Low Match • Significant Gaps",
        "verdict_title": "Strategic Recruiter Verdict",
        "experience_gap_title": "Experience & Seniority Assessment",
        "matched_keywords_title": "Matched Keywords",
        "missing_keywords_title": "Missing Critical Keywords",
        "no_matched_keywords": "No significant exact keyword matches detected.",
        "all_keywords_present": "✨ All essential keywords from the job description are present in your resume!",
        "missing_keywords_tip": "💡 Tip: Naturally incorporate these terms into your work experience bullet points if you have relevant experience.",
        "tailoring_title": "🎯 High-Impact Bullet Point Tailoring",
        "tailoring_subtitle": "Replace generic phrasing with quantifiable metrics and ATS-targeted keywords.",
        "original_bullet_label": "Original Resume Bullet:",
        "optimized_bullet_label": "ATS-Optimized Recommended Bullet:",
        "copy_btn": "Copy",
        "copied_btn": "Copied!",
        
        "rate_limit_title": "Rate Limit Exceeded (Free Tier Protection)",
        "rate_limit_desc": "To keep this service 100% free and fast for everyone, requests are limited to 2 analyses per minute per user.",
        "rate_limit_wait": "Please wait a few moments before submitting another scan.",
        
        "footer_tagline": "Empowering job seekers with enterprise-grade ATS transparency.",
        "footer_privacy": "Privacy-First (No Data Saved) • In-Memory Processing",
        
        "error_default_title": "Unable to Complete Analysis",
        "error_high_demand_title": "AI Service Temporarily Busy",
        "error_high_demand_msg": "Our AI analysis service is experiencing temporary high demand. Your file was processed safely in-memory, but the analysis timed out.",
        "error_suggestion_retry": "Please wait a moment and click 'Try Again' below to re-submit.",
        "error_bot_msg": "Automated submission rejected. If you are a human user, please try again.",
        "error_jd_empty": "Job Description cannot be empty. Please paste the job requirements and responsibilities in the text box.",
        "error_pdf_empty": "Uploaded resume file is empty. Please select a valid PDF file.",
        "error_pdf_read": "Unable to read the uploaded resume. Please make sure the PDF is text-based (not a scanned image) and under 120KB.",
        "error_footer_note": "PDF must be text-based (max 120KB, max 3 pages).",
        "btn_try_again": "Try Again",
    },
    "pt": {
        "lang_code": "pt",
        "lang_name": "Português",
        "title": "Verificador de Currículo ATS Gratuito | Score de Compatibilidade",
        "meta_description": "Verificador de Currículo ATS 100% Gratuito e sem cadastro. Compare seu currículo com qualquer vaga e receba feedback e otimizações instantâneas por IA.",
        "badge_free": "100% Grátis",
        "btn_download_template": "Baixar Modelo (.docx)",
        "badge_privacy": "100% Privado • Currículos Nunca Salvos",
        "hero_title_prefix": "Vença o ATS. Conquiste Mais ",
        "hero_title_highlight": "Entrevistas",
        "hero_title_suffix": ".",
        "hero_subtitle": "Envie seu currículo em PDF e cole a descrição da vaga. Nosso simulador ATS com IA analisa lacunas de habilidades, correspondência de palavras-chave e cria melhorias imediatas para suas experiências.",
        
        "upload_col_title": "1. Enviar Currículo (PDF)",
        "upload_col_limits": "Máx {max_pdf_kb}KB • Máx {max_pages} páginas",
        "dropzone_prompt": "Clique para enviar ou arraste o arquivo",
        "dropzone_subprompt": "Apenas arquivos PDF padrão",
        "dropzone_change_btn": "Remover e Escolher Outro",
        "upload_security_notice": "Processado com segurança em memória. Nunca indexado ou armazenado.",
        
        "jd_col_title": "2. Colar Descrição da Vaga (JD)",
        "jd_col_counter": "{chars} / {max_chars} caracteres",
        "jd_placeholder": "Cole aqui os requisitos, qualificações e responsabilidades da vaga desejada...",
        "jd_tip": "Inclui palavras-chave, experiência necessária e stack tecnológica.",
        "jd_clear_btn": "Limpar",
        
        "btn_analyze": "Executar Análise Completa ATS",
        "btn_analyzing": "Simulando Scanners ATS...",
        
        "loading_step_1": "Lendo e verificando camadas de texto do PDF...",
        "loading_step_2": "Simulando extração de tokens de parser ATS...",
        "loading_step_3": "Cruzando competências e senioridade com IA Dupla...",
        "loading_step_4": "Criando otimizações de bullet points no padrão Google XYZ...",
        
        "results_title": "Veredito e Análise de Compatibilidade ATS",
        "results_subtitle": "Comparado com os requisitos essenciais da vaga e filtros de triagem ATS.",
        "results_score_label": "Score ATS",
        "score_strong": "Forte Compatibilidade para Entrevista",
        "score_moderate": "Compatibilidade Média • Requer Ajustes",
        "score_low": "Baixa Compatibilidade • Lacunas Críticas",
        "verdict_title": "Veredito Estratégico de Recrutamento",
        "experience_gap_title": "Avaliação de Experiência e Senioridade",
        "matched_keywords_title": "Palavras-chave Encontradas",
        "missing_keywords_title": "Palavras-chave Críticas Ausentes",
        "no_matched_keywords": "Nenhuma palavra-chave exata significativa foi detectada.",
        "all_keywords_present": "✨ Todas as palavras-chave essenciais da vaga estão presentes no seu currículo!",
        "missing_keywords_tip": "💡 Dica: Incorpore estes termos de forma natural nas suas experiências de trabalho caso possua vivência com eles.",
        "tailoring_title": "🎯 Otimização de Experiências (Bullet Points)",
        "tailoring_subtitle": "Substitua frases genéricas por métricas quantificáveis e termos estratégicos de ATS.",
        "original_bullet_label": "Frase Original no Currículo:",
        "optimized_bullet_label": "Frase Otimizada Recomendada:",
        "copy_btn": "Copiar",
        "copied_btn": "Copiado!",
        
        "rate_limit_title": "Limite de Requisições Atingido (Proteção Gratuita)",
        "rate_limit_desc": "Para manter este serviço 100% gratuito e rápido para todos, o limite é de 2 análises por minuto por usuário.",
        "rate_limit_wait": "Por favor, aguarde alguns instantes antes de enviar uma nova análise.",
        
        "footer_tagline": "Dando aos candidatos transparência de nível corporativo sobre triagens ATS.",
        "footer_privacy": "Privacidade em 1º Lugar (Sem Dados Salvos) • Processamento em Memória",
        
        "error_default_title": "Não foi possível concluir a análise",
        "error_high_demand_title": "Serviço de IA Temporariamente Ocupado",
        "error_high_demand_msg": "Nosso serviço de IA está com alta demanda momentânea. Seu arquivo foi processado com segurança em memória, mas o tempo limite de análise expirou.",
        "error_suggestion_retry": "Por favor, aguarde alguns segundos e clique em 'Tentar Novamente' abaixo.",
        "error_bot_msg": "Envio automatizado rejeitado. Se você é um usuário real, tente novamente.",
        "error_jd_empty": "A Descrição da Vaga não pode estar vazia. Cole os requisitos e atribuições da vaga na caixa de texto.",
        "error_pdf_empty": "O arquivo de currículo enviado está vazio. Selecione um PDF válido.",
        "error_pdf_read": "Não foi possível ler o currículo enviado. Certifique-se de que o PDF contenha texto selecionável (não seja imagem escaneada) e tenha menos de 120KB.",
        "error_footer_note": "O PDF deve ser baseado em texto (máx 120KB, máx 3 páginas).",
        "btn_try_again": "Tentar Novamente",
    }
}

def get_translations(lang: str = "en") -> Dict[str, Any]:
    """Returns the translation dictionary for the given language code, defaulting to 'en'."""
    normalized = (lang or "").lower().strip()
    if normalized.startswith("pt"):
        return TRANSLATIONS["pt"]
    return TRANSLATIONS["en"]
