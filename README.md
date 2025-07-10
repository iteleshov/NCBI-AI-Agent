# NCBI MCP Server

A Model Context Protocol (MCP) server that provides access to NCBI E-utilities and BLAST tools. This server enables AI applications like Claude Desktop to search, fetch, and analyze biological data from NCBI databases in an intelligent, agentic manner.

## Features

### 🔧 **Tools Available**
- **search_ncbi** - Search any NCBI database with natural language queries
- **fetch_records** - Retrieve full records in various formats (XML, FASTA, GenBank, etc.)  
- **summarize_records** - Get structured summaries with titles, authors, journals, etc.
- **find_related_records** - Discover related records across different databases
- **blast_search** - Perform BLAST sequence alignment searches
- **list_databases** - Get all available NCBI databases
- **get_database_info** - Get detailed information about specific databases

### 📚 **Resources Available**
- **ncbi://databases** - Comprehensive list of NCBI databases with descriptions
- **ncbi://blast-programs** - Guide to BLAST programs and databases

### 🧠 **Agentic Behavior Examples**

When you ask Claude Desktop questions, it will intelligently use multiple tools together:

**Example Query:** *"Find recent papers about CRISPR gene editing in humans and get me the abstracts"*

Claude will automatically:
1. Use `search_ncbi` to search PubMed for CRISPR papers
2. Use `summarize_records` to get abstracts and metadata
3. Present the information in a readable format

**Example Query:** *"I have this DNA sequence ATCGATCGATCG - what protein does it code for?"*

Claude will automatically:
1. Use `blast_search` with blastx program to translate and search against protein databases
2. Analyze the results to identify the most likely protein matches
3. Possibly use `fetch_records` to get more details about matches

**Example Query:** *"Show me all the genome assemblies for E. coli and their quality metrics"*

Claude will automatically:
1. Use `search_ncbi` on the assembly database for E. coli
2. Use `fetch_records` to get detailed assembly information
3. Parse and present the quality metrics in a structured way

## Quick Start

### Installation

Install using uv (recommended):
```bash
uv add ncbi-mcp-server
```

Or with pip:
```bash
pip install -e .
```

### Configuration

1. **Get an NCBI API Key (Recommended)**
   - Visit: https://www.ncbi.nlm.nih.gov/account/settings/
   - Generate an API key for higher rate limits (10 req/sec vs 3 req/sec)

2. **Set Environment Variables**
   ```bash
   cp env.example .env
   # Edit .env with your credentials
   export NCBI_API_KEY="your_api_key_here"
   export NCBI_EMAIL="your.email@example.com"
   ```

### Usage with Claude Desktop

1. **Install in Claude Desktop:**
   ```bash
   mcp install ncbi_mcp_server/server.py --name "NCBI Research Assistant"
   ```

2. **Or add to Claude config manually:**
   ```json
   {
     "mcpServers": {
       "ncbi": {
         "command": "python",
         "args": ["/path/to/ncbi_mcp_server/server.py"],
         "env": {
           "NCBI_API_KEY": "your_api_key",
           "NCBI_EMAIL": "your.email@example.com"
         }
       }
     }
   }
   ```

3. **Start using it!** Ask Claude questions like:
   - "Find the latest research on Alzheimer's disease genetics"
   - "BLAST this protein sequence and tell me what it is"
   - "Get me information about the human genome assembly"
   - "Find papers by author John Smith about cancer research"

### Development & Testing

Test your server with the MCP Inspector:
```bash
mcp dev ncbi_mcp_server/server.py
```

Run with custom environment:
```bash
NCBI_API_KEY=your_key mcp dev ncbi_mcp_server/server.py
```

## Supported NCBI Databases

The server works with all NCBI databases including:

### Literature & References
- **pubmed** - PubMed biomedical literature  
- **pmc** - PubMed Central full-text articles
- **books** - NCBI Bookshelf

### Sequences
- **nucleotide** - Nucleotide sequences
- **protein** - Protein sequences  
- **nuccore** - Nucleotide collection (GenBank+EMBL+DDBJ+PDB+RefSeq)

### Genomes & Assemblies  
- **genome** - Genome sequencing projects
- **assembly** - Genome assemblies
- **gene** - Gene-centered information

### Specialized Databases
- **sra** - Sequence Read Archive
- **taxonomy** - Taxonomic information  
- **snp** - Single Nucleotide Polymorphisms
- **clinvar** - Clinical significance of genomic variation
- **mesh** - Medical Subject Headings

## BLAST Programs Supported

- **blastn** - Nucleotide vs nucleotide
- **blastp** - Protein vs protein  
- **blastx** - Translated nucleotide vs protein
- **tblastn** - Protein vs translated nucleotide
- **tblastx** - Translated nucleotide vs translated nucleotide

## Example Workflows

### Literature Research
```
User: "Find recent papers about COVID-19 vaccines effectiveness"
→ Claude automatically searches PubMed
→ Gets paper summaries with abstracts  
→ Presents organized results with key findings
```

### Sequence Analysis
```  
User: "Analyze this DNA sequence: ATCGATCGATCGAAATTTCCCGGG"
→ Claude runs appropriate BLAST search
→ Identifies similar sequences and organisms
→ Explains biological significance
```

### Comparative Genomics
```
User: "Compare the genome assemblies of different E. coli strains"  
→ Claude searches assembly database
→ Fetches assembly statistics
→ Compares quality metrics and completeness
```

## Rate Limits & Best Practices

- **With API Key**: 10 requests/second  
- **Without API Key**: 3 requests/second
- **Always provide email**: Required by NCBI terms of service
- **Be respectful**: Don't overwhelm NCBI servers

## Troubleshooting

### Common Issues

1. **Rate Limiting Errors**
   - Get an NCBI API key for higher limits
   - Reduce request frequency

2. **No Results Found**  
   - Check database name spelling
   - Try broader search terms
   - Verify sequence format for BLAST

3. **Connection Errors**
   - Check internet connectivity
   - Verify NCBI services are operational

### Debug Mode

Run with verbose logging:
```bash
DEBUG=1 mcp dev ncbi_mcp_server/server.py
```

## Contributing

Contributions welcome! Please see the development setup:

```bash
git clone https://github.com/your-username/ncbi-mcp-server.git
cd ncbi-mcp-server
uv sync
uv run mcp dev ncbi_mcp_server/server.py
```

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Built with the [Model Context Protocol](https://modelcontextprotocol.io)
- Uses [Biopython](https://biopython.org/) for BLAST functionality
- Powered by [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
