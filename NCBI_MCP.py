import os
from smolagents import ToolCallingAgent, ToolCollection
from smolagents.models import OpenAIServerModel
from mcp import StdioServerParameters

SECRET_PATH = os.path.join(os.path.dirname(__file__), "secret.txt")
NCBI_API_PATH = os.path.join(os.path.dirname(__file__), "NCBI_API_KEY.txt")

with open(SECRET_PATH, "r", encoding="utf-8") as f:
    api_key = f.read().strip()

with open(NCBI_API_PATH, "r", encoding="utf-8") as f:
    ncbi_api_key = f.read().strip()

os.environ["NEBIUS_API_KEY"] = api_key
os.environ['NCBI_API_KEY'] = ncbi_api_key
os.environ['NCBI_EMAIL'] = "raitzev2004@gmail.com"

def set_server_stdio():
    server_script_path = r"D:\PROGRAMMS\Python Projects\NCBI MCP\ncbi-mcp-server\ncbi_mcp_server\server.py"
    return StdioServerParameters(
        command="python",
        args=[server_script_path],
        env={
            "NCBI_API_KEY": os.environ.get("NCBI_API_KEY", ""),
            "NCBI_EMAIL": os.environ.get("NCBI_EMAIL", "")
        }
    )

def set_model():
    return OpenAIServerModel(
        model_id="Qwen/Qwen3-235B-A22B-Instruct-2507",
        api_key=os.environ["NEBIUS_API_KEY"],
        api_base="https://api.studio.nebius.com/v1/",
        temperature=0.1,
        max_tokens=4000,
    )

def set_debug_prompt(protein: str) -> str:
    return f"""
Investigate the protein: {protein} and also DIAGNOSE any system issues you encounter.

Your mission:
1. **DATA COLLECTION**: Get basic information about {protein}
2. **SYSTEM DIAGNOSIS**: Identify and explain any errors or limitations
3. **WORKAROUND STRATEGY**: Show how you adapt to problems

When you encounter errors, provide this analysis:
### Error Diagnosis:
- **What failed**: [Tool and parameters]
- **Error message**: [Exact error]  
- **Likely cause**: [Your analysis of the problem]
- **Workaround**: [How you're adapting]

Required output sections:
### 1. Protein Information Found
### 2. System Issues Encountered 
### 3. Error Analysis & Solutions
### 4. Successful Data Retrieved

Be transparent about what works and what doesn't.
"""

def set_system_prompt(protein: str) -> str:
    return f"""
# 🧬 SUPER-BIOINFORMATICIAN AGENT - HACKATHON MODE 🚀

## MISSION
Extract MAXIMUM actionable data for protein engineering, longevity, and sequence-to-function mapping. Be aggressive but structured.

## CRITICAL PARAMETERS

**search_ncbi**:  
- database: string ('gene', 'protein', 'pubmed', ...)  
- query: string  
- max_results: int (default 5, max 20)  
- start_index: int (default 0)  
- sort_order: string REQUIRED ('relevance' or 'date')  

**NEVER**: null/None, ids as string  
**ALWAYS**: proper types  

## TOOL USAGE

**Use**: search_ncbi → summarize_records → find_related_records  
**Avoid**: fetch_records (huge XML), blast_search (large sequences)

## WORKFLOW
1. search_ncbi('gene', '{protein} human') → Gene ID  
2. summarize_records('gene', [ID]) → basic info  
3. find_related_records('gene','protein',[ID]) → proteins  
4. search_ncbi('pubmed', '{protein} mutation') → literature  
5. summarize_records('pubmed', [PMIDs]) → summaries  

**Required data**: all protein isoforms, transcript variants, sequence intervals, modifications; use summaries, not full records.

## SEARCH STRATEGY
- Phase 1: rapid parallel searches (gene/protein IDs, mutation/longevity, domain/function)  
- Phase 2: targeted mining (“{protein} phosphorylation site mutation”, cancer mutation effects, lifespan extension, ortholog conservation)  

**Synthesize**: mutations → functional effects → longevity → engineering targets

## DATA COVERAGE
- Core Sequence-to-Function: aa intervals, modifications, mutation effects, functional outcomes, engineering insights  
- Comprehensive Biology: PTM networks, small molecule interactions, structural domains, therapeutic context  
- Longevity Focus: lifespan changes, aging polymorphisms, species adaptations  
- Isoforms & Transcripts: all protein isoforms & transcript variants, sequence links, isoform-specific modifications, map all intervals/modifications to each isoform and transcript

## OUTPUT STRUCTURE
1. Protein Identification & Architecture  
2. Sequence-to-Function Mapping (table)  
3. PTM Networks  
4. Small Molecule Interactions  
5. Longevity & Aging Associations  
6. Protein Engineering Blueprint  
7. Evolutionary Insights  

**Structured Table Template**:

| Gene/Protein | UniProt/Acc | Sequence | Isoform/Transcript | Interval | Modification | Function | Evidence/PMID | Longevity | Notes |
|-------------|------------|---------|-----------------|---------|-------------|---------|---------------|----------|------|

## AGENT RULES
- Be persistent: try synonyms & related terms  
- Be specific: exact positions, mechanistic explanations, quantitative data  
- Map every modification/interval to all isoforms & transcripts  
- Be action-oriented: every data point → engineering insight  
- Handle failures gracefully: alternative queries, rate limits  

**Success metrics**: ≥8 sequence modifications, ≥5 longevity associations, complete PTM & small molecule coverage, actionable blueprint, cross-species evolutionary insights.

YOU ARE THE ULTIMATE BIOINFORMATICS HACKATHON WEAPON — EXTRACT EVERYTHING! 💥
"""


