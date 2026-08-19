#!/usr/bin/env python3
"""
Generates ATS-Optimized Resume Templates in .docx format in both English and Portuguese
without external dependencies, using the OpenXML / WordprocessingML standard schema.
"""
import os
import zipfile

CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

PACKAGE_RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOCUMENT_RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

STYLES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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


def build_en_doc_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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
          <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
        <w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:bottom w:w="30" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>
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
            <w:r><w:rPr><w:sz w:val="19"/><w:color w:val="1F2937"/></w:rPr><w:t>+1 (555) 019-2834</w:t></w:r>
          </w:p>
        </w:tc>
      </w:tr>
    </w:tbl>

    <!-- SECTION: SKILLS -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/></w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="111827"/></w:rPr>
        <w:t>Skills</w:t>
      </w:r>
    </w:p>
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
        <w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/></w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="111827"/></w:rPr>
        <w:t>Summary</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="80"/><w:jc w:val="both"/></w:pPr>
      <w:r>
        <w:rPr><w:sz w:val="20"/></w:rPr>
        <w:t>Senior Software Engineer with 5+ years of experience building and scaling high-performance backend systems and distributed services. Proven track record of delivering measurable outcomes, such as 25% API latency reduction and automating business-critical operations. Passionate about domain-driven design, clean architectures, and modernizing legacy codebases while maintaining 99.9% uptime.</w:t>
      </w:r>
    </w:p>

    <!-- SECTION: EXPERIENCES -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/></w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="111827"/></w:rPr>
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
      <w:r><w:rPr><w:i/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Enterprise SaaS platform focused on high-throughput microservices. Built internal tooling and automated integrations that eliminated manual operations across the application ecosystem.</w:t></w:r>
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
        <w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/></w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="111827"/></w:rPr>
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

    <!-- Page Setup -->
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="936" w:right="936" w:bottom="936" w:left="936" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""


