from agent_smith_ai.utility_agent import UtilityAgent

import textwrap
import os
from typing import Any, Dict


## A UtilityAgent can call API endpoints and local methods
class GoAPIAgent(UtilityAgent):

    def __init__(self, name, model="gpt-3.5-turbo-16k-0613", openai_api_key=None):
        ## define a system message
        system_message = textwrap.dedent(f"""
            You are the Gene Ontology Assistant, an AI-powered chatbot that can answer questions about data from the 
            Gene Ontology Consortium API interface. You can search for entities such as genes, gene ontology terms, 
            and go-cam models by name to get the associated ontology identifier. You can retrieve associations between 
            entities via their identifiers. Users may use synonyms such as 'adenylyl cyclase activity' or 'cAMP 
            generating peptide activity'. DO NOT assume the user is familiar with gene ontology terminology. 
            ALWAYS add additional information such as lay descriptions of gene function, biological processes, and 
            cellular components. 
            IMPORTANT: Include markdown-formatted links to the Gene Ontology Consortium for all results using the 
            templates provided by function call responses, AND include links to publications if provided.
            """).strip()

        super().__init__(name,  # Name of the agent
                         system_message,  # Openai system message
                         model=model,  # Openai model name
                         openai_api_key=openai_api_key,  # API key; will default to OPENAI_API_KEY env variable
                         auto_summarize_buffer_tokens=500,
                         # Summarize and clear the history when fewer than this many tokens remains in the context
                         # window. Checked prior to each message sent to the model.
                         summarize_quietly=False,  # If True, do not alert the user when a summarization occurs
                         max_tokens=None,  # maximum number of tokens this agent can bank (default: None, no limit)
                         token_refill_rate=50000.0 / 3600.0)  # number of tokens to add to the bank per second

        ## register some API endpoints (inherited from UtilityAgent)
        ## the openapi.json spec must be available at the spec_url:
        ##    callable endpoints must have a "description" and "operationId"
        ##    params can be in body or query, but must be fully specified
        self.register_api(name="geneontology",
                          spec_url="http://0.0.0.0:8080/openapi.json",
                          base_url="http://0.0.0.0:8080/",
                          callable_endpoints=['get_term_metadata_by_id_api_ontology_term__id__get'])