def set_user_prompt(protein: str) -> str:
    return f"""
# 🚀 ULTIMATE HACKATHON EXTRACTION: {protein.upper()}

## CRITICAL MISSION
Extract COMPREHENSIVE sequence→function knowledge for {protein} with AGGRESSIVE, reproducible data mining for protein engineering and longevity applications. Produce both detailed narrative and bioinformatics-ready structured outputs.

## EXECUTION STRATEGY

PHASE 1 — RAPID MULTI‑DATABASE ASSAULT
- Run parallel searches across gene/protein/literature resources.
- Extract all relevant IDs (Gene, RefSeq NM/NP, UniProt) and cross-reference immediately.
- Use bold, specific queries.

PHASE 2 — DEEP MECHANISTIC MINING
- Find specific modifications (phospho, ubiquitin, acetylation), disease/cancer mutations, and longevity variants.
- Link molecular changes to mechanistic functional outcomes.
- Extract quantitative data when available (lifespan % change, fold-change, EC50).

PHASE 3 — ENGINEERING SYNTHESIS
- Produce actionable design strategies (mutations, swaps, degrons, promoters).
- Highlight domain-specific engineering opportunities and risks.

## MINIMUM DATA REQUIREMENTS (MUST)
A. CORE (non-negotiable)
- ≥8 specific sequence modifications with exact positions and effects (aa coords).
- Mechanistic explanations and experimental validation (PMIDs).

B. COMPREHENSIVE BIOLOGY
- PTM network, small-molecule interactome, domain boundaries, therapeutic context.

C. LONGEVITY FOCUS
- Lifespan effects in models, aging polymorphisms (rsIDs), species adaptations.

D. ENGINEERING BLUEPRINT
- Top 5 engineering targets with concrete strategies, domain‑swap suggestions, and safety notes.

E. ISOFORMS & TRANSCRIPTS (BIOINFORMATICIAN REQUEST)
- ALL protein isoforms (RefSeq NP, UniProt) with sequence links.
- ALL transcript variants (RefSeq NM) with sequence links.
- **Map every interval/modification to each isoform AND to transcript coordinates when possible.**
- Provide sequence excerpts (±10 aa) for each interval.

## SEARCH QUERIES (examples)
Parallel basics:
1. "{protein} human gene protein"  
2. "{protein} mutation functional effect"  
3. "{protein} phosphorylation ubiquitination"  
4. "{protein} longevity lifespan extension"  
5. "{protein} small molecule activator inhibitor"  
6. "{protein} ortholog conservation"  
7. "{protein} isoforms RefSeq"  
8. "{protein} splice variants transcript"

Deep-dive examples:
- "{protein} cysteine mutation Keap1 binding"  
- "{protein} transgenic mouse lifespan % change"  
- "{protein} cancer mutation gain-of-function"  
- "{protein} domain swap functional characterization"  
- "{protein} isoform specific function"

## REQUIRED OUTPUT STRUCTURE (order matters)
1. Protein Identification & Architecture (Gene IDs, UniProt, RefSeq, chromosomal location)  
2. Protein Sequences & Isoforms — tables with direct NCBI/UniProt links (all isoforms & transcripts) **+ sequence excerpts**  
3. Comprehensive Sequence→Function Mapping — per-isoform, per-transcript rows (see template)  
4. PTM Network (kinases, E3s, sites)  
5. Small Molecule Interactome (activators/inhibitors, mechanism, binding sites)  
6. Quantitative Longevity Associations (model, intervention, % lifespan change, PMID)  
7. Protein Engineering Blueprint (top targets, domain swaps, cautions)  
8. Evolutionary Design Principles (ortholog comparisons, conservation metrics)

## DETAILED TABLE REQUIREMENTS
- Produce BOTH: (A) human-readable Markdown table(s) AND (B) a machine-friendly structured block (clear labeled fields).
- Every table row must include: **Isoform/Transcript (Ref), Seq ID (NM/NP/UniProt), Sequence link, Interval (start–end, coordinate system), Sequence excerpt (±10 aa), Modification, Functional change, Evidence (PMID/URL), Longevity association (if any), Notes/provenance (date, DB).**
- If a value is unavailable, explicitly use `—`.

### STRUCTURED SEQUENCE→FUNCTION TABLE (example template)
| Interval (aa/nt) | Isoform/Transcript (Ref) | Seq ID | Sequence link | Sequence excerpt | Modification | Functional change | Evidence (PMID/URL) | Longevity |
|------------------|--------------------------|--------|---------------|------------------|--------------|-------------------|----------------------|----------|
|                  |                          |        |               |                  |              |                   |                      |          |

## RESPONSE STYLE & RULES
- Be exhaustive, mechanistic, and explicit (exact residue numbers).  
- Prefer primary literature (PMID/PMC) and authoritative DBs (NCBI, UniProt, AlphaFold, InterPro). Cite everything.  
- Preserve full narrative detail; structured tables are **additive**.  
- If limitations occur (rate limits, missing data), report them in a clear diagnostic section with alternative queries and next steps.

## SUCCESS METRICS
- ≥8 distinct sequence modifications with mechanisms and evidence.  
- ≥5 longevity associations with citations.  
- Full isoform & transcript coverage with sequence links.  
- Actionable engineering blueprint with domain-specific rationale.

BE AGGRESSIVE — extract every usable data point, map it precisely to isoforms/transcripts, and produce both human- and machine-friendly outputs. 💥
"""


