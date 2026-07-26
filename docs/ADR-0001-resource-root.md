# ADR-0001: Resource as the persistent root

Status: accepted.

All persistent domain objects inherit common identity, lifecycle, provenance, visibility and citation behavior from `Resource`. This is domain inheritance; storage may use joined-table inheritance or another representation when justified by measured performance.
