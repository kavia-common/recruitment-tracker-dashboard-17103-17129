#!/bin/bash
cd /home/kavia/workspace/code-generation/recruitment-tracker-dashboard-17103-17129/recruitment_dashboard_gui
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