def build_pt_doc_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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
        <w:t>João Silva</w:t>
      </w:r>
    </w:p>

    <!-- CONTACT DETAILS (TWO COLUMN TABLE) -->
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="10000" w:type="dxa"/>
        <w:tblBorders>
          <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
        <w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:bottom w:w="30" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>
      </w:tblPr>
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="5500" w:type="dxa"/></w:tcPr>
          <w:p>
            <w:pPr><w:spacing w:before="0" w:after="20"/></w:pPr>
            <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>LinkedIn: </w:t></w:r>
            <w:r><w:rPr><w:sz w:val="19"/><w:color w:val="1F2937"/></w:rPr><w:t>linkedin.com/in/joaosilva</w:t></w:r>
          </w:p>
          <w:p>
            <w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr>
            <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>GitHub: </w:t></w:r>
            <w:r><w:rPr><w:sz w:val="19"/><w:color w:val="1F2937"/></w:rPr><w:t>github.com/joaosilva</w:t></w:r>
          </w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="4500" w:type="dxa"/></w:tcPr>
          <w:p>
            <w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="20"/></w:pPr>
            <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>E-mail: </w:t></w:r>
            <w:r><w:rPr><w:sz w:val="19"/><w:color w:val="1F2937"/></w:rPr><w:t>joao.silva@exemplo.com</w:t></w:r>
          </w:p>
          <w:p>
            <w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="40"/></w:pPr>
            <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Telefone: </w:t></w:r>
            <w:r><w:rPr><w:sz w:val="19"/><w:color w:val="1F2937"/></w:rPr><w:t>+55 (11) 99999-9999</w:t></w:r>
          </w:p>
        </w:tc>
      </w:tr>
    </w:tbl>

    <!-- SECTION: HABILIDADES -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/></w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="111827"/></w:rPr>
        <w:t>Habilidades</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="20"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• Linguagens: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Python, TypeScript, JavaScript, Go, PHP, SQL</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="0" w:after="20"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• Frameworks: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>FastAPI, Django, Flask, React, Next.js, Node.js, Nest.js</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="0" w:after="20"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• DevOps e CI/CD: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>Docker, Kubernetes, GitHub Actions, Terraform, Linux, Nginx</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="0" w:after="20"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• Bancos de Dados: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>PostgreSQL, MySQL, Redis, MongoDB, DynamoDB</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="0" w:after="60"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t>• Nuvem e Arquitetura: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>AWS, GCP, Microsserviços, Arquitetura Orientada a Eventos</w:t></w:r>
    </w:p>

    <!-- SECTION: RESUMO PROFISSIONAL -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/></w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="111827"/></w:rPr>
        <w:t>Resumo Profissional</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:pPr><w:spacing w:before="40" w:after="80"/><w:jc w:val="both"/></w:pPr>
      <w:r>
        <w:rPr><w:sz w:val="20"/></w:rPr>
        <w:t>Engenheiro de Software Sênior com mais de 5 anos de experiência no desenvolvimento e escalabilidade de sistemas backend de alta performance e microsserviços distribuídos. Histórico comprovado de entrega de resultados mensuráveis, como redução de 25% na latência de APIs e automação de fluxos críticos de negócio. Focado em arquiteturas limpas, testes automatizados (unitários e e2e) e modernização de sistemas legados com alta disponibilidade (99,9% uptime).</w:t>
      </w:r>
    </w:p>

    <!-- SECTION: EXPERIÊNCIAS PROFISSIONAIS -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/></w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="111827"/></w:rPr>
        <w:t>Experiências Profissionais</w:t>
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
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="374151"/></w:rPr><w:t>Engenheiro Full Stack Sênior</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="4000" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>São Paulo, SP (Remoto)</w:t></w:r></w:p>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Jul 2024 - Presente</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Aceleração de 90% na velocidade de configuração de telas com mixins reutilizáveis em Python/Django para clonagem profunda de entidades relacionais.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Eliminação de 100% do desperdício de tokens de APIs de IA em planos inativos via feature flags granulares com controle administrativo.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Automação integral da avaliação de código com pipeline de webhooks e microsserviço de correção automática por IA.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Redução de 90% no tempo de emissão de credenciais via API de validação de domínio e geração de certificados.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="200"/><w:spacing w:before="20" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="374151"/></w:rPr><w:t>• Contexto: </w:t></w:r>
      <w:r><w:rPr><w:i/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Plataforma SaaS corporativa focada em microsserviços de alto volume. Construção de ferramentas internas e integrações que eliminaram operações manuais no ecossistema.</w:t></w:r>
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
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="374151"/></w:rPr><w:t>Engenheiro de Software Full Stack</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="4000" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="60" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Remoto</w:t></w:r></w:p>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Jul 2023 - Jun 2024</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Aumento de 15% na performance dos servidores por meio de otimizações de framework, pool de conexões de banco de dados e modernização de dependências.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Redução de 20% no tempo de feedback da esteira de CI/CD com paralelização de testes automatizados via pytest-xdist em containers Docker.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Diminuição de 20x no tempo de resposta de endpoints críticos através de otimização de queries SQL, eliminação de gargalos N+1 e paginação indexada.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Economia de R$ 60 mil anuais em infraestrutura com desativação de workers ociosos e migração para arquitetura de API sob demanda.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="200"/><w:spacing w:before="20" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="374151"/></w:rPr><w:t>• Contexto: </w:t></w:r>
      <w:r><w:rPr><w:i/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Foco em confiabilidade e engenharia de performance backend — modernização de serviços legados e otimização de consultas no PostgreSQL.</w:t></w:r>
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
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="374151"/></w:rPr><w:t>Desenvolvedor Backend</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="4000" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="60" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>São Paulo, SP</w:t></w:r></w:p>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Jun 2022 - Jun 2023</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Blindagem da superfície de ataque da aplicação com bloqueio de robôs maliciosos e varreduras de vulnerabilidades na camada do proxy reverso Nginx.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Mitigação de 100% das perdas de leads por instabilidade de rede via desacoplamento de sincronizações de CRM em workers assíncronos Celery com retry exponencial.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:before="0" w:after="30"/></w:pPr>
      <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t>• Redução de 80% na latência de resposta do feed por meio de cache de resultados com Redis.</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="200"/><w:spacing w:before="20" w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="374151"/></w:rPr><w:t>• Contexto: </w:t></w:r>
      <w:r><w:rPr><w:i/><w:sz w:val="19"/><w:color w:val="4B5563"/></w:rPr><w:t>Desenvolvimento de funcionalidades backend e integrações arquiteturais entre microsserviços com alta cobertura de testes e observabilidade.</w:t></w:r>
    </w:p>

    <!-- SECTION: FORMAÇÃO ACADÊMICA -->
    <w:p>
      <w:pPr>
        <w:spacing w:before="120" w:after="40"/>
        <w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="111827"/></w:pBdr>
      </w:pPr>
      <w:r>
        <w:rPr><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="111827"/></w:rPr>
        <w:t>Formação Acadêmica</w:t>
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
          <w:p><w:pPr><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="21"/><w:color w:val="111827"/></w:rPr><w:t>Instituto de Tecnologia e Ciência</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Mestrado em Engenharia de Software e IA</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="3500" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Ago 2024 - Dez 2025</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
      <w:tr>
        <w:tc>
          <w:tcPr><w:tcW w:w="6500" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="21"/><w:color w:val="111827"/></w:rPr><w:t>Universidade Estadual de Tecnologia</w:t></w:r></w:p>
          <w:p><w:pPr><w:spacing w:before="0" w:after="40"/></w:pPr><w:r><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Bacharelado em Ciência da Computação</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr><w:tcW w:w="3500" w:type="dxa"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="40" w:after="0"/></w:pPr><w:r><w:rPr><w:sz w:val="20"/><w:color w:val="4B5563"/></w:rPr><w:t>Jan 2020 - Jun 2024</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>

    <!-- Page Setup -->
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="936" w:right="936" w:bottom="936" w:left="936" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""


def generate_docx(doc_xml: str, output_path: str):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', CONTENT_TYPES_XML)
        docx.writestr('_rels/.rels', PACKAGE_RELS_XML)
        docx.writestr('word/_rels/document.xml.rels', DOCUMENT_RELS_XML)
        docx.writestr('word/styles.xml', STYLES_XML)
        docx.writestr('word/document.xml', doc_xml)
    print(f"Generated {output_path}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    en_file = os.path.join(out_dir, "resume_template.docx")
    pt_file = os.path.join(out_dir, "resume_template_pt.docx")
    
    generate_docx(build_en_doc_xml(), en_file)
    generate_docx(build_pt_doc_xml(), pt_file)