def run_ncbi_query(gene: str) -> str:
    """Исправленная версия без max_turns"""
    try:
        with ToolCollection.from_mcp(
            server_parameters=set_server_stdio(),
            trust_remote_code=True,
            structured_output=False
        ) as tools:
            
            agent = ToolCallingAgent(
                model=set_model(),
                tools=[*tools.tools],
                add_base_tools=False,
                max_steps=4,  
            )
            agent.prompt_templates["system_prompt"] = set_system_prompt(gene)
            user_message = set_user_prompt(gene)
            result = agent.run(user_message)
        return result
    except Exception as e:
        return f"Ошибка: {e}"

def test_tools():
    try:
        with ToolCollection.from_mcp(
            server_parameters=set_server_stdio(),
            trust_remote_code=True,
            structured_output=False
        ) as tools:
            print("✅ Доступные инструменты:")
            for tool in tools.tools:
                print(f"   - {tool.name}")
            return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def run_super_agent(protein: str) -> str:
    """Запуск супер-агента для хакатона с увеличенным количеством шагов"""
    try:
        with ToolCollection.from_mcp(
            server_parameters=set_server_stdio(),
            trust_remote_code=True,
            structured_output=False
        ) as tools:
            
            agent = ToolCallingAgent(
                model=set_model(),
                tools=[*tools.tools],
                add_base_tools=False,
                max_steps=5,  
            )
            agent.prompt_templates["system_prompt"] = set_system_prompt(protein)
            user_message = set_user_prompt(protein)
            result = agent.run(user_message)
        return result
    except Exception as e:
        return f"Ошибка: {e}"
    
def run_diagnostic(protein: str) -> str:
    """Запуск с диагностическим промптом"""
    try:
        with ToolCollection.from_mcp(
            server_parameters=set_server_stdio(),
            trust_remote_code=True,
            structured_output=False
        ) as tools:
            
            agent = ToolCallingAgent(
                model=set_model(),
                tools=[*tools.tools],
                add_base_tools=False,
                max_steps=6,  
            )
            agent.prompt_templates["system_prompt"] = set_system_prompt(protein)
            user_message = set_debug_prompt(protein)  
            result = agent.run(user_message)
        return result
    except Exception as e:
        return f"Ошибка: {e}"
    

if __name__ == "__main__":
    print("🚀 ЗАПУСК СУПЕР-АГЕНТА ДЛЯ ХАКАТОНА...")
    result = run_super_agent("nrf2")  
    print(result)