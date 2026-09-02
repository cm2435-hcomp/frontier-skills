#!/usr/bin/env bash
set -euo pipefail

phase="${1:-}"
if [[ "$phase" != "completion" && "$phase" != "combined" && "$phase" != "full" ]]; then
  echo "usage: $0 completion|combined|full" >&2
  exit 2
fi

for name in HAI_API_KEY OPENAI_API_KEY WANDB_API_KEY OSWORLD_V2_TASK_CLASS_DIR; do
  if [[ -z "${!name:-}" ]]; then
    echo "$name must be exported before launching OSW-2 through Sky" >&2
    exit 2
  fi
done

hai_checkout="${HAI_CHECKOUT:-/Users/charlie.masters/Desktop/hcomp/.worktrees/skill-registry-runtime}"
registry_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
asset_uri="s3://agent-calltraces/benchmark-inputs/osworld-v2/v2026.06.24/assets-gated.tar.gz"
asset_sha="18ead7e13a2745571d97527d41ff3560e18e7b2d9372a606980323b4c8d917bd"
stamp="$(date +%Y%m%d-%H%M%S)"

case "$phase" in
  completion)
    task_override="task_suite.task_collection=[009,040,055,070,083,102,087,090]"
    treatment_config="$registry_root/evaluations/agents/osw2-completion.yaml"
    ;;
  combined)
    task_override="task_suite.task_collection=[040,049,080,087,090,102,108,044,053,057,036,062,097]"
    treatment_config="$registry_root/evaluations/agents/osw2-registry.yaml"
    ;;
  full)
    task_override="task_suite.task_collection=[]"
    treatment_config="$registry_root/evaluations/agents/osw2-registry.yaml"
    ;;
esac

launch() {
  local arm="$1"
  local config="$2"
  (
    cd "$hai_checkout"
    AWS_PROFILE="${AWS_PROFILE:-training}" uv run agent-tasks-sky \
      task_suite=osworld_v2 \
      "task_suite.task_class_dir=$OSWORLD_V2_TASK_CLASS_DIR" \
      "task_suite.env.asset_bundle_s3_uri=$asset_uri" \
      "task_suite.env.asset_bundle_sha256=$asset_sha" \
      task_suite.env.instance_type=t3.xlarge \
      'task_suite.accepted_dependency_receipts=[osworld-v2-web-2026.06.24,osworld-v2-gitlab-2026.06.24]' \
      "$task_override" \
      agent=sagent_threaded \
      agent.enable_trace_writer=true \
      "agent_config=$config" \
      scheduler=semaphore \
      scheduler.concurrency=50 \
      scheduler.stagger_delay_s=1 \
      n_retries_on_exception=1 \
      'callbacks=[wandb,save_evaluation]' \
      "display_name=oswv2-skills-$phase-$arm-$stamp"
  )
}

launch control "$registry_root/evaluations/agents/osw2-control.yaml"
launch treatment "$treatment_config"
