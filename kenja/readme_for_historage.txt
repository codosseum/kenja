# README

This is a method-level repository (Historage).

## Notes for cloning
Case sensitive file system is preferable because method contents are stored in files named for their method names (and they are case sensitive).

## Original repository
This historage is converted from **$name**. You can get the original repository from: $url

## Commits in Historage
Although historage preserves the commit history of the original repository (dates and authors of commits, DAG relaitons, etc.), their SHA-1 values of commits are different because of contents in snapshots (method-level contents). Original SHA-1 values are stored in git notes and can be seen with git-show. The notes can be fetched with the following command.

git fetch origin refs/notes/*:refs/notes/*

## Version
This repository was created by kenja at version **$version**
