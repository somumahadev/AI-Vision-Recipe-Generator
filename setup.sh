#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
enableXsrfProtection = true\n\
\n\
[theme]\n\
primaryColor = \"#FF6B6B\"\n\
backgroundColor = \"#0E1117\"\n\
secondaryBackgroundColor = \"#262730\"\n\
textColor = \"#FAFAFA\"\n\
" > ~/.streamlit/config.toml