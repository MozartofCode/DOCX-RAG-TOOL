#!/usr/bin/env python
import sys
from rag_tool.crew import RagToolCrew
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

def run():
    """
    Run the crew.
    """
    inputs = {
        'question': 'What are the products and services of Bunchful?',
    }
    RagToolCrew().crew().kickoff(inputs=inputs)