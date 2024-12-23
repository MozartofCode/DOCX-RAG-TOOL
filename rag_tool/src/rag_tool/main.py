#!/usr/bin/env python
import sys
from rag_tool.crew import RagToolCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        'question': ''
    }
    RagToolCrew().crew().kickoff(inputs=inputs)