#!/bin/sh

  if [ "$1" = "-V" ] || [ "$1" = "--version" ]; then
    python3 main.py -V
  elif [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    python3 main.py -h
  elif { [ "$1" = "--type" ] && { [ "$2" = "Fan" ] || [ "$2" = "Power Supply" ];};} || { [ "$1" = "-T" ] && { [ "$2" = "Fan" ] || [ "$2" = "Power Supply" ];};}; then
    python3 main.py -T "$2" | jq
  else
    python3 main.py -h
  fi