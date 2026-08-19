#!/usr/bin/env python3
"""
Generates an ATS-Optimized Resume Template in .docx format without external dependencies.
Uses the OpenXML / WordprocessingML standard schema.
"""
import os
import zipfile

def generate_resume_docx(output_path: str):
    content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    package_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    document_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>
        <w:sz w:val="21"/>
        <w:szCs w:val="21"/>
        <w:color w:val="222222"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:line="260" w:lineRule="auto" w:after="80"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>"""

    # Helper function to generate paragraphs and tables
    doc_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    <!-- PAGE TITLE / CANDIDATE NAME -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="0" w:after="40" w:line="240" w:lineRule="auto"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="40"/>
          <w:szCs w:val="40"/>
          <w:color w:val="111827"/>
        </w:rPr>
        <w:t>John Doe</w:t>
      </w:r>
    </w:p>

    <!-- CONTACT DETAILS (TWO COLUMN TABLE) -->
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="10000" w:type="dxa"/>
        <w:tblBorders>
          <w:top w:val="none"/>
          <w:left w:val="none"/>
          <w:bottom w:val="none"/>
          <w:right w:val="none"/>
          <w:insideH w:val="none"/>
          <w:insideV w:val="none"/>
        </w:tblBorders>
        <w:tblCellMar>
          <w:top w:w="0" w:type="dxa"/>
          <w:bottom w:w="30" w:type="dxa"/>
          <w:left w:w="0" w:type="dxa"/>
          <w:right w:w="0" w:type="dxa"/>
        </w:tblCellMar>
      </w:tblPr>
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="5500" w:type="dxa"/></w:tcPr>
          <w:p>
            <w:pPr><w:spacing w:before="0" w:after="20"/></w:pPr>
            <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>LinkedIn: </w:t></w:r>
            <w:r><w:rPr><w:sz w:val="19"/><w:color w:val="1F2937"/></w:rPr><w:t>linkedin.com/in/johndoe</w:t></w:r>
          </w:p>
          <w:p>
            <w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr>
            <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>GitHub: </w:t></w:r>
            <w:r><w:rPr><w:sz w:val="19"/><w:color w:val="1F2937"/></w:rPr><w:t>github.com/johndoe</w:t></w:r>
          </w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="4500" w:type="dxa"/></w:tcPr>
          <w:p>
            <w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="20"/></w:pPr>
            <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Email: </w:t></w:r>
            <w:r><w:rPr><w:sz w:val="19"/><w:color w:val="1F2937"/></w:rPr><w:t>john.doe@example.com</w:t></w:r>
          </w:p>
          <w:p>
            <w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="40"/></w:pPr>
            <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Phone: </w:t></w:r>
            <w:r><w:rPr><w:sz w:val="19"/><w:color w:val="1F2937"/></w:rPr><w:t>+9999999999999</w:t></w:r>
          </w:p>
        </w:tc>
      </w:tr>
    </w:tbl>

    <!-- SECTION: SKILLS -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr>
          <w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/>
        </w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="26"/>
          <w:szCs w:val="26"/>
          <w:color w:val="111827"/>
        </w:rPr>
        <w:t>Skills</w:t>
      </w:r>
    </w:p>

    <!-- Skills items -->
    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="20"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• Languages: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Python, TypeScript, JavaScript, Go, PHP, SQL</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="0" w:after="20"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• Frameworks: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>FastAPI, Django, Flask, React, Next.js, Node.js, Nest.js</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="0" w:after="20"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• DevOps &amp; CI/CD: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Docker, Kubernetes, GitHub Actions, Terraform, Linux, Nginx</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="0" w:after="20"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• Databases: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>PostgreSQL, MySQL, Redis, MongoDB, DynamoDB</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="0" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• Cloud &amp; Arch: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>AWS, GCP, Microservices, Event-Driven Architecture</w:t></w:r>
    </w:p>

    <!-- SECTION: SUMMARY -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr>
          <w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/>
        </w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="26"/>
          <w:szCs w:val="26"/>
          <w:color w:val="111827"/>
        </w:rPr>
        <w:t>Summary</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="80"/><w:jc w:val="both"/></w:pPr>
      <w:r>
        <w:rPr><w:sz w:val="20"/></w:rPr>
        <w:t>Senior Software Engineer with 5+ years of experience building and scaling high-performance backend systems and distributed services. Proven track record of delivering measurable outcomes, such as 25% API performance gains and automating business-critical operations. Passionate about domain-driven design, clean and testable architectures (unit &amp; e2e testing), and modernizing legacy codebases while maintaining continuous uptime. Pragmatic team collaborator focused on high-leverage technical decisions that directly accelerate business growth.</w:t>
      </w:r>
    </w:p>

    <!-- SECTION: EXPERIENCES -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr>
          <w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/>
        </w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="26"/>
          <w:szCs w:val="26"/>
          <w:color w:val="111827"/>
        </w:rPr>
        <w:t>Experiences</w:t>
      </w:r>
    </w:p>

    <!-- JOB 1 -->
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="10000" w:type="dxa"/>
        <w:tblBorders>
          <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
        <w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>
      </w:tblPr>
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="6000" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/><w:color w:val="111827"/></w:rPr><w:t>Acme Cloud Technologies</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="374151"/></w:rPr><w:t>Senior Full Stack Engineer</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="4000" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>San Francisco, CA (Remote)</w:t></w:r></w:p>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Jul 2024 - Present</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>

    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Accelerated page setup velocity by 90% by engineering reusable Python/Django admin mixins for automated deep-cloning of multi-relational entity configurations.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Prevented 100% of unwanted third-party AI API token consumption on disabled client tiers by implementing granular server-side feature flags with admin controls.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Eliminated 100% of manual code assessment work by architecting an automated evaluation webhook pipeline integrated with an AI-powered grading microservice.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Cut administrative credentialing overhead by 90% by creating an automated lifecycle API with domain validation rules and automated certificate generation.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="200"/><w:spacing w:before="20" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="374151"/></w:rPr><w:t>• Context: </w:t></w:r>
      <w:r><w:rPr><w:i/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Acme Cloud is an enterprise SaaS platform focused on high-throughput microservices. Built internal tooling and automated integrations that eliminated manual operations across the application ecosystem.</w:t></w:r>
    </w:p>

    <!-- JOB 2 -->
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="10000" w:type="dxa"/>
        <w:tblBorders>
          <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
        <w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>
      </w:tblPr>
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="6000" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="60" w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/><w:color w:val="111827"/></w:rPr><w:t>TechFlow Solutions</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="374151"/></w:rPr><w:t>Full Stack Engineer</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="4000" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="60" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Austin, TX (Remote)</w:t></w:r></w:p>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Jul 2023 - Jun 2024</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>

    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Increased server performance by 15% through framework optimization, database connection pooling, and dependency modernization on production workloads.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Reduced CI/CD pipeline feedback time by 20% by parallelizing automated test execution suites using pytest-xdist within Docker containers.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Decreased critical endpoint query response times by 20x through query optimization, eliminating N+1 select bottlenecks and implementing indexed pagination.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Cut infrastructure costs by $12K annually by decommissioning idle dedicated worker pods and replacing them with an on-demand API architecture.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="200"/><w:spacing w:before="20" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="374151"/></w:rPr><w:t>• Context: </w:t></w:r>
      <w:r><w:rPr><w:i/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Focused on backend reliability and performance engineering — modernizing legacy services, optimizing PostgreSQL query execution, and accelerating CI/CD developer feedback loops.</w:t></w:r>
    </w:p>

    <!-- JOB 3 -->
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="10000" w:type="dxa"/>
        <w:tblBorders>
          <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
        <w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>
      </w:tblPr>
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="6000" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="60" w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/><w:color w:val="111827"/></w:rPr><w:t>Nova Digital Labs</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="374151"/></w:rPr><w:t>Backend Software Engineer</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="4000" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="60" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>New York, NY</w:t></w:r></w:p>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Jun 2022 - Jun 2023</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>

    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Shielded application attack surface by blocking automated bot probes and exploit path scans at the Nginx reverse proxy layer.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Prevented lead data loss from transient network timeouts by decoupling CRM synchronizations into asynchronous Celery workers with exponential backoff.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Reduced feed query response latency by 80% through parameterized multi-join result caching using Redis.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="200"/><w:spacing w:before="20" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="374151"/></w:rPr><w:t>• Context: </w:t></w:r>
      <w:r><w:rPr><w:i/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Delivered backend features and architectural integrations across core microservices while maintaining high test coverage and observability.</w:t></w:r>
    </w:p>

    <!-- SECTION: EDUCATION -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr>
          <w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/>
        </w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:b/>
          <w:sz w:val="26"/>
          <w:szCs w:val="26"/>
          <w:color w:val="111827"/>
        </w:rPr>
        <w:t>Education</w:t>
      </w:r>
    </w:p>

    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="10000" w:type="dxa"/>
        <w:tblBorders>
          <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
        <w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:bottom w:w="20" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>
      </w:tblPr>
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="6500" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="21"/><w:color w:val="111827"/></w:rPr><w:t>Tech University Institute</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Master of Science in Software Engineering &amp; AI</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="3500" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Aug 2024 - Dec 2025</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="6500" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="21"/><w:color w:val="111827"/></w:rPr><w:t>State University of Technology</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Bachelor of Science in Computer Science</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="3500" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Jan 2020 - Jun 2024</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>

    <!-- Page Setup (0.65in margins for maximum readable ATS surface) -->
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="936" w:right="936" w:bottom="936" w:left="936" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', content_types_xml)
        docx.writestr('_rels/.rels', package_rels_xml)
        docx.writestr('word/_rels/document.xml.rels', document_rels_xml)
        docx.writestr('word/styles.xml', styles_xml)
        docx.writestr('word/document.xml', doc_xml)

    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(out_dir, "resume_template.docx")
    generate_resume_docx(target_file)
