
# Purpose

The purpose of `mutation_effect_on_interactions_signal` is to explore the effect that mutations have on the interaction strength between species constituting a gene circuit (in this case an RNA circuit) and consequently the effect mutations have on the circuit's response to the input signal.

## Requirements

This script selects a set of circuits that will be used as a starting point for generating mutations from a table summarising the interaction strengths of various randomly generated circuits. These were previously generated by the `generate_species_templates` script and then tabulated with the `gather_interaction_stats` script, so these should be run first.

In the config file, specify as the source directory (`source_dir`) the directory that `gather_interaction_stats` tabulated the circuit statistics into. From there, the circuits are chosen by optional filters, for example a minimum bound on the number of species that are significantly interacting. Each circuit is mutated randomly using the `Evolver` class, whereby mutations are added to the circuit and defined abstractly to save memory using numbers as opposed to re-generating the entire string sequence of each species. 
