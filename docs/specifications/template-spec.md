# Template Specification

Status: Draft
Version: 0.1.0

## Purpose

Defines the standard templates used by all artifact types in Apple Agent Kit to ensure consistency, interoperability, and deterministic parsing by AI coding agents.

## Supported Templates

- Knowledge Contract
- Skill
- Workflow
- Reference
- Validation Report

## General Requirements

Every template MUST:

- Include the standard metadata block.
- Follow the defined section order.
- Be human-readable and AI-parseable.
- Use Markdown only.
- Avoid unnecessary prose.

## Metadata Standard

Required fields:

- id
- title
- version
- status
- artifact_type
- last_updated

Artifact-specific metadata may extend this base schema.

## Section Ordering

Templates must preserve a deterministic section order. Required sections may not be reordered.

## Naming Rules

- Filenames use lowercase kebab-case.
- One artifact per file.
- Names should describe responsibility, not implementation.

## Linking Rules

- Use relative Markdown links.
- Do not link to generated files.
- Link only to authoritative artifacts.

## Validation Checklist

- Metadata valid
- Section order correct
- Naming convention followed
- Links resolve successfully
- Template matches artifact type
