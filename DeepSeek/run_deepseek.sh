#!/bin/sh

##################################################################
##
##  Install Ollama and deepseek-r1:1.5b
##
##################################################################

## sudo to install
curl -fsSL https://ollama.com/install.sh | sudo sh

## regular user to run the LLM
ollama run deepseek-r1:1.5b

