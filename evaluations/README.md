# Evaluation configs

`osw2-control.yaml` is the resolved agent snapshot from accepted W&B run `o8z81viw` at HAI commit
`80f53108ba52c39c919922736bad359bcf5de7ba`, including its model, prompt, budgets, compactor, desktop tools, and
same-workstation shell tools. Its branch-only budget-alert callback is omitted because the skill machinery stacks on
current `main`; both experiment arms omit it identically.

`osw2-registry.yaml` inherits that snapshot and changes only `agent.skill_registry`. `osw2-completion.yaml` is the
isolated completion-verification treatment. Both pin release digest
`dbc158c7c4f27c0297ec06c21de7e82e78d2f89ca1d7d13d19c4a5531bad93fd`.

The current evaluation snapshot explicitly uses the temporary public release mirror at
`cm2435-hcomp/frontier-skills` because the implementation account cannot create the intended organization repository.
The runtime's production default remains `hcompai/frontier-skills`; remove the override after transfer or mirroring.

The run command must keep the OSW-2 dataset, task list, scheduler, retry policy, and both `wandb` and
`save_evaluation` callbacks identical between arms. Known environment, evaluator, and serving failures remain in raw
counts but are excluded from the skill-effect denominator.

`run_osw2_ablation.sh` launches an exact matched pair for the isolated completion gate, combined audited slice, or
full suite. It deliberately has no `all` mode: inspect each phase's evidence before spending on the next one. Export
`HAI_API_KEY`, `WANDB_API_KEY`, and `OSWORLD_V2_TASK_CLASS_DIR`; the script fails before submission when any is absent.
The launcher pins the accepted web and GitLab dependency receipts from the reference run so the full task inventory
does not silently change between arms.
