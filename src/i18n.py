"""
Internationalization (i18n) dictionary and helper for ATS MatchProof.
Supported languages: English ('en', default) and Portuguese ('pt').
"""

from typing import Any, Dict

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "en": {
        "lang_code": "en",
        "lang_name": "English",
        "site_name": "ATS MatchProof",
        "title": "ATS MatchProof | Free ATS Resume & Job Matcher • AI Score & Optimization",
        "meta_description": "ATS MatchProof is a 100% free, zero-account ATS Resume & Job Matcher. Compare your resume against any job description with instant AI feedback, keyword extraction, and Google XYZ optimizations.",
        "og_image_alt": "ATS MatchProof - Free ATS Resume & Job Matcher with AI Score",

        # Navigation
        "nav_home": "Analyzer",
        "nav_guide": "ATS Guide",
        "nav_about": "About Us",
        "nav_contact": "Contact",
        "nav_privacy": "Privacy Policy",
        "nav_terms": "Terms of Service",
        "nav_faq": "FAQ",

        # Badges & Buttons
        "badge_free": "100% Free",
        "btn_download_template": "Download ATS Template (.docx)",
        "badge_privacy": "100% Private • Resumes Never Stored",

        # Hero Section
        "hero_title_prefix": "Beat the ATS. Land More ",
        "hero_title_highlight": "Interviews",
        "hero_title_suffix": ".",
        "hero_subtitle": "Upload your resume PDF and paste the job description. Our dual-engine ATS simulator analyzes skill gaps, keyword matching, and crafts instant recruiter-grade bullet points using the Google XYZ formula.",

        # Form Fields
        "upload_col_title": "1. Upload Resume (PDF)",
        "upload_col_limits": "Max {max_pdf_kb}KB • {max_pages} pages",
        "dropzone_prompt": "Click to upload or drag and drop",
        "dropzone_subprompt": "Standard text-based PDF files only",
        "dropzone_change_btn": "Remove & Choose Another",
        "upload_security_notice": "Parsed securely in-memory. Resumes are never saved to disk or database.",
        "jd_col_title": "2. Job Description (JD)",
        "jd_col_counter": "{chars} / {max_chars} chars",
        "jd_placeholder": "Paste the target job requirements, qualifications, responsibilities, and tech stack here...",
        "jd_tip": "Paste the full text for maximum keyword accuracy.",
        "jd_clear_btn": "Clear Text",
        "btn_analyze": "Run ATS DeepScan Analysis",
        "btn_analyzing": "Simulating ATS Scanners...",

        # Loading Steps
        "loading_step_1": "Reading and verifying PDF text layer...",
        "loading_step_2": "Simulating ATS parser token extraction...",
        "loading_step_3": "Benchmarking skills and experience with Dual-AI...",
        "loading_step_4": "Crafting Google XYZ bullet point optimizations...",

        # Results View
        "results_title": "ATS Match Verdict & Analysis",
        "results_subtitle": "Benchmarked against target job requirements and ATS keyword filters.",
        "results_score_label": "ATS Match Score",
        "score_strong": "Strong Interview Match",
        "score_moderate": "Moderate Match • Needs Tailoring",
        "score_low": "Low Match • Significant Gaps",
        "verdict_title": "Strategic Recruiter Verdict",
        "experience_gap_title": "Experience & Seniority Assessment",
        "matched_keywords_title": "Matched Keywords Found",
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
        "export_toolbar_title": "Export & Share Analysis",
        "export_pdf_btn": "Print / Save PDF",
        "export_copy_btn": "Copy Full Report",
        "export_download_btn": "Download (.txt)",
        "export_copied": "Full Report Copied!",

        # Rate Limiting & Errors
        "rate_limit_title": "Rate Limit Exceeded (Free Tier Protection)",
        "rate_limit_desc": "To keep this service 100% free and fast for everyone, requests are limited to 2 analyses per minute per user.",
        "rate_limit_wait": "Please wait a few moments before submitting another scan.",
        "error_default_title": "Unable to Complete Analysis",
        "error_high_demand_title": "AI Service Temporarily Busy",
        "error_high_demand_msg": "Our AI analysis service is experiencing temporary high demand. Your file was processed safely in-memory, but the analysis timed out.",
        "error_suggestion_retry": "Please wait a moment and click 'Try Again' below to re-submit.",
        "error_bot_msg": "Automated submission rejected. If you are a human user, please try again.",
        "error_jd_empty": "Job Description cannot be empty. Please paste the job requirements and responsibilities in the text box.",
        "error_jd_too_long": "Job Description exceeds the maximum limit of {max_chars} characters. Please shorten it to proceed.",
        "error_pdf_empty": "Uploaded resume file is empty. Please select a valid PDF file.",
        "error_pdf_read": "Unable to read the uploaded resume. Please make sure the PDF is text-based (not a scanned image) and under 120KB.",
        "error_footer_note": "PDF must be text-based (max 120KB, max 3 pages).",
        "btn_try_again": "Try Again",

        # Educational Homepage Content
        "edu_title": "How to Master the Applicant Tracking System (ATS)",
        "edu_subtitle": "Over 75% of resumes are filtered out before reaching human recruiters. Learn how ATS algorithms score applications and how to optimize your resume effectively.",

        "edu_card1_title": "How ATS Algorithms Work",
        "edu_card1_desc": "Applicant Tracking Systems (like Workday, Taleo, Greenhouse, and Lever) parse incoming resumes into structured candidate profiles. They tokenize your text, extract skills, categorize employment dates, and rank candidates based on keyword relevance and semantic similarity to the job description.",

        "edu_card2_title": "The Google XYZ Formula",
        "edu_card2_desc": "Top recruiters look for measurable impact, not just a list of daily responsibilities. Formulate every achievement as: 'Accomplished [X], as measured by [Y], by doing [Z]'. This structure proves business value, incorporates target keywords, and immediately elevates your resume above competitors.",

        "edu_card3_title": "Formatting for Clean Parsing",
        "edu_card3_desc": "Complex two-column graphics, text boxes, tables, icons, and non-standard fonts cause parsing errors in older ATS parsers. Use a single-column, standard reverse-chronological layout with clean headings and UTF-8 bullet points to guarantee 100% readability.",

        # Before/After Examples Section
        "examples_title": "Before vs After: Google XYZ Bullet Points",
        "examples_subtitle": "See how rewriting generic statements into metric-driven XYZ statements dramatically improves ATS keyword scores and recruiter appeal.",
        "example1_role": "Software Engineer",
        "example1_bad": "Worked on backend APIs and fixed system bugs for our web application.",
        "example1_good": "Engineered 12+ scalable REST APIs using Python and FastAPI, reducing average latency by 38% and supporting 150k daily active users.",
        "example2_role": "Marketing Specialist",
        "example2_bad": "Managed email marketing campaigns and monitored social media metrics.",
        "example2_good": "Designed and executed 24 automated email nurturing workflows in HubSpot, generating $420k in pipeline revenue with a 28% open rate.",
        "example3_role": "Product Manager",
        "example3_bad": "Led sprint planning and coordinated feature launches with the engineering team.",
        "example3_good": "Spearheaded end-to-end launch of customer onboarding portal across 4 cross-functional squads, cutting user drop-off by 45% in Q3.",

        # Checklist Section
        "checklist_title": "Essential ATS Compliance Checklist",
        "checklist_subtitle": "Review these 6 vital rules before submitting your application to any corporate job portal.",
        "checklist_item1": "File Format: Use text-searchable PDF or standard DOCX without embedded image scans.",
        "checklist_item2": "Keyword Alignment: Match exact technical skills, tools, and certifications mentioned in the job post.",
        "checklist_item3": "Layout Simplicity: Avoid tables, nested boxes, headers/footers with critical contact info.",
        "checklist_item4": "Standard Headings: Stick to standard titles like 'Work Experience', 'Education', and 'Skills'.",
        "checklist_item5": "Quantifiable Metrics: Include numbers, percentages, currency, and measurable results in every role.",
        "checklist_item6": "No Keyword Stuffing: Use keywords in natural, contextual sentences rather than hidden blocks.",

        # FAQ Section
        "faq_title": "Frequently Asked Questions",
        "faq_subtitle": "Everything you need to know about ATS MatchProof, resume parsing, and hiring algorithms.",
        "faqs": [
            {
                "q": "What is an ATS (Applicant Tracking System)?",
                "a": "An Applicant Tracking System (ATS) is software used by employers, recruiters, and HR teams to collect, organize, filter, and rank job applicants. When you submit a resume online, the ATS parses the document to determine if your qualifications match the job description before a human recruiter ever sees it."
            },
            {
                "q": "Is ATS MatchProof completely free to use?",
                "a": "Yes! ATS MatchProof is 100% free with no account creation, subscription, or payment required. You can scan and tailor your resume against multiple job descriptions without entering credit card information."
            },
            {
                "q": "Is my resume private and secure?",
                "a": "Absolutely. We operate on a strict privacy-first, zero-retention policy. Uploaded PDFs are parsed strictly in server RAM and immediately discarded. We never store, sell, log, or train public AI models on your resume, contact info, or job descriptions."
            },
            {
                "q": "Why is my ATS score lower than expected?",
                "a": "A lower score usually means your resume is missing exact keyword matches found in the job description, uses generic bullet points without measurable impact, or lacks the specific technical stack or certifications required. Use our feedback to bridge these gaps."
            },
            {
                "q": "Can I use creative templates with two columns and graphics?",
                "a": "While creative multi-column templates may look visually appealing to humans, they often confuse ATS parsers, resulting in scrambled text, missing experience sections, or lost contact details. For corporate applications, a clean single-column format is recommended."
            },
            {
                "q": "What is the Google XYZ formula?",
                "a": "The Google XYZ formula was popularized by Google's former SVP of People Operations, Laszlo Bock. It structures bullet points as: 'Accomplished [X], as measured by [Y], by doing [Z]'. This format clearly demonstrates your action, the metric used to gauge success, and your unique method."
            },
            {
                "q": "How many pages should my resume be?",
                "a": "For candidates with fewer than 5–7 years of experience, a single page is standard. For senior professionals, researchers, or executives with 10+ years of relevant experience, a 2-page resume is acceptable. Avoid 3+ pages unless submitting an academic CV."
            },
            {
                "q": "What is keyword stuffing and why should I avoid it?",
                "a": "Keyword stuffing is the practice of unnaturally repeating keywords (or hiding white text in margins) to manipulate ATS scanners. Modern ATS parsers easily detect this, and human recruiters will immediately disqualify applications with artificial keyword blocks."
            }
        ],

        # Footer
        "footer_about": "ATS MatchProof is an open, privacy-first career enablement tool designed to give job seekers algorithmic transparency and enterprise-grade resume optimization.",
        "footer_quick_links": "Quick Links",
        "footer_legal": "Legal & Privacy",
        "footer_resources": "Resources",
        "footer_tagline": "Empowering job seekers with enterprise-grade ATS transparency.",
        "footer_privacy": "Privacy-First (No Data Saved) • In-Memory Processing",
        "footer_rights": "All rights reserved.",

        # Dedicated Pages Titles & Meta
        "page_privacy_title": "Privacy Policy | ATS MatchProof",
        "page_terms_title": "Terms of Service | ATS MatchProof",
        "page_about_title": "About Us & Mission | ATS MatchProof",
        "page_contact_title": "Contact & Support | ATS MatchProof",
        "page_guide_title": "The Ultimate ATS Resume Optimization Guide (2026) | ATS MatchProof",
    },

    "pt": {
        "lang_code": "pt",
        "lang_name": "Português",
        "site_name": "ATS MatchProof",
        "title": "ATS MatchProof | Verificador de Currículo ATS Gratuito • Score e Otimização com IA",
        "meta_description": "ATS MatchProof é um verificador de currículo ATS 100% gratuito e sem cadastro. Compare seu currículo com qualquer vaga e receba feedback, palavras-chave e otimizações na Fórmula Google XYZ.",
        "og_image_alt": "ATS MatchProof - Verificador de Currículo ATS Gratuito com IA",

        # Navigation
        "nav_home": "Analisador",
        "nav_guide": "Guia ATS",
        "nav_about": "Sobre Nós",
        "nav_contact": "Contato",
        "nav_privacy": "Privacidade",
        "nav_terms": "Termos de Uso",
        "nav_faq": "FAQ",

        # Badges & Buttons
        "badge_free": "100% Grátis",
        "btn_download_template": "Baixar Modelo ATS (.docx)",
        "badge_privacy": "100% Privado • Currículos Nunca Salvos",

        # Hero Section
        "hero_title_prefix": "Vença o ATS. Conquiste Mais ",
        "hero_title_highlight": "Entrevistas",
        "hero_title_suffix": ".",
        "hero_subtitle": "Envie seu currículo em PDF e cole a descrição da vaga. Nosso simulador ATS com IA analisa lacunas de habilidades, correspondência de palavras-chave e cria melhorias imediatas no padrão de recrutamento Google XYZ.",

        # Form Fields
        "upload_col_title": "1. Enviar Currículo (PDF)",
        "upload_col_limits": "Máx {max_pdf_kb}KB • {max_pages} págs",
        "dropzone_prompt": "Clique para enviar ou arraste o arquivo",
        "dropzone_subprompt": "Apenas arquivos PDF baseados em texto",
        "dropzone_change_btn": "Remover e Escolher Outro",
        "upload_security_notice": "Processado em memória. Currículos nunca são salvos em disco ou banco de dados.",
        "jd_col_title": "2. Descrição da Vaga (JD)",
        "jd_col_counter": "{chars} / {max_chars} carac.",
        "jd_placeholder": "Cole aqui os requisitos, qualificações, responsabilidades e stack técnica da vaga desejada...",
        "jd_tip": "Cole o texto completo da vaga para maior precisão de palavras-chave.",
        "jd_clear_btn": "Limpar Texto",
        "btn_analyze": "Executar Análise Completa ATS",
        "btn_analyzing": "Simulando Scanners ATS...",

        # Loading Steps
        "loading_step_1": "Lendo e verificando camadas de texto do PDF...",
        "loading_step_2": "Simulando extração de tokens de parser ATS...",
        "loading_step_3": "Cruzando competências e senioridade com IA Dupla...",
        "loading_step_4": "Criando otimizações de bullet points no padrão Google XYZ...",

        # Results View
        "results_title": "Veredito e Análise de Compatibilidade ATS",
        "results_subtitle": "Comparado com os requisitos essenciais da vaga e filtros de triagem ATS.",
        "results_score_label": "Score de Compatibilidade ATS",
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
        "tailoring_title": "🎯 Otimização de Experiências (Fórmula Google XYZ)",
        "tailoring_subtitle": "Substitua frases genéricas por métricas quantificáveis e termos estratégicos de ATS.",
        "original_bullet_label": "Frase Original no Currículo:",
        "optimized_bullet_label": "Frase Otimizada Recomendada:",
        "copy_btn": "Copiar",
        "copied_btn": "Copiado!",
        "export_toolbar_title": "Exportar e Compartilhar Relatório",
        "export_pdf_btn": "Salvar / Imprimir PDF",
        "export_copy_btn": "Copiar Relatório",
        "export_download_btn": "Baixar (.txt)",
        "export_copied": "Relatório Copiado!",

        # Rate Limiting & Errors
        "rate_limit_title": "Limite de Requisições Atingido (Proteção Gratuita)",
        "rate_limit_desc": "Para manter este serviço 100% gratuito e rápido para todos, o limite é de 2 análises por minuto por usuário.",
        "rate_limit_wait": "Por favor, aguarde alguns instantes antes de enviar uma nova análise.",
        "error_default_title": "Não foi possível concluir a análise",
        "error_high_demand_title": "Serviço de IA Temporariamente Ocupado",
        "error_high_demand_msg": "Nosso serviço de IA está com alta demanda momentânea. Seu arquivo foi processado com segurança em memória, mas o tempo limite de análise expirou.",
        "error_suggestion_retry": "Por favor, aguarde alguns segundos e clique em 'Tentar Novamente' abaixo.",
        "error_bot_msg": "Envio automatizado rejeitado. Se você é um usuário real, tente novamente.",
        "error_jd_empty": "A Descrição da Vaga não pode estar vazia. Cole os requisitos e atribuições da vaga na caixa de texto.",
        "error_jd_too_long": "A Descrição da Vaga excede o limite máximo de {max_chars} caracteres. Reduza o texto para prosseguir.",
        "error_pdf_empty": "O arquivo de currículo enviado está vazio. Selecione um PDF válido.",
        "error_pdf_read": "Não foi possível ler o currículo enviado. Certifique-se de que o PDF contenha texto selecionável (não seja imagem escaneada) e tenha menos de 120KB.",
        "error_footer_note": "O PDF deve ser baseado em texto (máx 120KB, máx 3 páginas).",
        "btn_try_again": "Tentar Novamente",

        # Educational Homepage Content
        "edu_title": "Como Dominar os Sistemas de Triagem ATS",
        "edu_subtitle": "Mais de 75% dos currículos são descartados por robôs antes de chegarem aos recrutadores humanos. Descubra como os algoritmos avaliam seu perfil e como otimizar seu currículo.",

        "edu_card1_title": "Como Funcionam os Algoritmos de ATS",
        "edu_card1_desc": "Sistemas de Triagem de Candidatos (como Gupy, Workday, Taleo, Greenhouse e Lever) transformam seu arquivo PDF em um perfil de dados estruturado. Eles extraem palavras-chave, analisam a cronologia das suas experiências e calculam uma nota de aderência em relação aos requisitos da vaga.",

        "edu_card2_title": "A Fórmula Google XYZ",
        "edu_card2_desc": "Grandes empresas não querem ler listas de tarefas rotineiras, mas sim impacto comprovado. Escreva suas realizações na estrutura: 'Realizei [X], medido por [Y], fazendo [Z]'. Essa fórmula destaca métricas claras, insere palavras-chave essenciais e comprova seu valor para a empresa.",

        "edu_card3_title": "Formatação Compatível com Parsers",
        "edu_card3_desc": "Colunas duplas sofisticadas, caixas de texto flutuantes, tabelas e fontes não convencionais confundem os robôs de triagem. Utilize layouts de coluna única, títulos tradicionais ('Experiência', 'Educação', 'Habilidades') e ordem cronológica inversa.",

        # Before/After Examples Section
        "examples_title": "Antes vs Depois: Fórmula Google XYZ na Prática",
        "examples_subtitle": "Veja a diferença entre frases de responsabilidade comuns e conquistas otimizadas para ranquear no topo do ATS.",
        "example1_role": "Desenvolvedor de Software",
        "example1_bad": "Responsável por desenvolver APIs no backend e corrigir bugs no sistema.",
        "example1_good": "Desenvolvi mais de 12 APIs REST escaláveis em Python e FastAPI, reduzindo a latência média em 38% e suportando 150 mil usuários ativos diários.",
        "example2_role": "Especialista em Marketing",
        "example2_bad": "Gerenciava disparos de e-mail marketing e acompanhava métricas de redes sociais.",
        "example2_good": "Criei 24 fluxos automatizados de nutrição no HubSpot, gerando R$ 420 mil em pipeline de vendas com taxa média de abertura de 28%.",
        "example3_role": "Gerente de Produto (PM)",
        "example3_bad": "Liderava reuniões de sprint e organizava lançamentos de funcionalidades com os desenvolvedores.",
        "example3_good": "Liderei o lançamento de ponta a ponta do novo portal de onboarding com 4 squads, diminuindo a taxa de abandono em 45% no 3º trimestre.",

        # Checklist Section
        "checklist_title": "Checklist Definitivo de Aprovação no ATS",
        "checklist_subtitle": "Verifique estes 6 pontos indispensáveis antes de submeter sua candidatura a qualquer processo seletivo.",
        "checklist_item1": "Formato do Arquivo: Envie sempre em PDF com texto pesquisável ou DOCX sem imagens incorporadas.",
        "checklist_item2": "Alinhamento de Termos: Utilize as mesmas nomenclaturas de ferramentas, metodologias e certificações da vaga.",
        "checklist_item3": "Layout Simples: Evite cabeçalhos com dados de contato ocultos, colunas complexas ou tabelas.",
        "checklist_item4": "Títulos Clássicos: Mantenha seções padrão como 'Experiência Profissional', 'Formação Acadêmica' e 'Competências'.",
        "checklist_item5": "Métricas Quantitativas: Inclua números, percentuais e resultados de negócio em cada uma das suas experiências.",
        "checklist_item6": "Sem Keyword Stuffing: Insira palavras-chave contextualmente em frases reais, nunca em blocos de texto escondidos.",

        # FAQ Section
        "faq_title": "Perguntas Frequentes sobre ATS e Currículos",
        "faq_subtitle": "Tudo o que você precisa saber sobre o funcionamento de robôs de RH e otimização de currículo.",
        "faqs": [
            {
                "q": "O que é um sistema ATS (Applicant Tracking System)?",
                "a": "Um ATS é um software corporativo utilizado por equipes de Recursos Humanos e recrutadores para receber, organizar, triar e classificar candidaturas de emprego. O sistema lê o conteúdo do seu currículo e compara suas qualificações com os requisitos da vaga antes de qualquer pessoa avaliar seu perfil."
            },
            {
                "q": "O ATS MatchProof é realmente gratuito?",
                "a": "Sim! O ATS MatchProof é 100% gratuito, sem necessidade de cadastro, criação de conta ou pagamento. Você pode comparar e otimizar seu currículo contra quantas vagas desejar sem informar dados de cartão de crédito."
            },
            {
                "q": "Meus dados e currículo estão seguros e privados?",
                "a": "Sim, com segurança absoluta. Operamos sob uma política rígida de retenção zero. O PDF enviado é processado exclusivamente na memória RAM do servidor durante a análise e é descartado imediatamente. Não salvamos currículos em disco nem em banco de dados, e não treinamos modelos públicos com seus dados."
            },
            {
                "q": "Por que minha nota de compatibilidade ATS deu baixa?",
                "a": "Uma pontuação menor geralmente indica que faltam palavras-chave específicas exigidas na vaga, que as descrições de experiência estão genéricas sem números de impacto, ou que a senioridade das tecnologias mencionadas difere da vaga. Utilize as sugestões da análise para ajustar esses pontos."
            },
            {
                "q": "Posso usar modelos visuais com gráficos, barras de nível e colunas duplas?",
                "a": "Embora pareçam bonitos visualmente, modelos com colunas duplas, barras de progresso de habilidades e caixas de texto flutuantes frequentemente causam erros graves de leitura nos robôs de triagem. Para passar nos filtros, o layout de coluna única limpo é o mais seguro e recomendado."
            },
            {
                "q": "O que é a Fórmula Google XYZ?",
                "a": "Popularizada por Laszlo Bock (ex-SVP de Pessoas do Google), a fórmula estrutura cada conquista no formato: 'Realizei [X], medido por [Y], fazendo [Z]'. Essa estrutura evidencia o que você fez, a métrica de sucesso alcançada e o método utilizado."
            },
            {
                "q": "Quantas páginas deve ter o meu currículo?",
                "a": "Para profissionais com até 5 a 7 anos de experiência, 1 página é o ideal. Para profissionais seniores, especialistas ou executivos com mais de 10 anos de carreira relevante, 2 páginas são perfeitamente aceitas. Evite currículos de 3 ou mais páginas."
            },
            {
                "q": "O que é 'Keyword Stuffing' e por que devo evitar?",
                "a": "Keyword stuffing é a prática de repetir palavras-chave de forma artificial (como colar uma lista de termos em letra branca minúscula no rodapé). Os parsers modernos identificam essa tentativa de manipulação com facilidade e os recrutadores descartam imediatamente o candidato."
            }
        ],

        # Footer
        "footer_about": "O ATS MatchProof é uma ferramenta de carreira aberta e focada em privacidade, criada para oferecer aos candidatos transparência algorítmica e otimização profissional de currículos.",
        "footer_quick_links": "Links Rápidos",
        "footer_legal": "Legal & Privacidade",
        "footer_resources": "Recursos",
        "footer_tagline": "Dando aos candidatos transparência de nível corporativo sobre triagens ATS.",
        "footer_privacy": "Privacidade em 1º Lugar (Sem Dados Salvos) • Processamento em Memória",
        "footer_rights": "Todos os direitos reservados.",

        # Dedicated Pages Titles & Meta
        "page_privacy_title": "Política de Privacidade | ATS MatchProof",
        "page_terms_title": "Termos de Uso e Serviço | ATS MatchProof",
        "page_about_title": "Sobre Nós e Missão | ATS MatchProof",
        "page_contact_title": "Contato e Suporte | ATS MatchProof",
        "page_guide_title": "Guia Definitivo de Otimização de Currículo para ATS (2026) | ATS MatchProof",
    },
}


def get_translations(lang: str = "en") -> Dict[str, Any]:
    """Returns the translation dictionary for the given language code, defaulting to 'en'."""
    normalized = (lang or "").lower().strip()
    if normalized.startswith("pt"):
        return TRANSLATIONS["pt"]
    return TRANSLATIONS["en"]
